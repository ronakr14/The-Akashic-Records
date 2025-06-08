# Linux Network Configuration and Monitoring Commands

## Overview

Linux provides a variety of commands for configuring and monitoring network interfaces and connections. These commands are essential for managing network settings, diagnosing network issues, and ensuring proper connectivity. This document covers basic and commonly used network configuration and monitoring commands.

## Network Configuration

### `ip`

A powerful tool for configuring network interfaces, routing, and tunnels.

#### Display Network Interfaces

```sh
ip addr
```

##### Example

```sh
ip addr
# Output: Lists all network interfaces with their IP addresses and other details
```

#### Display Routing Table

```sh
ip route
```

##### Example

```sh
ip route
# Output: Displays the current routing table
```

#### Add an IP Address

```sh
sudo ip addr add <ip_address>/<subnet> dev <interface>
```

##### Example

```sh
sudo ip addr add 192.168.1.100/24 dev eth0
# Adds the IP address 192.168.1.100 with subnet 24 to the interface 'eth0'
```

#### Delete an IP Address

```sh
sudo ip addr del <ip_address>/<subnet> dev <interface>
```

##### Example

```sh
sudo ip addr del 192.168.1.100/24 dev eth0
# Removes the IP address 192.168.1.100 from the interface 'eth0'
```

### `ifconfig`

Displays and configures network interfaces. Note: `ifconfig` is deprecated in favor of `ip`.

```sh
ifconfig
```

#### Example

```sh
ifconfig
# Output: Displays network interface configuration
```

### `nmcli`

Command-line interface for NetworkManager, used to manage network connections.

#### List Network Connections

```sh
nmcli connection show
```

##### Example

```sh
nmcli connection show
# Output: Lists all network connections managed by NetworkManager
```

#### Connect to a Network

```sh
nmcli connection up <connection_name>
```

##### Example

```sh
nmcli connection up my-wifi
# Connects to the network named 'my-wifi'
```

#### Disconnect from a Network

```sh
nmcli connection down <connection_name>
```

##### Example

```sh
nmcli connection down my-wifi
# Disconnects from the network named 'my-wifi'
```

## Network Monitoring

### `ping`

Sends ICMP ECHO_REQUEST packets to a network host to check connectivity.

```sh
ping <hostname_or_ip>
```

#### Example

```sh
ping google.com
# Output: Sends packets to 'google.com' to check connectivity
```

### `traceroute`

Displays the route packets take to a network host.

```sh
traceroute <hostname_or_ip>
```

#### Example

```sh
traceroute google.com
# Output: Shows the route taken by packets to reach 'google.com'
```

### `netstat`

Displays network connections, routing tables, and interface statistics. Note: `netstat` is deprecated in favor of `ss`.

#### Display All Connections

```sh
netstat -a
```

##### Example

```sh
netstat -a
# Output: Lists all network connections and listening ports
```

### `ss`

Displays detailed information about network sockets.

#### Display All Connections

```sh
ss -a
```

##### Example

```sh
ss -a
# Output: Lists all network connections and listening ports
```

### `tcpdump`

Captures and analyzes network packets.

```sh
sudo tcpdump
```

#### Example

```sh
sudo tcpdump -i eth0
# Captures packets on the 'eth0' interface
```

### `iftop`

Displays bandwidth usage on network interfaces.

```sh
sudo iftop
```

#### Example

```sh
sudo iftop
# Output: Displays real-time bandwidth usage on all network interfaces
# Use 'q' to quit
```

### `nmap`

Network scanning tool used to discover hosts and services on a network.

```sh
nmap <hostname_or_ip>
```

#### Example

```sh
nmap 192.168.1.1
# Scans the IP address 192.168.1.1 for open ports and services
```

## Summary

Linux provides a comprehensive set of commands for configuring and monitoring network interfaces and connections. These commands are essential for managing network settings, diagnosing issues, and ensuring network connectivity. For more detailed information on each command, refer to the [Linux manual pages](https://man7.org/linux/man-pages/).