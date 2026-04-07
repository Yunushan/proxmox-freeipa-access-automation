#!/usr/bin/env python3
from __future__ import annotations

import hmac
import json
import logging
import os
import queue
import shlex
import ssl
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_ALLOWED_PHASES = ("post-start", "post-migrate")


def parse_bool(raw: str | None, default: bool) -> bool:
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def parse_csv(raw: str | None, default: tuple[str, ...]) -> tuple[str, ...]:
    if raw is None:
        return default
    values = [item.strip() for item in raw.split(",")]
    normalized = tuple(item for item in values if item)
    return normalized or default


def resolve_optional_path(base_dir: Path, raw: str | None) -> Path | None:
    if raw is None or raw.strip() == "":
        return None
    path = Path(raw.strip())
    return path if path.is_absolute() else (base_dir / path).resolve()


@dataclass(frozen=True)
class Config:
    bind: str
    port: int
    webhook_path: str
    health_path: str
    token: str
    allowed_phases: tuple[str, ...]
    debounce_seconds: int
    pre_run_delay_seconds: int
    retry_count: int
    retry_delay_seconds: int
    repo_dir: Path
    playbook: Path
    inventory: Path | None
    ansible_playbook_bin: str
    ansible_extra_args: str
    tls_certfile: Path | None
    tls_keyfile: Path | None


def load_config() -> Config:
    repo_dir = resolve_optional_path(ROOT_DIR, os.getenv("PFA_REPO_DIR")) or ROOT_DIR
    playbook = resolve_optional_path(repo_dir, os.getenv("PFA_PLAYBOOK")) or (repo_dir / "playbooks" / "proxmox-vm-event.yml")
    inventory = resolve_optional_path(repo_dir, os.getenv("PFA_INVENTORY"))
    tls_certfile = resolve_optional_path(repo_dir, os.getenv("PFA_TLS_CERTFILE"))
    tls_keyfile = resolve_optional_path(repo_dir, os.getenv("PFA_TLS_KEYFILE"))
    token = os.getenv("PFA_WEBHOOK_TOKEN", "").strip()
    if token == "":
        raise RuntimeError("PFA_WEBHOOK_TOKEN must be set for the Proxmox event webhook.")

    return Config(
        bind=os.getenv("PFA_WEBHOOK_BIND", "0.0.0.0").strip(),
        port=int(os.getenv("PFA_WEBHOOK_PORT", "8085").strip()),
        webhook_path=os.getenv("PFA_WEBHOOK_PATH", "/hooks/proxmox-vm-event").strip(),
        health_path=os.getenv("PFA_HEALTH_PATH", "/healthz").strip(),
        token=token,
        allowed_phases=parse_csv(os.getenv("PFA_ALLOWED_PHASES"), DEFAULT_ALLOWED_PHASES),
        debounce_seconds=int(os.getenv("PFA_DEBOUNCE_SECONDS", "5").strip()),
        pre_run_delay_seconds=int(os.getenv("PFA_PRE_RUN_DELAY_SECONDS", "20").strip()),
        retry_count=int(os.getenv("PFA_RETRY_COUNT", "2").strip()),
        retry_delay_seconds=int(os.getenv("PFA_RETRY_DELAY_SECONDS", "30").strip()),
        repo_dir=repo_dir,
        playbook=playbook,
        inventory=inventory,
        ansible_playbook_bin=os.getenv("PFA_ANSIBLE_PLAYBOOK_BIN", "ansible-playbook").strip(),
        ansible_extra_args=os.getenv("PFA_ANSIBLE_EXTRA_ARGS", "").strip(),
        tls_certfile=tls_certfile,
        tls_keyfile=tls_keyfile,
    )


class EventWebhookServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, server_address: tuple[str, int], handler_class: type[BaseHTTPRequestHandler], config: Config, runner: "EventRunner") -> None:
        super().__init__(server_address, handler_class)
        self.config = config
        self.runner = runner


