# Linux Process Management Commands

## Overview

Linux provides several commands for managing processes, which include starting, stopping, and monitoring processes. These commands are essential for controlling and managing the execution of programs and tasks on a Linux system. This document covers basic and commonly used process management commands.

## Display Processes

### `ps`

Displays information about active processes.

```sh
ps
```

#### Example

```sh
ps
# Output: Lists processes running in the current shell
```

### `ps aux`

Displays a detailed list of all running processes, including those from other users.

```sh
ps aux
```

#### Example

```sh
ps aux
# Output: Detailed list of all running processes
```

### `top`

Displays a dynamic, real-time view of system processes.

```sh
top
```

#### Example

```sh
top
# Output: Real-time display of active processes and system resource usage
# Use 'q' to quit
```

### `htop`

An interactive process viewer similar to `top`, but with a more user-friendly interface.

```sh
htop
```

#### Example

```sh
htop
# Output: Interactive display of processes with user-friendly interface
# Use 'q' to quit
```

### `pgrep`

Searches for processes by name or other attributes.

```sh
pgrep <name>
```

#### Example

```sh
pgrep ssh
# Output: Lists process IDs of processes matching 'ssh'
```

## Manage Processes

### `kill`

Sends a signal to a process, commonly used to terminate it.

```sh
kill <PID>
```

#### Example

```sh
kill 1234
# Sends the default SIGTERM signal to the process with PID 1234
```

### `kill -9`

Forcibly terminates a process.

```sh
kill -9 <PID>
```

#### Example

```sh
kill -9 1234
# Sends the SIGKILL signal to the process with PID 1234, forcibly terminating it
```

### `pkill`

Sends a signal to processes by name.

```sh
pkill <name>
```

#### Example

```sh
pkill firefox
# Sends the default SIGTERM signal to all processes named 'firefox'
```

### `killall`

Sends a signal to all processes with a specific name.

```sh
killall <name>
```

#### Example

```sh
killall firefox
# Sends the default SIGTERM signal to all processes named 'firefox'
```

## Process Prioritization

### `nice`

Runs a command with a specified priority level.

```sh
nice -n <priority> <command>
```

#### Example

```sh
nice -n 10 gzip largefile.txt
# Runs 'gzip largefile.txt' with a priority level of 10
```

### `renice`

Changes the priority of a running process.

```sh
renice <priority> -p <PID>
```

#### Example

```sh
renice 5 -p 1234
# Changes the priority of the process with PID 1234 to 5
```

## Background and Foreground Jobs

### `&`

Runs a command in the background.

```sh
command &
```

#### Example

```sh
sleep 60 &
# Runs the 'sleep 60' command in the background
```

### `jobs`

Lists all background jobs.

```sh
jobs
```

#### Example

```sh
jobs
# Output: Lists background jobs and their job numbers
```

### `fg`

Brings a background job to the foreground.

```sh
fg %<job_number>
```

#### Example

```sh
fg %1
# Brings the background job with job number 1 to the foreground
```

### `bg`

Resumes a suspended job in the background.

```sh
bg %<job_number>
```

#### Example

```sh
bg %1
# Resumes the suspended job with job number 1 in the background
```

## Summary

Linux offers a variety of commands for managing processes, from displaying and monitoring to controlling and prioritizing. Understanding these commands helps effectively manage and troubleshoot processes on a Linux system. For more detailed information on each command, refer to the [Linux manual pages](https://man7.org/linux/man-pages/).