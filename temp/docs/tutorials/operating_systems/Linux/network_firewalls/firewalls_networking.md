# Linux Firewalls and Networking Commands

## Overview

Linux provides various tools for managing network configurations and firewalls. This document covers basic and commonly used commands for network management and firewall configuration.

## Networking Commands

### `ifconfig`

Displays or configures network interfaces.

```sh
ifconfig [interface]
```

#### Example

```sh
ifconfig eth0
# Displays the configuration for the 'eth0' network interface
```

#### Example

```sh
ifconfig eth0 up
# Brings up the 'eth0' network interface
```

### `ip`

A more modern tool for managing network interfaces, routes, and addresses.

#### Show Network Interfaces

```sh
ip addr show
```

#### Example

```sh
ip addr show
# Displays detailed information about all network interfaces
```

#### Assign an IP Address

```sh
sudo ip addr add <IP_address>/<netmask> dev <interface>
```

#### Example

```sh
sudo ip addr add 192.168.1.100/24 dev eth0
# Assigns the IP address 192.168.1.100 to the 'eth0' interface
```

#### Bring Up/Down an Interface

```sh
sudo ip link set <interface> up
sudo ip link set <interface> down
```

#### Example

```sh
sudo ip link set eth0 up
# Brings up the 'eth0' interface
```

### `netstat`

Displays network connections, routing tables, interface statistics, and more.

```sh
netstat [options]
```

#### Example

```sh
netstat -tuln
# Displays listening TCP and UDP ports with numeric addresses
```

### `ss`

A utility to investigate sockets and network connections, a modern replacement for `netstat`.

```sh
ss [options]
```

#### Example

```sh
ss -tuln
# Displays listening TCP and UDP sockets with numeric addresses
```

### `ping`

Sends ICMP ECHO_REQUEST packets to network hosts.

```sh
ping [options] <host>
```

#### Example

```sh
ping google.com
# Pings 'google.com' to check network connectivity
```

### `traceroute`

Displays the route packets take to a network host.

```sh
traceroute <host>
```

#### Example

```sh
traceroute google.com
# Shows the path taken to reach 'google.com'
```

### `nslookup`

Queries DNS to obtain domain name or IP address mapping.

```sh
nslookup <domain>
```

#### Example

```sh
nslookup google.com
# Queries DNS for information about 'google.com'
```

### `route`

Displays or modifies the IP routing table.

```sh
route [options]
```

#### Example

```sh
route -n
# Displays the IP routing table with numeric addresses
```

### `ip route`

Displays and manages the routing table.

```sh
ip route [options]
```

#### Example

```sh
ip route show
# Displays the current routing table
```

## Firewall Commands

### `iptables`

Configures and manages firewall rules.

#### List Rules

```sh
sudo iptables -L
```

#### Example

```sh
sudo iptables -L
# Lists all current firewall rules
```

#### Add Rule

```sh
sudo iptables -A <chain> -p <protocol> --dport <port> -j <target>
```

#### Example

```sh
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
# Allows incoming TCP connections on port 22 (SSH)
```

#### Delete Rule

```sh
sudo iptables -D <chain> -p <protocol> --dport <port> -j <target>
```

#### Example

```sh
sudo iptables -D INPUT -p tcp --dport 22 -j ACCEPT
# Deletes the rule allowing incoming TCP connections on port 22
```

### `ufw`

Uncomplicated Firewall (UFW) is a user-friendly front-end for managing firewall rules.

#### Enable UFW

```sh
sudo ufw enable
```

#### Example

```sh
sudo ufw enable
# Enables the UFW firewall
```

#### Allow a Port

```sh
sudo ufw allow <port>
```

#### Example

```sh
sudo ufw allow 22
# Allows incoming connections on port 22 (SSH)
```

#### Deny a Port

```sh
sudo ufw deny <port>
```

#### Example

```sh
sudo ufw deny 80
# Denies incoming connections on port 80 (HTTP)
```

#### Check UFW Status

```sh
sudo ufw status
```

#### Example

```sh
sudo ufw status
# Displays the current status and rules of UFW
```

## Summary

Linux provides a robust set of tools for managing network configurations and firewall rules. Mastering these commands helps in monitoring and securing network traffic, configuring network interfaces, and troubleshooting network issues. For more detailed information on each command, refer to the [Linux manual pages](https://man7.org/linux/man-pages/).