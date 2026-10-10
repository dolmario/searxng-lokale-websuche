# Eine neue lokale Suche unter Windows aufbauen

Dieser Stand ergänzt den bisherigen Suchtest um einen Installationsweg. Am 10. Oktober haben wir in einem eigenen neuen Ordner Python 3.11, eine virtuelle Umgebung und den festgelegten SearXNG-Quellstand installiert. Eine echte Browser- und JSON-Suche lieferte anschließend die offizielle Search-API-Seite. Unsere schon vorhandene Suche auf Port 8080 blieb dabei unverändert.

## Herunterladen und installieren

Den ganzen neuen Begleitordner entpacken. Die bisherigen DE/EN-ZIPs unter `downloads` sind ältere Suchtest-Pakete und enthalten diesen neuen Installer noch nicht. Der neue Stand liegt zunächst als lokaler Entwurf vor.

Python 3.11 für Windows von https://www.python.org/downloads/windows/ installieren, falls es fehlt. Im entpackten Ordner ein Terminal öffnen. Der folgende Befehl verwendet den Python-Launcher und legt einen **neuen** Zielordner an:

```powershell
py -3.11 .\install_windows.py --target .\MEINE-SEARX-SUCHE --port 18080
```

Der Installer lädt den offiziellen Quellstand `3fdc6d753a339b5f4a7dc5842c94c0d8324726f1`, installiert dessen Pakete, ergänzt `tzdata` und erstellt die Konfiguration. Downloads und Paketinstallation benötigen Internet. Ein vorhandener Zielordner wird abgewiesen. `INSTALLATION.log` enthält die tatsächlichen Befehle; `INSTALLATION.json` die Quellrevision und Hashes.

## Konfiguration ansehen und starten

`MEINE-SEARX-SUCHE\settings-ANSICHT.yml` öffnen. Die tatsächliche Datei `settings.yml` enthält einen neu erzeugten Schlüssel und bleibt lokal. `search.formats: [html, json]` erlaubt beide Ausgabeformen. Adresse ist `127.0.0.1`, Port `18080`. Diese Konfiguration ist für die lokale Übung gedacht.

```powershell
py -3.11 .\MEINE-SEARX-SUCHE\START-SEARXNG.py
```

Das Terminal bleibt geöffnet. Der Python-Starter funktioniert auch, wenn Windows PowerShell Skripte sperrt; die Systemeinstellung wird dafür nicht geändert. Im Browser `http://127.0.0.1:18080` aufrufen und `SearXNG search API documentation` suchen. Den Treffer unter `docs.searxng.org/dev/search_api.html` öffnen. Auf der Originalseite stehen die Erklärung für `q` und die Freigabe des Ausgabeformats in `settings.yml`. Die Suchfrage wird an externe Suchmaschinen weitergereicht.

## Dasselbe Ergebnis als Datei

Ein zweites Terminal im Begleitordner öffnen:

```powershell
py -3.11 .\suchprobe.py --base-url http://127.0.0.1:18080 --output .\mein-suchergebnis.json
```

`mein-suchergebnis.json` öffnen: Titel, URL, Auszüge und `unresponsive_engines` bleiben erhalten. Unser aktueller Test lieferte die offizielle API-Seite als ersten Treffer; Brave meldete eine Ratenbegrenzung und Startpage ein Captcha. Diese Meldungen stehen neben den brauchbaren Ergebnissen.

## Beenden, wiederholen und eigene Frage

Im Serverterminal mit Strg+C beenden. Zum nächsten Start denselben Startbefehl verwenden. Bei einer eigenen Frage einen neuen Dateinamen wählen:

```powershell
py -3.11 .\suchprobe.py --base-url http://127.0.0.1:18080 --query 'SearXNG settings search formats' --output .\zweite-suche.json
```

Eine vorhandene Ergebnisdatei wird nicht überschrieben. Bei belegtem Port einen freien Port vor der Installation wählen oder in der eigenen Konfiguration ändern. Ein Verbindungsfehler heißt zunächst: Serverterminal und Adresse prüfen. `403` bei JSON: `search.formats` prüfen.

`suchprobe.py` braucht nur die Python-Standardbibliothek und funktioniert auch bei gesperrten PowerShell-Skripten. Die ältere `TEST-WEBSUCHE.ps1` bleibt als Alternative enthalten; die oben gezeigte Python-Probe umgeht keine Systemeinstellung.

## Der echte Windows-Fehler

Beim ersten Suchlauf der neuen Installation erschien `500`, obwohl die Startseite funktionierte. Windows lieferte bei der Aufzählung der Ergebnisvorlagen Backslashes; die spätere Vorlagensuche erwartet Schrägstriche. Der Installer korrigiert im festgelegten Quellstand `result_templates.add(f)` zu `result_templates.add(f.replace(os.sep, "/"))`. Dazu kommt die schon vorher verwendete optionale `pwd`-Einbindung für Windows. Beide Änderungen werden mit Vorher-/Nachher-Hashes dokumentiert. Unerwarteter Quellcode führt zum Abbruch der Patchanwendung.

## Den Assistenten verbinden

Node.js 22 oder neuer von https://nodejs.org/ installieren, falls es fehlt. Der hier geprüfte Lauf verwendete Node 24.19.0. Im Begleitordner:

```powershell
npm install --prefix .\MEIN-MCP --no-audit --no-fund mcp-searxng@2.1.0
```

`MCP-STDIO-VORLAGE.json` öffnen. Den vollständigen eigenen Node-Pfad und den Pfad zu `MEIN-MCP\node_modules\mcp-searxng\dist\cli.js` einsetzen. `SEARXNG_URL` auf `http://127.0.0.1:18080` setzen. Diesen stdio-Eintrag in der MCP-Konfiguration des eigenen Assistenten übernehmen und dort dessen Verbindung neu laden.

Der frische Adapter meldete `searxng_web_search`, `searxng_search_suggestions`, `searxng_instance_info` und `web_url_read`. Tatsächlich geprüft: `searxng_web_search` mit `SearXNG search API documentation` → URL aus dieser Antwort → `web_url_read` mit dieser URL. Der Leser lieferte den Originaltext der Search-API-Seite. Die Prüfung verwendete unsere bestehende Suche auf Port 8080; für deine neue Übungsinstanz ist 18080 einzusetzen.

Die installierte Übungsinstanz wurde nach der Aufnahme wieder beendet. Sie startet nicht automatisch im Hintergrund.

Der Installer normalisiert auch die Pfade im Verzeichnis der statischen Dateien. Dadurch funktionieren die CSS- und JavaScript-Adressen unter Windows. Die korrigierte Fassung wurde in einem neuen Ordner installiert und mit echter Browser-Suche, dem Klick zur Originalquelle und HTTP-200-Antworten der Dateien geprüft.
