# 🐙 ARKHAM

<p align="center">
  <i>«No puedo evitar sentir que hay algo más antiguo que los propios Dioses»</i>
  <br>— H.P. Lovecraft
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
</p>

## 📖 Descripción

**ARKHAM** (Automated Reconnaissance & Knowledge HARvesting Agent of Providence) es un asistente de IA para resolver desafíos CTF. Soporta HackTheBox, TryHackMe, picoCTF y laboratorios personalizados.

## ⚡ Características

- 🎯 **Multi-plataforma**: HTB, THM, picoCTF, custom
- 📡 **Enumeración**: Nmap, Gobuster, Nikto, SQLMap
- 🛠️ **Explotación**: Hydra, John, Steghide, herramientas de análisis
- 📝 **Documentación**: Guarda comandos, notas, flags
- 🚩 **Flag Tracking**: Registra todas las flags encontradas
- 📊 **Reporting**: Genera reportes detallados
- 💾 **Sesiones**: Guarda y reanuda desafíos
- 🧠 **Sugerencias**: Guía basada en categoría

## 📦 Instalación

### Requisitos Previos

- Python 3.8+
- Git

### Instalación con Entorno Virtual (Recomendado)

```bash
# Clonar repositorio
git clone https://github.com/rhizor/arkham.git
cd arkham

# Crear entorno virtual (recomendado)
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate  # Linux/macOS
# O en Windows:
# venv\Scripts\activate

# Instalar dependencias
pip install requests

# (Opcional) Instalar dependencias extras
pip install colorama readline
```

### Instalación Rápida (Sin entorno virtual)

```bash
git clone https://github.com/rhizor/arkham.git
cd arkham
pip install requests
```

> ⚠️ **Nota**: Se recomienda usar un entorno virtual (`venv`) para evitar conflictos con otras dependencias del sistema.

## 🚀 Uso

```bash
# Modo interactivo
python3 arkham.py --interactive
```

### Comandos Principales

```bash
start "Lab Name" --web --ip 10.10.10.5    # Iniciar desafío
run nmap -sVC 10.10.10.5                   # Ejecutar comando
flag HTB{flag_here}                        # Registrar flag
note Found admin panel at /admin            # Agregar nota
suggest                                     # Ver sugerencias
report                                      # Generar reporte
save                                        # Guardar sesión
stats                                       # Ver estadísticas
```

## 📁 Estructura

```
~/.arkham/
├── sessions/      # Sesiones guardadas
├── logs/         # Logs
└── history.json  # Historial
```

## 📖 Documentación

Ver [USAGE.md](USAGE.md) para guía completa.

## ⚠️ Uso Ético

> *«Las verdades que encontramos pueden seranas»*

Este herramienta es para **fines educativos** en entornos CTF autorizados.

---

*«El hombre más viejo es siempre el más joven»*
— H.P. Lovecraft
