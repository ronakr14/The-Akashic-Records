# Linux SSH Commands

## Overview

SSH (Secure Shell) is a protocol used to securely access and manage remote systems over a network. The SSH suite of commands provides a variety of tools for connecting to, configuring, and managing remote systems. This document covers basic and commonly used SSH commands.

## Basic SSH Commands

### `ssh`

Used to securely connect to a remote machine.

```sh
ssh <user>@<hostname_or_ip>
```

#### Example

```sh
ssh john@192.168.1.100
# Connects to the remote host 192.168.1.100 as user 'john'
```

### `ssh-keygen`

Generates a new SSH key pair.

```sh
ssh-keygen
```

#### Example

```sh
ssh-keygen
# Prompts to generate a new SSH key pair; saves the private key and public key in the default location (~/.ssh/)
```

### `ssh-copy-id`

Copies your SSH public key to a remote host's authorized keys.

```sh
ssh-copy-id <user>@<hostname_or_ip>
```

#### Example

```sh
ssh-copy-id john@192.168.1.100
# Copies the public key to the remote host to enable passwordless login for user 'john'
```

### `scp`

Securely copies files between hosts over SSH.

```sh
scp <source> <user>@<hostname_or_ip>:<destination>
```

#### Example

```sh
scp localfile.txt john@192.168.1.100:/home/john/
# Copies 'localfile.txt' from the local machine to the '/home/john/' directory on the remote host
```

### `sftp`

Secure File Transfer Protocol for transferring files over SSH.

```sh
sftp <user>@<hostname_or_ip>
```

#### Example

```sh
sftp john@192.168.1.100
# Opens an SFTP session with the remote host
```

### `ssh-add`

Adds SSH private keys to the SSH authentication agent.

```sh
ssh-add <key_file>
```

#### Example

```sh
ssh-add ~/.ssh/id_rsa
# Adds the private key 'id_rsa' to the SSH agent for authentication
```

### `ssh-agent`

Manages SSH keys and handles authentication for SSH sessions.

```sh
eval $(ssh-agent)
```

#### Example

```sh
eval $(ssh-agent)
# Starts the SSH agent and sets environment variables for the current session
```

## Advanced SSH Commands

### `ssh -i`

Specifies a private key file to use for authentication.

```sh
ssh -i <private_key_file> <user>@<hostname_or_ip>
```

#### Example

```sh
ssh -i ~/.ssh/id_rsa john@192.168.1.100
# Connects to the remote host using the specified private key file
```

### `ssh -p`

Specifies a port number for the SSH connection.

```sh
ssh -p <port_number> <user>@<hostname_or_ip>
```

#### Example

```sh
ssh -p 2222 john@192.168.1.100
# Connects to the remote host on port 2222
```

### `ssh -L`

Creates a local port forwarding.

```sh
ssh -L <local_port>:<remote_host>:<remote_port> <user>@<hostname_or_ip>
```

#### Example

```sh
ssh -L 8080:localhost:80 john@192.168.1.100
# Forwards local port 8080 to port 80 on the remote host through SSH
```

### `ssh -R`

Creates a remote port forwarding.

```sh
ssh -R <remote_port>:<local_host>:<local_port> <user>@<hostname_or_ip>
```

#### Example

```sh
ssh -R 9090:localhost:80 john@192.168.1.100
# Forwards remote port 9090 to port 80 on the local machine through SSH
```

### `ssh -C`

Enables compression for the SSH connection.

```sh
ssh -C <user>@<hostname_or_ip>
```

#### Example

```sh
ssh -C john@192.168.1.100
# Connects to the remote host with compression enabled
```

## Summary

The SSH suite of commands provides powerful tools for securely managing and transferring data between systems. By mastering these commands, you can effectively perform remote administration and file transfers while maintaining secure connections. For more detailed information on each command, refer to the [Linux manual pages](https://man7.org/linux/man-pages/).