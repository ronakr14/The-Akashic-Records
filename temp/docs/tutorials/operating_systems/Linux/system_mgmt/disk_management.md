# Linux Disk Management Commands

## Overview

Linux provides various commands for managing disks and filesystems. These commands allow you to view disk usage, partition disks, format filesystems, and more. This document covers basic and commonly used disk management commands.

## Disk Usage and Information

### `df`

Displays information about disk space usage on filesystems.

```sh
df [options] [file...]
```

#### Example

```sh
df -h
# Output: Displays disk space usage in human-readable format (e.g., GB, MB)
```

### `du`

Displays disk usage for files and directories.

```sh
du [options] [directory...]
```

#### Example

```sh
du -sh /home/user
# Output: Shows the total disk usage of the directory '/home/user' in human-readable format
```

### `lsblk`

Lists information about all available block devices.

```sh
lsblk [options]
```

#### Example

```sh
lsblk
# Output: Displays a list of block devices, including partitions and their mount points
```

### `fdisk`

Partition table manipulator for creating, deleting, and managing disk partitions.

```sh
sudo fdisk /dev/sdX
```

#### Example

```sh
sudo fdisk /dev/sda
# Opens fdisk to manage partitions on the /dev/sda disk
```

#### Common `fdisk` Commands

- **List partitions**: `p`
- **Create a new partition**: `n`
- **Delete a partition**: `d`
- **Write changes**: `w`
- **Quit without saving**: `q`

### `parted`

A tool for managing disk partitions.

```sh
sudo parted /dev/sdX
```

#### Example

```sh
sudo parted /dev/sda
# Opens parted to manage partitions on the /dev/sda disk
```

#### Common `parted` Commands

- **Print partition table**: `print`
- **Create a new partition**: `mkpart`
- **Delete a partition**: `rm`
- **Resize a partition**: `resizepart`
- **Quit**: `quit`

## Filesystem Management

### `mkfs`

Creates a filesystem on a disk or partition.

```sh
sudo mkfs -t <filesystem_type> /dev/sdXn
```

#### Example

```sh
sudo mkfs -t ext4 /dev/sda1
# Creates an ext4 filesystem on the /dev/sda1 partition
```

### `fsck`

Checks and repairs a filesystem.

```sh
sudo fsck [options] /dev/sdXn
```

#### Example

```sh
sudo fsck /dev/sda1
# Checks and repairs the filesystem on /dev/sda1
```

### `mount`

Mounts a filesystem to a directory.

```sh
sudo mount [options] /dev/sdXn <mount_point>
```

#### Example

```sh
sudo mount /dev/sda1 /mnt
# Mounts the filesystem on /dev/sda1 to the /mnt directory
```

### `umount`

Unmounts a filesystem from a directory.

```sh
sudo umount <mount_point>
```

#### Example

```sh
sudo umount /mnt
# Unmounts the filesystem from the /mnt directory
```

### `lsblk` (again)

Lists block devices and their mount points.

```sh
lsblk -f
```

#### Example

```sh
lsblk -f
# Output: Displays filesystem type and labels along with block device information
```

## Disk Usage Analysis

### `ncdu`

A disk usage analyzer with a text-based user interface.

```sh
ncdu [directory]
```

#### Example

```sh
ncdu /home/user
# Opens ncdu to analyze disk usage in the '/home/user' directory
```

## Summary

Linux offers a comprehensive set of commands for managing disks and filesystems. Understanding these commands helps in monitoring disk usage, partitioning disks, and maintaining filesystems effectively. For more detailed information on each command, refer to the [Linux manual pages](https://man7.org/linux/man-pages/).