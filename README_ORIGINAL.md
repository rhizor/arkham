# 🤖 CTF Agent

AI-powered assistant for solving CTF challenges. Supports HackTheBox, TryHackMe, picoCTF, and custom labs.

## 🎯 Features

- **Multi-platform**: HackTheBox, TryHackMe, picoCTF, custom
- **Automatic Enumeration**: Nmap, Gobuster, Nikto, SQLMap
- **Challenge Categories**: Web, Pwn, Rev, Crypto, OSINT, Misc
- **Session Management**: Save/resume challenges
- **Flag Tracking**: Record all flags found
- **Reporting**: Generate detailed reports
- **Learning**: Built-in hints and suggestions
- **Tool Integration**: Nmap, Nikto, Gobuster, SQLMap, Hydra, John, Steghide

## 📦 Installation

```bash
git clone https://github.com/rhizor/ctf-agent.git
cd ctf-agent
pip install requests
```

## 🚀 Usage

### Interactive Mode

```bash
python3 ctf_agent.py --interactive
```

### Commands

```
ctf-agent> start lab01 --category web --difficulty medium --ip 10.10.10.5
ctf-agent> run nmap -sVC -p- 10.10.10.5
ctf-agent> run gobuster dir -u http://10.10.10.5 -w /usr/share/wordlists/dirb/common.txt
ctf-agent> note Found login page at /admin
ctf-agent> suggest
ctf-agent> flag HTB{f4k3_fl4g}
ctf-agent> report
ctf-agent> save
ctf-agent> stats
```

### Single Command Mode

```bash
# Start challenge
python3 ctf_agent.py start "SQL Injection Lab" --category web --ip 10.10.10.10

# Run command
python3 ctf_agent.py run "nmap -sV 10.10.10.10"

# Add flag
python3 ctf_agent.py flag "HTB{flag_here}"

# View stats
python3 ctf_agent.py stats
```

## 🔧 Configuration

### Environment Variables

| Variable | Description |
|----------|-------------|
| `HTB_API_KEY` | HackTheBox API key |
| `THM_API_KEY` | TryHackMe API key |

### Available Tools

| Tool | Purpose |
|------|---------|
| `nmap` | Port scanning |
| `nikto` | Web vulnerability scan |
| `gobuster` | Directory busting |
| `sqlmap` | SQL injection |
| `hydra` | Password brute forcing |
| `john` | Hash cracking |
| `steghide` | Steganography |
| `ghidra` | Reverse engineering |
| `checksec` | Binary protections |

## 📁 Files

```
~/.ctf_agent/
├── sessions/          # Saved challenge sessions
├── logs/             # Agent logs
├── nmap/             # Nmap scans
└── history.json      # Complete history
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│              CTF Agent Core                  │
├─────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Platform  │  │ Challenge│  │ Session  │  │
│  │ Manager   │  │ Tracker  │  │ Manager  │  │
│  └──────────┘  └──────────┘  └──────────┘  │
│                                              │
│  ┌──────────────────────────────────────┐   │
│  │         Tool Integration              │   │
│  │  nmap | nikto | gobuster | sqlmap   │   │
│  │  hydra | john | steghide | ghidra   │   │
│  └──────────────────────────────────────┘   │
│                                              │
│  ┌──────────────────────────────────────┐   │
│  │         Challenge Solvers             │   │
│  │  Web | Pwn | Rev | Crypto | OSINT   │   │
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

## 📊 Examples

### Solving a Web Challenge

```bash
ctf-agent> start xss-lab --category web --ip 10.10.10.20
ctf-agent> run nmap -sVC -p80,443 10.10.10.20
ctf-agent> run gobuster dir -u http://10.10.10.20 -w /usr/share/wordlists/dirb/common.txt
ctf-agent> note Found parameter 'q' in search
ctf-agent> run "curl 'http://10.10.10.20/search?q=<script>alert(1)</script>'"
ctf-agent> flag HTB{xss_pwn3d}
ctf-agent> report
```

### Solving a Crypto Challenge

```bash
ctf-agent> start crypto1 --category crypto
ctf-agent> note Given: "SGVsbG8gV29ybGQ=" - looks like base64
ctf-agent> run "echo 'SGVsbG8gV29ybGQ=' | base64 -d"
ctf-agent> flag HTB{base64_easy}
```

## 🔐 Security Notes

- Always use in authorized CTF environments
- Don't run commands you don't understand
- Review before executing exploit code
- Keep your API keys secure

## 📝 License

MIT License

## 🤝 Contributing

Pull requests welcome! Add new tools, solvers, and platform integrations.
