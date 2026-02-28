# 📖 ARKHAM - Agente CTF de Providence

*«No puedo evitar sentir que hay algo más antiguo que los propios Dioses, algo que reposa en los espacios intermedios que la mente humana no puede comprender.»*
— H.P. Lovecraft

---

## 🐙 Descripción

**ARKHAM** (Automated Reconnaissance & Knowledge HARvesting Agent of Providence) es un asistente de IA diseñado para ayudarte a resolver desafíos CTF de plataformas como HackTheBox, TryHackMe, picoCTF y laboratorios personalizados.

El agente:
- 📡 **Enumera** automáticamente objetivos
- 🔍 **Identifica** vulnerabilidades
- 🛠️ **Ejecuta** herramientas de explotación
- 📝 **Documenta** todo el proceso
- 🚩 **Registra** flags encontradas
- 🧠 **Aprende** de cada desafío

---

## 🎮 Uso Básico

### Modo Interactivo

```bash
python3 arkam.py --interactive
```

### Flujo de Trabajo

```
┌─────────────────────────────────────────────────────────────────────┐
│                     FLUJO DE TRABAJO ARKHAM                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   1. INICIAR          2. EXPLORAR         3. EXPLOTAR             │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐        │
│   │ start lab    │ ─► │ run nmap     │ ─► │ run sqlmap   │        │
│   │ --web        │    │ run gobuster │    │ run hydra    │        │
│   │ --ip x.x.x.x │    │ note hallazgos│    │ flag {xxx}   │        │
│   └──────────────┘    └──────────────┘    └──────────────┘        │
│          │                   │                   │                   │
│          └───────────────────┼───────────────────┘                   │
│                              ▼                                      │
│                     4. DOCUMENTAR                                   │
│                     ┌──────────────┐                                │
│                     │ report       │                                │
│                     │ save         │                                │
│                     └──────────────┘                                │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Comandos

### Iniciar Desafío

```bash
arkham> start [nombre] [opciones]

# Ejemplos:
arkham> start "EzpzLab" --web --ip 10.10.10.5
arkham> start "Buffer Overflow" --pwn --difficulty hard
arkham> start "Crypto Challenge" --crypto
```

**Opciones:**
| Opción | Descripción |
|--------|-------------|
| `--web`, `--pwn`, `--rev`, `--crypto`, `--osint`, `--misc` | Categoría |
| `--easy`, `--medium`, `--hard`, `--insane` | Dificultad |
| `--ip x.x.x.x` | IP del objetivo |
| `--port 22` | Puerto específico |
| `--desc "descripción"` | Descripción del desafío |

---

### Ejecutar Comandos

```bash
arkham> run [comando]

# Ejemplos:
arkham> run nmap -sVC -p- 10.10.10.5
arkham> run gobuster dir -u http://10.10.10.5 -w /usr/share/wordlists/dirb/common.txt
arkham> run nikto -h 10.10.10.5
arkham> run sqlmap -u "http://10.10.10.5/login.php?q=1" --batch
arkham> run "echo 'SGVsbG8=' | base64 -d"
```

**Puedes ejecutar cualquier comando de shell.** El agente lo registrará automáticamente.

---

### Registrar Flags

```bash
arkham> flag [flag]

# Ejemplos:
arkham> flag HTB{3z_pz_1n_c0mm4nds}
arkham> flag THM{l0v3cR4ft_4g41n}
arkham> flag picoCTF{pwn_4g41n_4nd_4g41n}
```

---

### Notas y Hallazgos

```bash
arkham> note [texto]

# Ejemplos:
arkham> note Found admin panel at /admin
arkham> note SQL error: MySQL syntax near ''
arkham> note User: admin, Password: password123
arkham> note Binary has NX disabled - buffer overflow possible!
```

---

### Sugerencias

```bash
arkham> suggest
```

Te da sugerencias basadas en la categoría del desafío:

| Categoría | Sugerencias |
|-----------|-------------|
| **Web** | gobuster, nikto, SQLMap, parámetros |
| **Pwn** | checksec, ghidra, rop gadgets |
| **Rev** | strings, ghidra, binwalk |
| **Crypto** | base64, ROT13, hash identification |
| **OSINT** | username search, email leak check |
| **Misc** | nmap, revisar archivos |

---

### Reportes

```bash
arkham> report
```

Genera un reporte completo:

```
╔══════════════════════════════════════════════════════════════════╗
║                    CTF CHALLENGE REPORT                         ║
╠══════════════════════════════════════════════════════════════════╣
║ Name:        SQL Injection Lab                                 ║
║ Category:    web                                               ║
║ Difficulty:  medium                                            ║
║ IP:          10.10.10.5                                       ║
╚══════════════════════════════════════════════════════════════════╝

🚩 FLAGS FOUND:
  - HTB{sql_1nj3ct10n_m4st3r}

🛠️ TOOLS USED:
  - nmap
  - gobuster
  - sqlmap

📋 NOTES:
  - Found admin panel at /admin
  - SQL error reveals MySQL version
