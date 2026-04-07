#!/usr/bin/env perl
use strict;
use warnings;

use HTTP::Tiny;
use JSON::PP qw(encode_json);
use Sys::Hostname qw(hostname);

my $DEFAULT_CONFIG_FILE = '/etc/default/proxmox-freeipa-hook';
my $config_file = $ENV{PFA_HOOK_CONFIG} // $DEFAULT_CONFIG_FILE;

sub read_config {
    my ($path) = @_;
    my %config = ();

    return %config if !-r $path;

    open my $fh, '<', $path or return %config;
    while (my $line = <$fh>) {
        chomp $line;
        $line =~ s/^\s+//;
        $line =~ s/\s+$//;
        next if $line eq '';
        next if $line =~ /^#/;
        next if $line !~ /^([A-Za-z_][A-Za-z0-9_]*)=(.*)$/;

        my ($key, $value) = ($1, $2);
        $value =~ s/^['"]//;
        $value =~ s/['"]$//;
        $config{$key} = $value;
    }

    close $fh;
    return %config;
}

sub parse_bool {
    my ($value, $default) = @_;
    return $default if !defined $value || $value eq '';
    return $value =~ /^(1|true|yes|on)$/i ? 1 : 0;
}

sub normalize_csv {
    my ($value, $default) = @_;
    my @values = defined $value && $value ne '' ? split /,/, $value : split /,/, $default;
    @values = map {
        my $item = $_;
        $item =~ s/^\s+//;
        $item =~ s/\s+$//;
        $item;
    } @values;
    @values = grep { $_ ne '' } @values;
    return @values;
}

sub finish_with_error {
    my ($message, $strict) = @_;
    warn "$message\n";
    exit($strict ? 1 : 0);
}

my %config = read_config($config_file);
my $strict = parse_bool($config{PFA_STRICT}, 0);

my ($vmid, $phase) = @ARGV;
finish_with_error('Usage: proxmox-vm-hook.pl <vmid> <phase>', $strict) if !defined $vmid || !defined $phase;

my %allowed_phases = map { $_ => 1 } normalize_csv($config{PFA_ALLOWED_PHASES}, 'post-start,post-migrate');
exit 0 if !$allowed_phases{$phase};

my $webhook_url = $config{PFA_WEBHOOK_URL} // '';
my $webhook_token = $config{PFA_WEBHOOK_TOKEN} // '';
finish_with_error("Missing PFA_WEBHOOK_URL in $config_file", $strict) if $webhook_url eq '';
finish_with_error("Missing PFA_WEBHOOK_TOKEN in $config_file", $strict) if $webhook_token eq '';

my $timeout = $config{PFA_TIMEOUT_SECONDS} // 10;
my $verify_tls = parse_bool($config{PFA_VERIFY_TLS}, 1);

my $node_short = `hostname -s 2>/dev/null`;
chomp $node_short;
$node_short ||= hostname();

my $node_fqdn = `hostname -f 2>/dev/null`;
chomp $node_fqdn;
$node_fqdn ||= $node_short;

my $payload = {
    vmid => "$vmid",
    phase => $phase,
    node => $node_short,
    node_fqdn => $node_fqdn,
    source => 'proxmox-hookscript',
    sent_at => time(),
};

my $http = HTTP::Tiny->new(
    timeout => $timeout,
    verify_SSL => $verify_tls,
    default_headers => {
        Authorization => "Bearer $webhook_token",
        'Content-Type' => 'application/json',
    },
);

my $response = $http->post(
    $webhook_url,
    {
        content => encode_json($payload),
    },
);

if (!$response->{success}) {
    my $status = $response->{status} // 'unknown';
    my $reason = $response->{reason} // 'unknown';
    finish_with_error("Webhook request failed with status $status ($reason)", $strict);
}

exit 0;
