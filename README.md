# 🐳 Docklite - Einfacher Homelab Deployer

Docklite ist ein benutzerfreundliches Python-Tool, mit dem du **fertige Homelab-Anwendungen** kinderleicht nach Vorlagen deployen kannst. Perfekt für Einsteiger, die schnell ihr eigenes Homelab aufbauen möchten - **ohne Docker-Kenntnisse**!

🏠 **16 vorkonfigurierte Homelab-Apps:** Media Server, Smart Home, Dashboards, Passwort Manager, Git Server und mehr!

## ✨ Features

- 🎯 **Interaktives Menü** - Benutzerfreundliches Menüsystem für Einsteiger
- 📦 **Einfache Templates** - Vorkonfigurierte Vorlagen für beliebte Container
- 🚀 **Schnelles Deployment** - Container mit einem Befehl starten
- 🔧 **Interaktive Konfiguration** - Schritt-für-Schritt Einrichtung
- 📝 **Keine Docker-Kenntnisse nötig** - Ideal für Anfänger
- 🛠️ **Container-Verwaltung** - Stoppen, Starten und Entfernen über das Menü
- 🎨 **Erweiterbar** - Eigene Templates einfach hinzufügen

## 📋 Voraussetzungen

- Python 3.7 oder höher
- Docker installiert und lauffähig
- Linux, macOS oder Windows (mit WSL2)

### Docker installieren

Falls Docker noch nicht installiert ist:

- **Ubuntu/Debian:**
  ```bash
  curl -fsSL https://get.docker.com -o get-docker.sh
  sudo sh get-docker.sh
  sudo usermod -aG docker $USER
  ```

- **macOS:** Docker Desktop von https://www.docker.com/products/docker-desktop herunterladen

- **Windows:** Docker Desktop für Windows von https://www.docker.com/products/docker-desktop herunterladen

## 🚀 Installation

1. Repository klonen:
   ```bash
   git clone https://github.com/matdan1987/Docklite.git
   cd Docklite
   ```

2. Python-Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```

3. Skript ausführbar machen (Linux/macOS):
   ```bash
   chmod +x docklite.py
   ```

## 📖 Verwendung

### ⭐ Interaktives Menü (EMPFOHLEN für Anfänger!)

Einfach das Skript ohne Parameter starten:

```bash
python docklite.py
```

Du bekommst ein übersichtliches Menü mit folgenden Optionen:
- 📦 Container deployen (starten)
- 📋 Alle verfügbaren Templates anzeigen
- ℹ️ Template-Informationen anzeigen
- 🐳 Laufende Container anzeigen
- 🛑 Container stoppen
- 🗑️ Container entfernen

**Das ist der einfachste Weg!** Perfekt für Einsteiger - keine Befehle merken, alles über das Menü!

### Kommandozeilen-Modus (für Fortgeschrittene)

Falls du lieber direkt Befehle eingibst:

#### Verfügbare Templates anzeigen

```bash
python docklite.py list
```

#### Template-Informationen anzeigen

```bash
python docklite.py info nginx
```

#### Container deployen

```bash
python docklite.py deploy nginx
```

#### Mit benutzerdefinierten Variablen deployen

```bash
python docklite.py deploy nginx --var port=8080 --var html_dir=/path/to/html
```

## 📦 Verfügbare Homelab-Anwendungen

### 🎬 Media & Unterhaltung
- **jellyfin** - Media Server (Netflix-Alternative)
- **photoprism** - KI-basierte Fotoverwaltung

### 🏠 Smart Home & Netzwerk
- **homeassistant** - Smart Home Plattform
- **pihole** - Netzwerkweiter Werbeblocker
- **nginx-proxy-manager** - Reverse Proxy mit SSL

### 📊 Dashboards & Monitoring
- **homepage** - Modernes Homelab Dashboard
- **heimdall** - Application Dashboard
- **uptime-kuma** - Service Monitoring
- **portainer** - Docker GUI Management

### 🔐 Produktivität & Sicherheit
- **vaultwarden** - Passwort Manager (Bitwarden)
- **paperless-ngx** - Dokumenten-Management
- **nextcloud** - Private Cloud Storage
- **syncthing** - File-Synchronisation

### 💻 Development & Tools
- **gitea** - Self-hosted Git Server
- **wordpress** - CMS / Blog
- **nginx** - Webserver

## 💡 Beispiele

### Beispiel 1: Jellyfin Media Server

```bash
python docklite.py deploy jellyfin
```

Deine eigene Netflix-Alternative! Lege deine Filme und Serien in das Media-Verzeichnis und streame sie überall.

### Beispiel 2: Vaultwarden Passwort Manager

```bash
python docklite.py deploy vaultwarden
```

Sichere all deine Passwörter selbst-gehostet! Kompatibel mit Bitwarden Apps und Browser-Extensions.

### Beispiel 3: Homepage Dashboard

```bash
python docklite.py deploy homepage
```

Erstelle ein schönes Dashboard für all deine Homelab-Services!

### Beispiel 4: Portainer (Docker GUI)

```bash
python docklite.py deploy portainer
```

Nach dem Start öffne `http://localhost:9000` und erstelle einen Admin-Account.

