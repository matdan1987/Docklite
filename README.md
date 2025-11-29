# 🐳 Docklite - Einfacher Docker Container Deployer

Docklite ist ein benutzerfreundliches Python-Tool, mit dem du Docker Container kinderleicht nach Vorlagen deployen kannst. Perfekt für Einsteiger, die schnell und unkompliziert Docker Container einrichten möchten!

## ✨ Features

- 📦 **Einfache Templates** - Vorkonfigurierte Vorlagen für beliebte Container
- 🚀 **Schnelles Deployment** - Container mit einem Befehl starten
- 🔧 **Interaktive Konfiguration** - Schritt-für-Schritt Einrichtung
- 📝 **Keine Docker-Kenntnisse nötig** - Ideal für Anfänger
- 🎯 **Erweiterbar** - Eigene Templates einfach hinzufügen

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
   git clone <repository-url>
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

### Verfügbare Templates anzeigen

```bash
python docklite.py list
```

Zeigt alle verfügbaren Container-Templates an.

### Template-Informationen anzeigen

```bash
python docklite.py info nginx
```

Zeigt Details zu einem bestimmten Template (Ports, Volumes, Variablen, etc.).

### Container deployen

```bash
python docklite.py deploy nginx
```

Startet den interaktiven Deployment-Prozess. Du wirst nach allen notwendigen Informationen gefragt.

### Mit benutzerdefinierten Variablen deployen

```bash
python docklite.py deploy nginx --var port=8080 --var html_dir=/path/to/html
```

Überspringe die interaktive Eingabe, indem du Variablen direkt übergibst.

## 📦 Verfügbare Templates

### Webserver & Proxy
- **nginx** - Nginx Webserver
- **wordpress** - WordPress CMS
- **nextcloud** - Private Cloud Storage

### Datenbanken
- **postgres** - PostgreSQL Datenbank
- **mysql** - MySQL Datenbank
- **mariadb** - MariaDB Datenbank
- **mongodb** - MongoDB NoSQL Datenbank

### Cache & Storage
- **redis** - Redis Cache Server

### Management Tools
- **portainer** - Docker GUI Management Tool

## 💡 Beispiele

### Beispiel 1: Nginx Webserver starten

```bash
python docklite.py deploy nginx
```

Das Skript fragt dich nach:
- Port (Standard: 8080)
- HTML-Verzeichnis (Standard: ./html)

Nach dem Start kannst du auf `http://localhost:8080` zugreifen.

### Beispiel 2: PostgreSQL Datenbank

```bash
python docklite.py deploy postgres
```

Konfiguriere:
- Port (Standard: 5432)
- Passwort
- Benutzername
- Datenbank-Name
- Daten-Verzeichnis

### Beispiel 3: Portainer (Docker GUI)

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
