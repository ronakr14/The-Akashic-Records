# Linux `vim` Commands

## Overview

`vim` (Vi IMproved) is a powerful text editor in Linux with extensive features for editing text files. This document covers essential `vim` commands and operations to help you get started.

## Basic Usage

### Opening a File

To open a file with `vim`, use the following command:

```sh
vim <file_name>
```

#### Example

```sh
vim example.txt
# Opens 'example.txt' in vim
```

## `vim` Modes

`vim` operates in different modes, primarily:

- **Normal Mode**: For navigation and command execution (default mode when `vim` starts).
- **Insert Mode**: For text insertion.
- **Visual Mode**: For selecting text.
- **Command-Line Mode**: For executing commands (entered by pressing `:` in Normal Mode).

## Normal Mode Commands

### Navigation

- **Move Cursor**: `h` (left), `j` (down), `k` (up), `l` (right)
- **Move by Words**: `w` (forward), `b` (backward)
- **Move to Line Start/End**: `0` (start), `$` (end)
- **Move to Specific Line**: `:n` (where `n` is the line number)

#### Example

```sh
# Move cursor to the 10th line
:10
```

### Deleting Text

- **Delete Character**: `x`
- **Delete Line**: `dd`
- **Delete Word**: `dw`
- **Delete to End of Line**: `d$`

#### Example

```sh
# Delete the current line
dd
```

### Copying and Pasting

- **Copy Line**: `yy`
- **Paste**: `p`

#### Example

```sh
# Copy the current line and paste it below
yy
p
```

### Undo and Redo

- **Undo**: `u`
- **Redo**: `Ctrl + r`

#### Example

```sh
# Undo the last change
u
```

## Insert Mode Commands

### Entering Insert Mode

- **Insert Before Cursor**: `i`
- **Insert After Cursor**: `a`
- **Append After Line**: `A`
- **Insert New Line**: `o` (below), `O` (above)

#### Example

```sh
# Enter Insert Mode and type text
iHello, World!
```

### Exiting Insert Mode

- **Return to Normal Mode**: `Esc`

#### Example

```sh
# Press Esc to return to Normal Mode
```

## Visual Mode Commands

### Selecting Text

- **Enter Visual Mode**: `v`
- **Select Whole Line**: `V`
- **Select Block**: `Ctrl + v`

#### Example

```sh
# Enter Visual Mode and select text
v
```

### Copying and Pasting in Visual Mode

- **Copy**: `y` (after selection)
- **Paste**: `p` (after selection)

#### Example

```sh
# Select text and copy it
v
y
```

## Command-Line Mode Commands

### Saving and Quitting

- **Save and Quit**: `:wq` or `:x`
- **Save**: `:w`
- **Quit Without Saving**: `:q!`

#### Example

```sh
# Save changes and exit
:wq
```

### Searching and Replacing

- **Search**: `/search_term`
- **Replace**: `:s/old/new/g` (for current line), `:%s/old/new/g` (for entire file)

#### Example

```sh
# Search for 'example' in the file
/example

# Replace 'foo' with 'bar' in the entire file
:%s/foo/bar/g
```

## Miscellaneous Commands

### Show Line Numbers

To show line numbers, use:

```sh
:set number
```

#### Example

```sh
# Enable line numbers
:set number
```

### Split Windows

- **Horizontal Split**: `:split <file>`
- **Vertical Split**: `:vsplit <file>`
- **Navigate Between Splits**: `Ctrl + w`, then use `h`, `j`, `k`, `l`

#### Example

```sh
# Split window horizontally and open 'file1.txt'
:split file1.txt
```

## Summary

`vim` is a versatile text editor with powerful features for efficient text editing. Understanding and mastering the different modes, commands, and shortcuts will enhance your productivity. For more detailed information and advanced features, refer to the [Vim Documentation](https://vimhelp.org/).