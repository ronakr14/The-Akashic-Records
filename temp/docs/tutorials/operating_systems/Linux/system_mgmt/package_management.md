# Linux Package Management Commands

## Overview

Linux distributions use different package managers to handle software installation, updates, and removal. This document covers basic and commonly used package management commands for various package managers.

## Debian-Based Systems (e.g., Ubuntu)

### `apt`

The Advanced Package Tool (APT) is used for managing packages in Debian-based distributions.

#### Update Package List

```sh
sudo apt update
```

##### Example

```sh
sudo apt update
# Updates the package list from repositories
```

#### Upgrade Installed Packages

```sh
sudo apt upgrade
```

##### Example

```sh
sudo apt upgrade
# Upgrades all installed packages to their latest versions
```

#### Install a Package

```sh
sudo apt install <package_name>
```

##### Example

```sh
sudo apt install vim
# Installs the 'vim' text editor
```

#### Remove a Package

```sh
sudo apt remove <package_name>
```

##### Example

```sh
sudo apt remove vim
# Removes the 'vim' text editor
```

#### Search for a Package

```sh
apt search <package_name>
```

##### Example

```sh
apt search vim
# Searches for packages related to 'vim'
```

#### Show Package Details

```sh
apt show <package_name>
```

##### Example

```sh
apt show vim
# Displays detailed information about the 'vim' package
```

## Red Hat-Based Systems (e.g., CentOS, Fedora)

### `yum`

The Yellowdog Updater, Modified (YUM) is used for managing packages in older Red Hat-based distributions.

#### Update Package List and System

```sh
sudo yum update
```

##### Example

```sh
sudo yum update
# Updates the package list and upgrades all installed packages
```

#### Install a Package

```sh
sudo yum install <package_name>
```

##### Example

```sh
sudo yum install vim
# Installs the 'vim' text editor
```

#### Remove a Package

```sh
sudo yum remove <package_name>
```

##### Example

```sh
sudo yum remove vim
# Removes the 'vim' text editor
```

#### Search for a Package

```sh
yum search <package_name>
```

##### Example

```sh
yum search vim
# Searches for packages related to 'vim'
```

#### Show Package Details

```sh
yum info <package_name>
```

##### Example

```sh
yum info vim
# Displays detailed information about the 'vim' package
```

### `dnf`

The Dandified YUM (DNF) is used for managing packages in newer Red Hat-based distributions.

#### Update Package List and System

```sh
sudo dnf update
```

##### Example

```sh
sudo dnf update
# Updates the package list and upgrades all installed packages
```

#### Install a Package

```sh
sudo dnf install <package_name>
```

##### Example

```sh
sudo dnf install vim
# Installs the 'vim' text editor
```

#### Remove a Package

```sh
sudo dnf remove <package_name>
```

##### Example

```sh
sudo dnf remove vim
# Removes the 'vim' text editor
```

#### Search for a Package

```sh
dnf search <package_name>
```

##### Example

```sh
dnf search vim
# Searches for packages related to 'vim'
```

#### Show Package Details

```sh
dnf info <package_name>
```

##### Example

```sh
dnf info vim
# Displays detailed information about the 'vim' package
```

## SUSE-Based Systems

### `zypper`

The command-line interface for managing packages in SUSE-based distributions.

#### Update Package List and System

```sh
sudo zypper refresh
sudo zypper update
```

##### Example

```sh
sudo zypper refresh
sudo zypper update
# Refreshes package list and upgrades all installed packages
```

#### Install a Package

```sh
sudo zypper install <package_name>
```

##### Example

```sh
sudo zypper install vim
# Installs the 'vim' text editor
```

#### Remove a Package

```sh
sudo zypper remove <package_name>
```

##### Example

```sh
sudo zypper remove vim
# Removes the 'vim' text editor
```

#### Search for a Package

```sh
zypper search <package_name>
```

##### Example

```sh
zypper search vim
# Searches for packages related to 'vim'
```

#### Show Package Details

```sh
zypper info <package_name>
```

##### Example

```sh
zypper info vim
# Displays detailed information about the 'vim' package
```

## General Package Management

### `rpm`

The RPM Package Manager is used for managing packages in RPM-based distributions.

#### Install a Package

```sh
sudo rpm -i <package_file.rpm>
```

##### Example

```sh
sudo rpm -i vim-8.2.0-1.x86_64.rpm
# Installs the 'vim' package from the RPM file
```

#### Remove a Package

```sh
sudo rpm -e <package_name>
```

##### Example

```sh
sudo rpm -e vim
# Removes the 'vim' package
```

#### Query Package Information

```sh
rpm -q <package_name>
```

##### Example

```sh
rpm -q vim
# Queries information about the 'vim' package
```

## Summary

Linux offers various package management tools depending on the distribution used. Understanding these commands helps in efficiently managing software installations, updates, and removals. For more detailed information on each command, refer to the [Linux manual pages](https://man7.org/linux/man-pages/).