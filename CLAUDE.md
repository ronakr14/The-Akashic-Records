# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is an Obsidian vault for personal knowledge management (The-Akashic-Records). The vault contains markdown notes and is configured with Obsidian plugins.

## Common Commands

Since this is an Obsidian vault, there are no build, lint, or test commands. The primary interaction is through the Obsidian app or by editing markdown files directly.

- To view notes: Open the vault in Obsidian.
- To edit notes: Use any text editor or the Obsidian editor.
- To search notes: Use Obsidian's search or `grep` on the markdown files.

## Vault Structure

- The vault root contains markdown files (currently only README.md).
- The `.obsidian` directory contains Obsidian configuration and plugins (do not modify unless configuring Obsidian).

## Guidelines

- When adding new notes, use markdown format and place them in the vault root or in subfolders as desired.
- Follow existing note naming conventions (none established yet).
- For plugin-specific configurations, refer to the Obsidian documentation.

## Note Organization Rules

- New notes without Claude assistance: place in `00_Inbox`.
- New notes with Claude assistance: place in `00_Claude_Inbox` if unstructured or unconfirmed.
- Keep tags minimal and folder structure sustainable.
- Do not create new folders unless extremely important.

## Development Notes

This repository does not contain source code for software development. It is a knowledge base. If you intend to develop software, please create a separate project.

However, if you are working on the vault itself (e.g., adding automation via Obsidian plugins), then:

- Plugin development typically involves JavaScript/TypeScript and HTML/CSS.
- Plugin files are located in `.obsidian/plugins/<plugin-id>/`.
- To test a plugin, reload Obsidian or use the Obsidian developer tools.