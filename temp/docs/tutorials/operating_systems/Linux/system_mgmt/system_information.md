# Linux System Information Commands

## Overview

Linux provides a range of commands to gather information about the system's hardware, software, and overall status. These commands are useful for monitoring and troubleshooting system performance and configuration. This document covers basic and commonly used system information commands.

## System Information

### `uname`

Displays system information.

```sh
uname
```

#### Example

```sh
uname
# Output: Displays the kernel name (e.g., Linux)
```

### `uname -a`

Displays all available system information, including kernel version and system architecture.

```sh
uname -a
```

#### Example

```sh
uname -a
# Output: Linux hostname 5.4.0-42-generic #46-Ubuntu SMP Fri Sep 25 13:00:00 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
```

### `hostname`

Displays or sets the system's hostname.

```sh
hostname
```

#### Example

```sh
hostname
# Output: Displays the current hostname of the system
```

### `hostnamectl`

Displays or changes the system's hostname and other system information.

```sh
hostnamectl
```

#### Example

```sh
hostnamectl
# Output: Provides detailed information about the system's hostname, operating system, and hardware
```

## Hardware Information

### `lscpu`

Displays detailed information about the CPU architecture.

```sh
lscpu
```

#### Example

```sh
lscpu
# Output: Displays CPU architecture information including number of CPUs, model name, and more
```

### `lsblk`

Lists information about all available block devices.

```sh
lsblk
```

#### Example

```sh
lsblk
# Output: Lists block devices and their mount points, sizes, and types
```

### `lspci`

Lists all PCI devices on the system.

```sh
lspci
```

#### Example

```sh
lspci
# Output: Lists PCI devices such as graphics cards, network adapters, etc.
```

### `lsusb`

Lists all USB devices connected to the system.

```sh
lsusb
```

#### Example

```sh
lsusb
# Output: Lists USB devices connected to the system along with their vendor and product IDs
```

### `dmidecode`

Displays information about the system's hardware as described in the BIOS.

```sh
sudo dmidecode
```

#### Example

```sh
sudo dmidecode
# Output: Provides detailed information about hardware components, such as memory, CPU, and motherboard
```

## Memory and Disk Usage

### `free`

Displays information about system memory usage.

```sh
free
```

#### Example

```sh
free
# Output: Displays memory usage, including total, used, and free memory
```

### `df`

Displays information about disk space usage for mounted filesystems.

```sh
df
```

#### Example

```sh
df
# Output: Displays disk space usage for each mounted filesystem
```

### `du`

Displays disk usage of files and directories.

```sh
du <directory>
```

#### Example

```sh
du /home/user
# Output: Displays disk usage for the '/home/user' directory
```

### `top`

Displays real-time system performance and process information.

```sh
top
```

#### Example

```sh
top
# Output: Displays a real-time, interactive view of system processes and resource usage
# Use 'q' to quit
```

### `htop`

An enhanced version of `top` with a more user-friendly interface.

```sh
htop
```

#### Example

```sh
htop
# Output: Provides an interactive, user-friendly view of system processes and resource usage
# Use 'q' to quit
```

## System Uptime

### `uptime`

Displays how long the system has been running, along with the number of users and load average.

```sh
uptime
```

#### Example

```sh
uptime
# Output: Displays system uptime, number of users, and load averages
```

## Summary

Linux provides a variety of commands to gather detailed system information, from hardware details and disk usage to real-time performance metrics. Understanding these commands helps in monitoring and maintaining system health. For more detailed information on each command, refer to the [Linux manual pages](https://man7.org/linux/man-pages/).