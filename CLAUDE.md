# CLAUDE.md - AI Assistant Guide for Vibe

This document provides guidance for AI assistants working with the Vibe codebase.

## Project Overview

**Vibe** is an early-stage project currently in the initialization phase. The repository contains media assets but no source code implementation yet.

### Current State
- **Status**: Pre-development/Setup phase
- **Source Code**: None present
- **Build System**: Not configured
- **Testing**: Not set up

## Repository Structure

```
/vibe/
├── README.md                      # Project documentation (minimal)
├── CLAUDE.md                      # This file - AI assistant guide
├── .git/                          # Git version control
│
└── Media Assets:
    ├── studio_portrait_*.png      # Portrait images (864x1184)
    ├── Generated Image *.jpeg     # Generated artwork (1408x768)
    └── *.webm                     # Video content
```

## Key Files

| File | Purpose |
|------|---------|
| `README.md` | Project documentation with OpenClaw installation instructions |
| `CLAUDE.md` | AI assistant guidance (this file) |
| `*.png`, `*.jpeg`, `*.webm` | Media assets (sample/test content) |

## Dependencies

### OpenClaw
The only documented external dependency. Install with:
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

## Development Workflows

### Git Branching
- **Main branch**: `main` (via `origin/main`)
- **Feature branches**: Follow pattern `claude/<description>-<id>` for AI-assisted work
- Branches should be created from `main` and merged via pull requests

### Git Commands
```bash
# Check current status
git status

# Create and push a new branch
git checkout -b feature/your-feature
git push -u origin feature/your-feature

# Standard commit workflow
git add <files>
git commit -m "Descriptive message"
git push
```

## Code Conventions

Since no source code exists yet, conventions should be established when development begins. Recommended practices:

### When Adding Code
1. Choose appropriate language/framework for project goals
2. Set up package manager (npm, pip, cargo, etc.)
3. Configure linting and formatting tools
4. Add `.gitignore` for language-specific ignores
5. Create test framework setup

### File Organization
- Keep media assets in a dedicated `/assets` or `/media` directory
- Source code should go in `/src` directory
- Tests should mirror source structure in `/tests` or `/__tests__`

## Important Notes for AI Assistants

### What Exists
- Media assets (images, video) - treat as sample/test content
- Basic README with installation instructions
- Active Git repository with multiple branches

### What Does NOT Exist
- Source code implementation
- Build configuration (package.json, Makefile, etc.)
- Test suite or testing framework
- Code style configuration (.eslintrc, .prettierrc, etc.)
- CI/CD pipelines
- `.gitignore` file
- LICENSE file
- Contributing guidelines

### When Making Changes
1. Do not modify media files unless explicitly requested
2. Any new code should include appropriate tests
3. Update README.md when adding features
4. Follow semantic commit messages
5. Create PRs for non-trivial changes

## Quick Reference

### Repository Info
- **Owner**: kimsanguine
- **Platform**: GitHub (via local proxy)
- **License**: Not specified

### Common Tasks

**Add a new file:**
```bash
# Create and stage the file
git add <filename>
git commit -m "Add <description>"
git push -u origin <branch-name>
```

**Check repository status:**
```bash
git status
git log --oneline -5
```

## Future Development

When implementing features, consider:
1. Define project scope and purpose
2. Choose technology stack
3. Set up build system
4. Configure development environment
5. Add testing infrastructure
6. Document API/usage
7. Add license file

---

*Last updated: 2026-02-01*
