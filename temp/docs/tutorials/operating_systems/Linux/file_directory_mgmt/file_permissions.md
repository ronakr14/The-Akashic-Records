# Linux File Permissions Commands

## Overview

File permissions in Linux control the access to files and directories. Permissions determine who can read, write, or execute files. This document covers basic commands for viewing and modifying file permissions.

## Viewing Permissions

### `ls -l`

Lists files and directories with detailed information, including permissions.

```sh
ls -l
```

#### Example

```sh
ls -l
# Output: Lists files and directories with permissions, owner, group, size, and modification date
# Example output:
# -rwxr-xr-- 1 user group 1234 Aug  3 10:00 example.txt
```

## Understanding File Permissions

File permissions are represented by a string of 10 characters:

```
-rwxr-xr--
```

- **File Type**: `-` (regular file), `d` (directory), `l` (symlink)
- **Owner Permissions**: `rwx` (read, write, execute)
- **Group Permissions**: `r-x` (read, execute)
- **Others Permissions**: `r--` (read)

## Changing Permissions

### `chmod`

Changes the permissions of a file or directory.

```sh
chmod [options] <permissions> <file>
```

#### Example

```sh
chmod 755 example.txt
# Sets the permissions of 'example.txt' to rwxr-xr-x (owner: read, write, execute; group and others: read, execute)
```

#### Numeric Mode

- **7**: rwx (read, write, execute)
- **6**: rw- (read, write)
- **5**: r-x (read, execute)
- **4**: r-- (read)
- **3**: wx- (write, execute)
- **2**: w-- (write)
- **1**: --x (execute)
- **0**: --- (no permissions)

#### Example

```sh
chmod 644 example.txt
# Sets the permissions of 'example.txt' to rw-r--r-- (owner: read, write; group and others: read)
```

#### Symbolic Mode

- **u**: user (owner)
- **g**: group
- **o**: others
- **a**: all

Use `+` to add permissions, `-` to remove, and `=` to set exact permissions.

#### Example

```sh
chmod u+x example.txt
# Adds execute permission for the owner
```

```sh
chmod go-w example.txt
# Removes write permission for group and others
```

### `chown`

Changes the owner and/or group of a file or directory.

```sh
sudo chown [owner][:group] <file>
```

#### Example

```sh
sudo chown john:admins example.txt
# Changes the owner of 'example.txt' to 'john' and the group to 'admins'
```

### `chgrp`

Changes the group ownership of a file or directory.

```sh
sudo chgrp <group> <file>
```

#### Example

```sh
sudo chgrp admins example.txt
# Changes the group ownership of 'example.txt' to 'admins'
```

## Special Permissions

### Setuid (Set User ID)

When set on an executable file, the process runs with the permissions of the file's owner.

```sh
chmod u+s <file>
```

#### Example

```sh
chmod u+s /usr/bin/someprogram
# Sets the setuid bit on 'someprogram'
```

### Setgid (Set Group ID)

When set on a directory, new files and directories inherit the group of the directory.

```sh
chmod g+s <directory>
```

#### Example

```sh
chmod g+s /var/shared
# Sets the setgid bit on the '/var/shared' directory
```

### Sticky Bit

When set on a directory, only the file owner can delete files within that directory.

```sh
chmod +t <directory>
```

#### Example

```sh
chmod +t /tmp
# Sets the sticky bit on the '/tmp' directory
```

## Summary

Understanding and managing file permissions is crucial for maintaining security and proper access control in Linux. These commands allow you to view and modify permissions, ownership, and special attributes of files and directories. For more detailed information on each command, refer to the [Linux manual pages](https://man7.org/linux/man-pages/).