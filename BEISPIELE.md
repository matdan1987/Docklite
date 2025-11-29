# 📚 Docklite Beispiele und Tutorials

Hier findest du ausführliche Beispiele und Schritt-für-Schritt Anleitungen für verschiedene Szenarien.

## 🎯 Schnellstart-Szenarien

### Szenario 1: Einfacher Webserver für statische Website

**Ziel:** Eine HTML-Website lokal hosten

1. HTML-Verzeichnis erstellen:
   ```bash
   mkdir html
   echo "<h1>Hallo Welt!</h1>" > html/index.html
   ```

2. Nginx deployen:
   ```bash
   python docklite.py deploy nginx
   ```

3. Bei der Konfiguration eingeben:
   - Port: `8080` (oder einen anderen freien Port)
   - HTML-Verzeichnis: `./html`

4. Browser öffnen: http://localhost:8080

**Fertig!** Deine Website läuft jetzt in einem Docker Container.

---

### Szenario 2: Development Datenbank für lokale Entwicklung

**Ziel:** PostgreSQL Datenbank für ein Entwicklungsprojekt

1. PostgreSQL deployen:
   ```bash
   python docklite.py deploy postgres
   ```

2. Konfiguration:
   - Port: `5432`
   - Passwort: `dev123` (nur für lokale Entwicklung!)
   - Benutzer: `devuser`
   - Datenbank: `myapp_dev`
   - Daten-Verzeichnis: `./postgres-data`

3. In deiner App verbinden:
   ```python
   # Python Beispiel
   import psycopg2

   conn = psycopg2.connect(
       host="localhost",
       port=5432,
       database="myapp_dev",
       user="devuser",
       password="dev123"
   )
   ```

---

### Szenario 3: WordPress Blog mit Datenbank

**Ziel:** Vollständiger WordPress-Blog

**Schritt 1: MariaDB deployen**

```bash
python docklite.py deploy mariadb
```

Konfiguration:
- Port: `3306`
- Root-Passwort: `rootpass123`
- Benutzer: `wordpress`
- Passwort: `wp123`
- Datenbank: `wordpress`
- Daten-Verzeichnis: `./mariadb-data`

**Schritt 2: WordPress deployen**

```bash
python docklite.py deploy wordpress
```

Konfiguration:
- Port: `8080`
- Datenbank Host: `mariadb:3306`
- Datenbank Benutzer: `wordpress`
- Datenbank Passwort: `wp123`
- Datenbank Name: `wordpress`
- Daten-Verzeichnis: `./wordpress-data`

**Schritt 3: WordPress einrichten**

1. Öffne http://localhost:8080
2. Folge dem WordPress-Installationsassistenten
3. Erstelle deinen Admin-Account

**Hinweis:** Für einen produktiven Blog solltest du:
- Sichere Passwörter verwenden
- HTTPS einrichten (z.B. mit Traefik oder nginx-proxy)
- Regelmäßige Backups erstellen

---

### Szenario 4: Redis Cache für Performance

**Ziel:** Redis als Cache-Server

```bash
python docklite.py deploy redis
```

Konfiguration:
- Port: `6379`
- Daten-Verzeichnis: `./redis-data`

Verwendung in deiner App:
```python
# Python Beispiel
import redis

r = redis.Redis(host='localhost', port=6379, db=0)
r.set('key', 'value')
value = r.get('key')
```

```javascript
// Node.js Beispiel
const redis = require('redis');
const client = redis.createClient({
  host: 'localhost',
  port: 6379
});

client.set('key', 'value');
client.get('key', (err, value) => {
  console.log(value);
});
```

---

### Szenario 5: Docker mit GUI verwalten (Portainer)

**Ziel:** Grafische Oberfläche für Docker

```bash
python docklite.py deploy portainer
```

Konfiguration:
- Web UI Port: `9000`
- Edge Agent Port: `8000`
- Daten-Verzeichnis: `./portainer-data`

Nach dem Start:
1. Öffne http://localhost:9000
2. Erstelle Admin-Account (Username + Passwort)
3. Wähle "Local" Environment
4. Verwalte all deine Container grafisch!

**Portainer Features:**
- Container starten/stoppen/löschen
- Logs anzeigen
- Terminal in Container öffnen
- Images verwalten
- Networks und Volumes verwalten
- Resource Usage überwachen

---

### Szenario 6: Nextcloud - Private Cloud

**Ziel:** Eigene Cloud-Lösung wie Dropbox/Google Drive

```bash
python docklite.py deploy nextcloud
```

Konfiguration:
- Port: `8080`
- Admin Benutzer: `admin`
- Admin Passwort: `secure123` (wähle ein sicheres!)
- Daten-Verzeichnis: `./nextcloud-data`

Nach dem Start:
1. Öffne http://localhost:8080
2. Warte 1-2 Minuten (erste Initialisierung)
3. Login mit deinen Admin-Credentials
4. Installiere Apps (Calendar, Contacts, Notes, etc.)

**Nextcloud-Tipps:**
- Mobile Apps verfügbar (iOS/Android)
- Desktop Sync Client verfügbar
- Für externe Zugriffe: DynDNS + Port-Forwarding einrichten
- Für Produktivumgebung: HTTPS mit Let's Encrypt

