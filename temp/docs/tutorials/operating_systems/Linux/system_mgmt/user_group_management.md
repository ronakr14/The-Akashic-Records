# Linux User and Group Management Commands

## Overview

Linux provides a set of commands for managing users and groups. These commands allow you to create, modify, delete, and view users and groups on the system. This document covers basic and commonly used user and group management commands.

## User Management

### `adduser` or `useradd`

Creates a new user.

```sh
sudo adduser <username>
# or
sudo useradd <username>
```

#### Example

```sh
sudo adduser john
# Creates a new user named 'john'
```

### `usermod`

Modifies an existing user's account details.

```sh
sudo usermod <options> <username>
```

#### Example

```sh
sudo usermod -aG sudo john
# Adds the user 'john' to the 'sudo' group
```

### `deluser` or `userdel`

Deletes a user account.

```sh
sudo deluser <username>
# or
sudo userdel <username>
```

#### Example

```sh
sudo deluser john
# Deletes the user 'john' but keeps the home directory
```

### `passwd`

Changes a user's password.

```sh
sudo passwd <username>
```

#### Example

```sh
sudo passwd john
# Prompts to change the password for the user 'john'
```

### `id`

Displays information about a user.

```sh
id <username>
```

#### Example

```sh
id john
# Output: Displays user ID (UID), group ID (GID), and group memberships for 'john'
```

### `whoami`

Displays the username of the current user.

```sh
whoami
```

#### Example

```sh
whoami
# Output: Displays the current logged-in username
```

## Group Management

### `addgroup` or `groupadd`

Creates a new group.

```sh
sudo addgroup <groupname>
# or
sudo groupadd <groupname>
```

#### Example

```sh
sudo addgroup developers
# Creates a new group named 'developers'
```

### `delgroup` or `groupdel`

Deletes a group.

```sh
sudo delgroup <groupname>
# or
sudo groupdel <groupname>
```

#### Example

```sh
sudo delgroup developers
# Deletes the group named 'developers'
```

### `gpasswd`

Modifies group memberships and settings.

```sh
sudo gpasswd -a <username> <groupname>
```

#### Example

```sh
sudo gpasswd -a john developers
# Adds the user 'john' to the 'developers' group
```

### `groups`

Displays the groups that a user belongs to.

```sh
groups <username>
```

#### Example

```sh
groups john
# Output: Displays the groups that the user 'john' belongs to
```

## View Users and Groups

### `getent`

Displays entries from databases configured in `/etc/nsswitch.conf`, including users and groups.

```sh
getent passwd
```

#### Example

```sh
getent passwd
# Output: Displays all user accounts in the system
```

### `cat /etc/passwd`

Displays the contents of the user account database file.

```sh
cat /etc/passwd
```

#### Example

```sh
cat /etc/passwd
# Output: Displays user account information including username, UID, GID, home directory, and shell
```

### `cat /etc/group`

Displays the contents of the group database file.

```sh
cat /etc/group
```

#### Example

```sh
cat /etc/group
# Output: Displays group information including group name, GID, and group members
```

## Summary

Linux offers a range of commands for managing users and groups, including creating, modifying, and deleting accounts and groups. Understanding these commands helps in effectively managing user and group permissions on a Linux system. For more detailed information on each command, refer to the [Linux manual pages](https://man7.org/linux/man-pages/).