### Beispiel 4: WordPress mit MariaDB

Zuerst MariaDB starten:
```bash
python docklite.py deploy mariadb
```

Dann WordPress deployen:
```bash
python docklite.py deploy wordpress
```

Bei der WordPress-Konfiguration die MariaDB-Zugangsdaten eingeben.

## 🛠️ Eigene Templates erstellen

Du kannst ganz einfach eigene Templates erstellen!

1. Erstelle eine neue `.yaml` Datei im `templates/` Verzeichnis
2. Verwende folgende Struktur:

```yaml
name: mein-container
description: Beschreibung des Containers
image: docker-image:tag
detached: true
restart: unless-stopped

ports:
  - "${port}:80"

volumes:
  - "${data_dir}:/app/data"

environment:
  MY_VAR: "${my_value}"

variables:
  port:
    description: "Port Beschreibung"
    default: "8080"
  my_value:
    description: "Meine Variable"
    default: "wert"
  data_dir:
    description: "Daten Verzeichnis"
    default: "./data"

info: |
  Zusätzliche Informationen die nach dem Start angezeigt werden.
```

### Template-Optionen

- **name**: Container-Name
- **description**: Kurzbeschreibung
- **image**: Docker Image
- **detached**: Im Hintergrund laufen lassen (true/false)
- **restart**: Restart-Policy (unless-stopped, always, on-failure, no)
- **ports**: Port-Mappings (Format: "host:container")
- **volumes**: Volume-Mappings
- **environment**: Umgebungsvariablen
- **network**: Docker Network
- **command**: Überschreibe den Standard-Command
- **options**: Zusätzliche Docker-Optionen
- **variables**: Konfigurierbare Variablen
- **info**: Info-Text nach dem Deployment

## 🔍 Tipps & Tricks

### Container-Status prüfen

```bash
docker ps
```

Zeigt alle laufenden Container an.

### Container stoppen

```bash
docker stop <container-name>
```

### Container entfernen

```bash
docker rm <container-name>
```

### Container-Logs anzeigen

```bash
docker logs <container-name>
```

### Alle Container anzeigen (auch gestoppte)

```bash
docker ps -a
```

## 🆘 Häufige Probleme

### "Docker ist nicht verfügbar"

- Stelle sicher, dass Docker installiert und gestartet ist
- Prüfe mit `docker --version`
- Auf Linux: Füge deinen Benutzer zur docker-Gruppe hinzu: `sudo usermod -aG docker $USER`

### "Permission denied" beim Zugriff auf Volumes

- Stelle sicher, dass die angegebenen Verzeichnisse existieren
- Prüfe die Berechtigungen der Verzeichnisse
- Verwende absolute Pfade statt relativer Pfade

### "Port already in use"

- Ein anderer Container oder Dienst nutzt bereits den Port
- Wähle einen anderen Port mit `--var port=XXXX`
- Prüfe mit `docker ps`, welche Container laufen

### Container startet nicht

- Prüfe die Logs: `docker logs <container-name>`
- Stelle sicher, dass alle erforderlichen Umgebungsvariablen gesetzt sind
- Überprüfe die Template-Konfiguration

## 🤝 Beitragen

Eigene Templates oder Verbesserungen? Gerne!

1. Fork das Repository
2. Erstelle einen Feature-Branch
3. Committe deine Änderungen
4. Erstelle einen Pull Request

## 📝 Lizenz

MIT License - Siehe LICENSE Datei für Details

## 🎯 Roadmap

- [ ] Docker Compose Unterstützung
- [ ] Multi-Container Setups
- [ ] Template-Pakete
- [ ] Web-Interface
- [ ] Container-Updates
- [ ] Backup-Funktionen

## 💬 Support

Bei Fragen oder Problemen erstelle bitte ein Issue im Repository.

---

**Viel Spaß mit Docklite! 🐳**