```

---

### Gestión de Sesiones

```bash
arkham> save                    # Guardar sesión actual
arkham> save my-lab-01         # Guardar con nombre específico
arkham> load my-lab-01         # Cargar sesión previa
arkham> sessions               # Listar sesiones guardadas
arkham> stats                 # Ver estadísticas
```

---

## 🛠️ Herramientas Integradas

El agente puede ejecutar cualquier herramienta. Las más comunes:

| Herramienta | Uso | Ejemplo |
|-------------|-----|---------|
| **nmap** | Escaneo de puertos | `run nmap -sVC -p- 10.10.10.5` |
| **gobuster** | Directorios | `run gobuster dir -u http://target` |
| **nikto** | Vulnerabilidades web | `run nikto -h target` |
| **sqlmap** | SQL Injection | `run sqlmap -u url --batch` |
| **hydra** | Fuerza bruta | `run hydra -l user -P pass.txt target ssh` |
| **john** | Crack hashes | `run john hash.txt --wordlist=rockyou.txt` |
| **steghide** | Esteganografía | `run steghide extract -sf image.png` |
| **ghidra** | Reverse engineering | (usar manualmente) |
| **curl** | Solicitudes HTTP | `run curl -X POST url -d data` |

---

## 🔧 Configuración

### Variables de Entorno

```bash
# API Keys (opcional)
export HTB_API_KEY="tu_api_key_de_htb"
export THM_API_KEY="tu_api_key_de_thm"

# Alias para facilitar
alias arkam='python3 /ruta/a/arkam.py --interactive'
```

### Estructura de Archivos

```
~/.arkham/
├── sessions/           # Sesiones guardadas
│   └── lab-01.json
├── logs/               # Logs del agente
│   └── arkam.log
├── nmap/               # Escaneos nmap
└── history.json        # Historial completo
```

---

## 📖 Ejemplos Completos

### Ejemplo 1: Web Challenge

```bash
arkham> start "SQL Lab" --web --ip 10.10.10.5
✅ Started: SQL Lab

arkham> run nmap -sVC -p80,443 10.10.10.5
[output...]

arkham> run gobuster dir -u http://10.10.10.5 -w /usr/share/wordlists/dirb/common.txt
[output...]

arkham> note Found login form at /admin/login.php

arkham> run "curl -d 'username=admin&password=admin' http://10.10.10.5/login.php"
[output...]

arkham> suggest
→ Try sqlmap: sqlmap -u "http://10.10.10.5/login.php" --batch

arkham> run sqlmap -u "http://10.10.10.5/login.php" --batch --level=2
[output...]

arkham> flag HTB{sql_1nj3ct10n_r0cks!}
✅ Flag recorded!

arkham> report
[genera reporte]

arkham> save sql-lab-01
💾 Session saved!
```

### Ejemplo 2: Crypto Challenge

```bash
arkham> start "Crypto 101" --crypto
✅ Started: Crypto 101

arkham> note Given string: "U0VDUkV7MXNfM3J0M3JfZnJvbV9wcm92aWRlbmNl}"

arkham> run "echo 'U0VDUkV7MXNfM3J0M3JfZnJvbV9wcm92aWRlbmNl}' | base64 -d"
SECR{1s_3rt3r_fr0m_pr0v1d3nc3}

arkham> flag SECR{1s_3rt3r_fr0m_pr0v1d3nc3}
✅ Flag recorded!
```

### Ejemplo 3: Buffer Overflow

```bash
arkham> start "BoF 1" --pwn --ip 10.10.10.5 --port 9999
✅ Started: BoF 1

arkham> run "nc 10.10.10.5 9999"
[output: "Welcome to the vulnerable service"]

arkham> run checksec --file=vuln_binary
[output: NX disabled, canary found...]

arkham> note Binary at /home/user/vuln

arkham> suggest
→ Run: python3 -c "print('A'*100)"
→ Try pattern create and locate offset

arkham> run "python3 /usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 200"
[output: pattern...]

arkham> flag HTB{buff3r_0v3rfl0w_m4st3r}
```

---

## 🎭 Categorías de Desafío

| Categoría | Descripción | Herramientas Clave |
|-----------|-------------|-------------------|
| **Web** | Inyección SQL, XSS, RCE, LFI | nmap, gobuster, nikto, sqlmap |
| **Pwn** | Buffer overflow, ROP | checksec, ghidra, pwntools |
| **Rev** | Reverse engineering | strings, ghidra, radare2 |
| **Crypto** | Criptografía clásica | cyberchef,hashcat |
| **OSINT** | Información pública | sherlock, theHarvester |
| **Misc** | Varios | Depende del desafío |

---

## 🧠 Consejos

1. **Siempre documenta** - El agente guardará todo
2. **Usa `note`** - Registrar hallazgos importantes
3. **Consulta `suggest`** - Si no sabes qué hacer
4. **Guarda sesiones** - Para continuar después
5. **Revisa `report`** - Antes de entregar

---

## ⚠️ Advertencia

> *«Las verdades que encontramos pueden seranas, y es mejor que permanezcan ocultas.»*
> — H.P. Lovecraft

Este agente es para **fines educativos** en entornos CTF autorizados. No lo uses en sistemas sin permiso.

---

## 🚀 Comandos Rápidos

```bash
# Iniciar
python3 arkam.py -i

# Lista de comandos en modo interactivo:
start <nombre>     # Iniciar desafío
run <cmd>         # Ejecutar comando
flag <flag>       # Registrar flag
note <texto>      # Agregar nota
suggest           # Ver sugerencias
report            # Generar reporte
save              # Guardar sesión
load <nombre>     # Cargar sesión
stats             # Ver estadísticas
quit              # Salir
```

---

*«El hombre más viejo es siempre el más joven, pues lo que llamamos tiempo no es sino la ignorancia de la eternidad.»*
— H.P. Lovecraft, "La llave de plata"
