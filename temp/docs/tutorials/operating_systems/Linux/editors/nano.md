# Linux `nano` Commands

## Overview

`nano` is a simple and user-friendly text editor for the command line. It is often used for editing configuration files and scripting. This document provides a guide to common `nano` commands and operations.

## Basic Commands

### Open a File

To open a file in `nano`, simply specify the file name.

```sh
nano <file_name>
```

#### Example

```sh
nano example.txt
# Opens 'example.txt' in the nano editor
```

### Save Changes

To save changes while editing, press `Ctrl + O` (Write Out), then press `Enter` to confirm the file name.

#### Example

1. Edit the file.
2. Press `Ctrl + O`.
3. Press `Enter`.

### Exit `nano`

To exit `nano`, press `Ctrl + X`. If you have unsaved changes, `nano` will prompt you to save them.

#### Example

1. Press `Ctrl + X`.
2. If prompted to save changes, press `Y` (Yes) or `N` (No).

### Cut Text

To cut text, use `Ctrl + K`. This will cut the current line or selected text.

#### Example

1. Place the cursor on the line you want to cut.
2. Press `Ctrl + K`.
3. The line will be removed and stored in the clipboard.

### Paste Text

To paste text that was cut or copied, use `Ctrl + U`.

#### Example

1. Move the cursor to the location where you want to paste.
2. Press `Ctrl + U`.

### Copy Text

To copy text, use `Ctrl + ^` to set the mark, move the cursor to select the text, and then press `Ctrl + K` to cut. Paste it using `Ctrl + U`.

#### Example

1. Press `Ctrl + ^` to set the mark.
2. Move the cursor to select the text.
3. Press `Ctrl + K` to cut the selected text.
4. Move the cursor to the paste location.
5. Press `Ctrl + U` to paste.

### Search for Text

To search for text within the file, press `Ctrl + W` (Where Is), then enter the search term and press `Enter`.

#### Example

1. Press `Ctrl + W`.
2. Enter the search term.
3. Press `Enter`.

### Replace Text

To replace text, press `Ctrl + \` (Replace), then enter the search term, press `Enter`, enter the replacement term, and press `Enter`.

#### Example

1. Press `Ctrl + \`.
2. Enter the search term.
3. Press `Enter`.
4. Enter the replacement term.
5. Press `Enter`.

### Go to Line Number

To move the cursor to a specific line number, press `Ctrl + _` (Underscore), enter the line number, and press `Enter`.

#### Example

1. Press `Ctrl + _`.
2. Enter the line number (e.g., `10`).
3. Press `Enter`.

### Show Line Numbers

To enable line numbers, press `Ctrl + C` to view the current line number, or check the status bar for line numbers.

#### Example

1. Press `Ctrl + C` to view the current line number.
2. Check the status bar at the bottom of the editor.

## Summary

`nano` is a powerful yet easy-to-use text editor that allows you to efficiently edit files from the command line. Understanding these basic commands will help you navigate and modify files effectively. For more detailed information, refer to the `nano` man pages by running `man nano` in the terminal.