---

## 🔄 Multi-Container Setups

### Setup 1: Microservices Stack

Für eine komplette Microservices-Umgebung:

```bash
# 1. Datenbank
python docklite.py deploy postgres --var port=5432 --var database=app_db

# 2. Cache
python docklite.py deploy redis --var port=6379

# 3. MongoDB für Logs
python docklite.py deploy mongodb --var port=27017

# 4. Management
python docklite.py deploy portainer --var port=9000
```

### Setup 2: Web Development Stack

```bash
# 1. MariaDB
python docklite.py deploy mariadb --var port=3306

# 2. Redis für Sessions
python docklite.py deploy redis --var port=6379

# 3. Nginx als Reverse Proxy
python docklite.py deploy nginx --var port=80
```

---

## 🛠️ Erweiterte Nutzung

### Eigenes Template erstellen

Beispiel: Custom PHP-App

Erstelle `templates/php-app.yaml`:

```yaml
name: my-php-app
description: Meine PHP Anwendung
image: php:8.2-apache
detached: true
restart: unless-stopped

ports:
  - "${port}:80"

volumes:
  - "${app_dir}:/var/www/html"

environment:
  PHP_MEMORY_LIMIT: "${memory}"

variables:
  port:
    description: "Webserver Port"
    default: "8080"
  app_dir:
    description: "Pfad zur PHP-App"
    default: "./app"
  memory:
    description: "PHP Memory Limit"
    default: "256M"

info: |
  PHP App läuft auf http://localhost:${port}
```

Deployen:
```bash
python docklite.py deploy php-app
```

---

## 🐛 Troubleshooting-Beispiele

### Problem: Container startet nicht

**Diagnose:**
```bash
# Container Status prüfen
docker ps -a

# Logs ansehen
docker logs <container-name>

# Container Details
docker inspect <container-name>
```

**Lösung je nach Fehler:**

1. **Port bereits belegt:**
   ```bash
   # Anderen Port verwenden
   python docklite.py deploy nginx --var port=8081
   ```

2. **Volume-Berechtigungen:**
   ```bash
   # Verzeichnis erstellen und Rechte setzen
   mkdir -p ./data
   chmod 777 ./data
   ```

3. **Netzwerk-Probleme:**
   ```bash
   # Docker neu starten
   sudo systemctl restart docker
   ```

### Problem: Container können nicht miteinander kommunizieren

**Lösung: Eigenes Docker Network erstellen**

```bash
# Network erstellen
docker network create my-network

# Container mit Network starten (Template anpassen)
# Im Template hinzufügen:
# network: my-network
```

---

## 📊 Container Management

### Alle Container auflisten
```bash
docker ps -a
```

### Container stoppen
```bash
docker stop <container-name>
```

### Container neu starten
```bash
docker restart <container-name>
```

### Container entfernen
```bash
# Stoppen
docker stop <container-name>

# Entfernen
docker rm <container-name>

# In einem Befehl
docker rm -f <container-name>
```

### Alle gestoppten Container entfernen
```bash
docker container prune
```

### Volumes aufräumen
```bash
docker volume prune
```

---

## 🎓 Best Practices

### 1. Entwicklung vs. Produktion

**Entwicklung:**
- Einfache Passwörter OK
- Daten können gelöscht werden
- Direkte Port-Mappings

**Produktion:**
- Starke Passwörter (min. 16 Zeichen)
- Regelmäßige Backups
- Reverse Proxy mit HTTPS
- Resource Limits setzen
- Monitoring einrichten

### 2. Daten-Persistenz

Verwende **immer** Volumes für wichtige Daten:
```yaml
volumes:
  - "./data:/var/lib/mysql"  # ✅ Gut
```

Nicht:
```yaml
# ❌ Daten gehen verloren wenn Container gelöscht wird
# (keine Volume-Angabe)
```

### 3. Backups

Einfaches Backup-Skript:
```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
tar -czf backup_${DATE}.tar.gz \
  ./postgres-data \
  ./redis-data \
  ./wordpress-data

echo "Backup erstellt: backup_${DATE}.tar.gz"
```

### 4. Updates

Container aktualisieren:
```bash
# 1. Container stoppen und entfernen
docker stop <container-name>
docker rm <container-name>

# 2. Neues Image pullen
docker pull <image-name>:latest

# 3. Container neu deployen
python docklite.py deploy <template>
```

---

## 💡 Profi-Tipps

### Automatisches Cleanup

Alte, ungenutzte Ressourcen entfernen:
```bash
# Alles auf einmal
docker system prune -a

# Nur gestoppte Container
docker container prune

# Nur ungenutzte Images
docker image prune -a

# Nur ungenutzte Volumes
docker volume prune
```

### Resource Monitoring

Container-Ressourcen überwachen:
```bash
# Live-Stats
docker stats

# Nur ein Container
docker stats <container-name>
```

### Logs verfolgen

```bash
# Live-Logs
docker logs -f <container-name>

# Letzte 100 Zeilen
docker logs --tail 100 <container-name>

# Mit Timestamps
docker logs -t <container-name>
```

---

**Viel Erfolg mit Docklite!** 🚀

Bei Fragen oder weiteren Beispiel-Wünschen, erstelle ein Issue im Repository.
