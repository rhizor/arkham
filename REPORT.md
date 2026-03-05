# ARKHAM - Repository Analysis Report

## Repository Overview

- **Name:** ARKHAM (Automated Reconnaissance & Knowledge HARvesting Agent of Providence)
- **Language:** Python 3.8+
- **Type:** CLI Tool for CTF (Capture The Flag) challenge management
- **License:** MIT

## Repository Structure

```
arkham/
├── main.py          # Main entry point (~27KB)
├── arkham.py        # Core module (~27KB)
├── README.md        # Documentation
├── README_ORIGINAL.md
├── USAGE.md         # Detailed usage guide
└── (no tests directory)
```

## How the Application Runs

```bash
python3 main.py --interactive    # Interactive mode
python3 main.py <command>        # Command mode
python3 arkham.py --interactive   # Alternative entry
```

## Dependencies

- `requests` - HTTP library (main dependency)
- `colorama` - Terminal colors (optional)
- `readline` - Interactive input (optional, built-in)

## Architecture

- **Pattern:** Object-oriented with dataclasses
- **Components:**
  - `Challenge` dataclass - represents CTF challenges
  - `Command` dataclass - represents executed commands
  - `CTFTools` class - collection of CTF tool wrappers (nmap, gobuster, etc.)
  - Interactive CLI with command parsing

## Existing Tests

**None.** No test directory or test files exist.

## Recommended Testing Strategy

Since this is a CTF CLI tool:

1. **Unit tests** for:
   - Command parsing
   - Data validation (Challenge dataclass)
   - Flag format validation
   - File path handling

2. **Smoke tests** for:
   - CLI invocation
   - Help command
   - Basic session management

3. **Mock external calls** - nmap, gobuster, etc. cannot run in container

## Potential Reliability Issues

- **External tool dependencies:** nmap, hydra, etc. must be installed on host
- **File system:** Uses `~/.arkham/` for sessions and logs
- **No input sanitization** in some commands
- **Network calls:** Uses requests library for potential API calls

## Environment Variables

None required. Uses default paths in home directory.

## External Dependencies (for full functionality)

- nmap
- gobuster
- nikto
- sqlmap
- hydra
- john
- steghide

## Risks for Docker Testing

- Cannot run actual nmap/penetration tools inside container
- Tests must be mocked or limited to unit tests only
- Interactive CLI may require tty

## Testing Approach for Docker

Focus on **unit tests with mocked external tools**. The Docker container will validate:
- Python syntax and imports
- Dataclass validation logic
- Command parsing
- Flag regex validation
- Session file operations (mocked)