class EventRunner:
    def __init__(self, config: Config) -> None:
        self.config = config
        self._queue: queue.Queue[dict[str, Any] | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._run_loop, name="proxmox-event-runner", daemon=True)

    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        self._queue.put(None)
        self._thread.join(timeout=5)

    def submit(self, event: dict[str, Any]) -> None:
        self._queue.put(event)

    def _run_loop(self) -> None:
        while not self._stop_event.is_set():
            first_event = self._queue.get()
            if first_event is None:
                break

            batched_events = [first_event]
            batch_deadline = time.monotonic() + max(self.config.debounce_seconds, 0)
            while True:
                remaining = batch_deadline - time.monotonic()
                if remaining <= 0:
                    break
                try:
                    next_event = self._queue.get(timeout=remaining)
                except queue.Empty:
                    break
                if next_event is None:
                    self._stop_event.set()
                    break
                batched_events.append(next_event)

            if self.config.pre_run_delay_seconds > 0:
                logging.info(
                    "Waiting %s seconds before running the event playbook for %s queued Proxmox event(s).",
                    self.config.pre_run_delay_seconds,
                    len(batched_events),
                )
                time.sleep(self.config.pre_run_delay_seconds)

            self._run_playbook_with_retries(batched_events)

    def _run_playbook_with_retries(self, batched_events: list[dict[str, Any]]) -> None:
        attempts = max(self.config.retry_count, 0) + 1
        for attempt in range(1, attempts + 1):
            result = self._run_playbook_once(batched_events)
            if result.returncode == 0:
                return
            if attempt == attempts:
                logging.error(
                    "The event playbook failed after %s attempt(s).",
                    attempts,
                )
                return
            logging.warning(
                "The event playbook failed on attempt %s/%s. Retrying in %s seconds.",
                attempt,
                attempts,
                self.config.retry_delay_seconds,
            )
            time.sleep(self.config.retry_delay_seconds)

    def _run_playbook_once(self, batched_events: list[dict[str, Any]]) -> subprocess.CompletedProcess[str]:
        vmids = sorted(
            {
                str(event.get("vmid", "")).strip()
                for event in batched_events
                if str(event.get("vmid", "")).strip() != ""
            }
        )
        nodes = sorted(
            {
                str(event.get("node_fqdn") or event.get("node") or "").strip()
                for event in batched_events
                if str(event.get("node_fqdn") or event.get("node") or "").strip() != ""
            }
        )
        extra_vars = {
            "linux_ipa_proxmox_discovery_vmids": vmids,
            "proxmox_event_batch": batched_events,
            "proxmox_event_batch_size": len(batched_events),
            "proxmox_event_last": batched_events[-1],
            "proxmox_event_nodes": nodes,
            "proxmox_event_vmids": vmids,
        }

        command = [self.config.ansible_playbook_bin]
        if self.config.inventory is not None:
            command.extend(["-i", str(self.config.inventory)])
        if self.config.ansible_extra_args:
            command.extend(shlex.split(self.config.ansible_extra_args))
        command.extend(["--extra-vars", json.dumps(extra_vars, separators=(",", ":"))])
        command.append(str(self.config.playbook))

        logging.info(
            "Running event playbook for VMIDs %s with command: %s",
            ", ".join(vmids) if vmids else "<none>",
            " ".join(command),
        )
        result = subprocess.run(
            command,
            cwd=self.config.repo_dir,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.stdout.strip():
            logging.info("ansible-playbook stdout:\n%s", result.stdout.rstrip())
        if result.stderr.strip():
            logging.warning("ansible-playbook stderr:\n%s", result.stderr.rstrip())
        if result.returncode == 0:
            logging.info("Event playbook completed successfully for VMIDs %s.", ", ".join(vmids) if vmids else "<none>")
        else:
            logging.error("Event playbook exited with rc=%s.", result.returncode)
        return result


class ProxmoxEventWebhookHandler(BaseHTTPRequestHandler):
    server_version = "ProxmoxFreeIPAWebhook/1.0"

    @property
    def config(self) -> Config:
        return self.server.config  # type: ignore[attr-defined]

    @property
    def runner(self) -> EventRunner:
        return self.server.runner  # type: ignore[attr-defined]

    def log_message(self, fmt: str, *args: Any) -> None:
        logging.info("%s - %s", self.address_string(), fmt % args)

    def do_GET(self) -> None:
        if self.path != self.config.health_path:
            self._send_json(404, {"status": "not_found"})
            return
        self._send_json(200, {"status": "ok"})

    def do_POST(self) -> None:
        if self.path != self.config.webhook_path:
            self._send_json(404, {"status": "not_found"})
            return
        if not self._is_authorized():
            self._send_json(403, {"status": "forbidden"})
            return

        raw_length = self.headers.get("Content-Length", "0").strip() or "0"
        try:
            content_length = int(raw_length)
        except ValueError:
            self._send_json(400, {"status": "invalid_content_length"})
            return

        body = self.rfile.read(content_length)
        try:
            payload = json.loads(body.decode("utf-8"))
        except json.JSONDecodeError:
            self._send_json(400, {"status": "invalid_json"})
            return

        phase = str(payload.get("phase", "")).strip()
        vmid = str(payload.get("vmid", "")).strip()
        if phase == "" or vmid == "":
            self._send_json(400, {"status": "missing_phase_or_vmid"})
            return

        if phase not in self.config.allowed_phases:
            self._send_json(
                202,
                {"status": "ignored", "phase": phase, "reason": "phase_not_allowed"},
            )
            return

        event = {
            "phase": phase,
            "vmid": vmid,
            "node": str(payload.get("node", "")).strip(),
            "node_fqdn": str(payload.get("node_fqdn", "")).strip(),
            "source": str(payload.get("source", "proxmox-hookscript")).strip(),
            "received_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "payload": payload,
        }
        self.runner.submit(event)
        self._send_json(
            202,
            {"status": "queued", "phase": phase, "vmid": vmid},
        )

    def _is_authorized(self) -> bool:
        auth_header = self.headers.get("Authorization", "")
        header_token = ""
        if auth_header.startswith("Bearer "):
            header_token = auth_header.removeprefix("Bearer ").strip()
        if header_token == "":
            header_token = self.headers.get("X-Webhook-Token", "").strip()
        return header_token != "" and hmac.compare_digest(header_token, self.config.token)

    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        stream=sys.stdout,
    )


def main() -> int:
    configure_logging()
    config = load_config()
    runner = EventRunner(config)
    runner.start()

    server = EventWebhookServer((config.bind, config.port), ProxmoxEventWebhookHandler, config, runner)
    if config.tls_certfile is not None:
        if config.tls_keyfile is None:
            raise RuntimeError("PFA_TLS_KEYFILE must be set when PFA_TLS_CERTFILE is used.")
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=str(config.tls_certfile), keyfile=str(config.tls_keyfile))
        server.socket = context.wrap_socket(server.socket, server_side=True)
        logging.info("Serving HTTPS webhook on %s:%s%s", config.bind, config.port, config.webhook_path)
    else:
        logging.info("Serving HTTP webhook on %s:%s%s", config.bind, config.port, config.webhook_path)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Stopping Proxmox event webhook.")
    finally:
        server.server_close()
        runner.stop()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1) from exc
