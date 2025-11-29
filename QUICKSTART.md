# ⚡ Quickstart - In 5 Minuten zu deinem Homelab

Diese Anleitung zeigt dir, wie du in 5 Minuten deine erste Homelab-Anwendung mit Docklite startest - **ohne Docker-Vorkenntnisse**!

🏠 Wähle aus **16 fertigen Homelab-Apps**: Media Server, Dashboards, Smart Home, Passwort Manager und mehr!

## Schritt 1: Voraussetzungen prüfen ✓

### Python installiert?

```bash
python --version
```

Sollte `Python 3.7` oder höher anzeigen. Falls nicht:
- **Ubuntu/Debian:** `sudo apt install python3`
- **macOS:** `brew install python3`
- **Windows:** Python von python.org herunterladen

### Docker installiert?

```bash
docker --version
```

Falls nicht installiert, siehe [Docker Installation](#docker-installieren) am Ende.

## Schritt 2: Docklite einrichten 🚀

```bash
# 1. In das Verzeichnis wechseln
cd Docklite

# 2. Python-Abhängigkeiten installieren
pip install -r requirements.txt

# Fertig! Das war's schon. 🎉
```

## Schritt 3: Deinen ersten Container starten 🐳

### ⭐ Der einfachste Weg: Interaktives Menü (EMPFOHLEN!)

Starte einfach das Skript **ohne Parameter**:

```bash
python docklite.py
```

Du siehst jetzt ein schönes Menü wie dieses:

```
╔══════════════════════════════════════════════════════════════╗
║                   🐳  D O C K L I T E  🐳                    ║
║           Einfacher Docker Container Deployer                ║
╚══════════════════════════════════════════════════════════════╝

📋 HAUPTMENÜ
  [1] 📦 Container deployen (starten)
  [2] 📋 Alle verfügbaren Templates anzeigen
  [3] ℹ️  Template-Informationen anzeigen
  [4] 🐳 Laufende Container anzeigen
  [5] 🛑 Container stoppen
  [6] 🗑️  Container entfernen
  [0] ❌ Beenden
```

**So startest du deinen ersten Container:**
1. Tippe `1` und drücke Enter (Container deployen)
2. Wähle ein Template, z.B. `5` für nginx
3. Beantworte die Fragen (oder drücke einfach Enter für Standardwerte)
4. Fertig! 🎉

**Das ist alles!** Super einfach, keine Befehle merken!

### Alternative: Kommandozeilen-Modus

Falls du die klassischen Befehle bevorzugst:

```bash
# 1. Verfügbare Templates ansehen
python docklite.py list

# 2. Nginx deployen
python docklite.py deploy nginx
```

Du wirst gefragt:
- **Port auf dem Host [8080]:** Drücke einfach Enter (Standard: 8080)
- **Pfad zum HTML-Verzeichnis [./html]:** Drücke Enter

Erstelle eine Test-Datei:
```bash
mkdir -p html
echo "<h1>Hallo Welt! 🚀</h1>" > html/index.html
```

Öffne deinen Browser: **http://localhost:8080**

**Glückwunsch! Dein erster Container läuft!** 🎉

### Weitere Beispiele mit dem Menü

**Docker GUI (Portainer):**
- Starte Menü: `python docklite.py`
- Wähle `[1]` Container deployen
- Wähle `portainer`
- Bestätige alle Werte mit Enter
- Öffne http://localhost:9000

### Beispiel 2: Docker GUI (Portainer - alte Methode)

**Was macht das?** Gibt dir eine grafische Oberfläche zum Verwalten deiner Container.

```bash
python docklite.py deploy portainer
```

Einfach alle Standardwerte mit Enter bestätigen.

Öffne: **http://localhost:9000**

Beim ersten Start:
1. Erstelle einen Admin-Account (Username + Passwort)
2. Klicke auf "Local"
3. Fertig! Du siehst jetzt alle deine Container

### Beispiel 3: Datenbank (PostgreSQL)

**Was macht das?** Startet eine PostgreSQL-Datenbank.

```bash
python docklite.py deploy postgres
```

Eingaben:
- Port: `5432` (Enter)
- Passwort: `test123` (oder was du möchtest)
- Benutzer: `testuser`
- Datenbank: `testdb`
- Daten-Verzeichnis: `./postgres-data` (Enter)

Fertig! Deine Datenbank läuft auf Port 5432.

## Schritt 4: Container verwalten 🛠️

### Container ansehen
```bash
docker ps
```

Zeigt alle laufenden Container mit:
- Namen
- Status
- Ports
- etc.

### Container stoppen
```bash
docker stop nginx-web
```

Ersetze `nginx-web` mit dem Namen deines Containers.

### Container neu starten
```bash
docker restart nginx-web
```

### Container entfernen
```bash
docker rm -f nginx-web
```

**Achtung:** Daten in Volumes bleiben erhalten!

### Container-Logs ansehen
```bash
docker logs nginx-web
```

Zeigt was im Container passiert.

### Live-Logs verfolgen
```bash
docker logs -f nginx-web
```

Drücke `Ctrl+C` zum Beenden.

## Nützliche Befehle 📋

```bash
# Alle verfügbaren Templates
python docklite.py list

# Info über ein Template
python docklite.py info redis

# Mit eigenen Werten deployen
python docklite.py deploy nginx --var port=8080 --var html_dir=/my/path

# Docker Status
docker ps              # Laufende Container
docker ps -a           # Alle Container (auch gestoppte)
docker images          # Alle Images
docker volume ls       # Alle Volumes

# Aufräumen
docker container prune # Gestoppte Container löschen
docker system prune    # Alles Ungenutzte löschen
```

## Häufige Anfängerfehler ⚠️

### "Permission denied"

**Problem:** Docker benötigt Root-Rechte

**Lösung (Linux):**
```bash
sudo usermod -aG docker $USER
```

Dann **ab- und wieder anmelden**.

### "Port already in use"

**Problem:** Der Port wird schon verwendet.

**Lösung:** Anderen Port wählen:
```bash
python docklite.py deploy nginx --var port=8081
```

### "No such file or directory"

**Problem:** Verzeichnis existiert nicht.

**Lösung:** Erstelle es erst:
```bash
mkdir -p ./mein-verzeichnis
```

Oder verwende absolute Pfade:
```bash
python docklite.py deploy nginx --var html_dir=/home/user/html
```

## Docker installieren 🐳

### Ubuntu / Debian

```bash
# Docker installieren
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Deinen Benutzer zur docker-Gruppe hinzufügen
sudo usermod -aG docker $USER

# Ab- und wieder anmelden (wichtig!)
```

### macOS

1. Docker Desktop herunterladen: https://www.docker.com/products/docker-desktop
2. Installieren und starten
3. Fertig!

### Windows

1. Docker Desktop für Windows: https://www.docker.com/products/docker-desktop
2. WSL2 muss installiert sein
3. Docker Desktop installieren und starten

**Prüfen ob's funktioniert:**
```bash
docker run hello-world
```

## Was jetzt? 🎯

Du kannst jetzt:

✅ **Verschiedene Templates ausprobieren:**
```bash
python docklite.py list
```

✅ **Eigene Templates erstellen:**
Schau dir die Dateien in `templates/` an und erstelle eigene!

✅ **Mehr lernen:**
Lies die [ausführlichen Beispiele](BEISPIELE.md)

✅ **Docker GUI nutzen:**
Deploye Portainer für eine grafische Oberfläche

## Beliebte Container für Einsteiger 🌟

```bash
# Webserver
python docklite.py deploy nginx

# Docker GUI
python docklite.py deploy portainer

# Datenbanken
python docklite.py deploy postgres
python docklite.py deploy mysql
python docklite.py deploy redis

# Cloud-Speicher (wie Dropbox)
python docklite.py deploy nextcloud

# Blog/CMS
python docklite.py deploy wordpress
```

## Hilfe & Support 💬

- 📖 [Vollständige Dokumentation](README.md)
- 📚 [Ausführliche Beispiele](BEISPIELE.md)
- 🐛 Probleme? Erstelle ein Issue

---

**Viel Spaß beim Experimentieren! 🚀**

Docker ist jetzt super einfach! 🐳
