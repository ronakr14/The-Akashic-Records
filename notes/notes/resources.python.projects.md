---
id: gwxo901hh4940plkf0weh55
title: Projects
tags: [python, project]
desc: ''
updated: 1752424888892
created: 1752424876075
---

## Goal

Create a CLI tool called `mini-automator` that:

- Takes a config YAML file
- Executes file backups, folder cleanups, or fetches weather data via an API
- Logs results in a file
- Has modular tasks as plug-ins

## Features

- CLI Interface (`argparse` or `typer`)
- File I/O and system operations (`os`, `shutil`)
- API consumption (`requests`)
- Error logging
- Task-based class structure

## Stretch Goals

- Add unit tests
- Convert into a pip-installable package
- Add GUI with `tkinter` or `textual`