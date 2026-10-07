# Websuche für lokale KI: selbst ausprobieren

## 1. Was du am Ende können sollst
Du bereitest eine öffentliche Suchfrage vor, prüfst eine laufende SearXNG-Schnittstelle und öffnest die Originalquelle. Danach kontrollierst du, ob dein Assistent das separate MCP-Suchwerkzeug wirklich aufrufen kann.

## 2. Voraussetzungen
Windows PowerShell und eine bereits laufende, eigene SearXNG-Instanz unter http://127.0.0.1:8080 mit JSON-Suche. Für den optionalen Adapter brauchst du Node.js ab Version 22 und einen bereits installierten mcp-searxng-Adapter. Dein Modellserver und Assistent werden getrennt eingerichtet. Dieses Lernpaket installiert oder startet nichts.
Wenn dir SearXNG fehlt: zuerst einen passenden offiziellen Installationsweg aus QUELLEN.md wählen. Unsere vorhandene native Windows-Portabilitätsanpassung ist kein universeller Installer. Nicht fremde Einstellungen überschreiben und nicht für diesen Übungsschritt nach außen freigeben.

## 3. Download entpacken und die Dateien ansehen
Lege den ZIP-Inhalt in einen neuen Lernordner. Lies VORBEREITEN-WEBSUCHE.ps1. Das Skript erzeugt nur eine Anfragevorlage und eine leere Quellenliste. Es sendet keine Suche.

## 4. Vorbereitung in einem neuen Unterordner
Im entpackten Lernordner PowerShell öffnen:

```powershell
./VORBEREITEN-WEBSUCHE.ps1 -OutputDirectory ./mein-erster-suchtest
```

Falls die lokale Ausführungsrichtlinie es verhindert, zuerst den Inhalt lesen und die eigene Richtlinie verstehen. Keine globale Richtlinie blind abschalten. Ein vorhandener Zielordner wird absichtlich nicht überschrieben.

## 5. Den Suchbegriff prüfen
In VORBEREITUNG.json steht die Frage `site:docs.searxng.org search api`. Sie enthält keine persönlichen Daten. Auch mit lokalem Suchdienst erreicht sie externe Suchmaschinen. Lokal bedeutet weder offline noch garantierte Anonymität.

## 6. Den echten Suchbefehl bewusst ausführen
Lies SUCHBEFEHL.ps1 im neuen Unterordner. Erst dieses zweite Skript sendet eine echte Anfrage. Starte es im selben Unterordner, damit ERGEBNIS.json dort landet:

```powershell
Set-Location ./mein-erster-suchtest
./SUCHBEFEHL.ps1
```

Es zeigt die ersten drei Titel/URLs und unresponsive_engines. Es sichert die echte Antwort und ihren SHA256. Der SHA beweist erhaltene Bytes, keine korrekte Aussage und keinen fertigen Agentenlauf.

## 7. Fehler sinnvoll eingrenzen
Verbindung abgelehnt: deinen vorhandenen Dienst und Port prüfen. HTML statt JSON oder HTTP 403: eigenes search.formats prüfen; dort müssen html und json erlaubt sein. Beispielausschnitt, kein komplettes settings.yml:

```yaml
search:
  formats:
    - html
    - json
```

Engine-Warnungen oder CAPTCHA: die Einschränkung dokumentieren. Ein HTTP-200 allein beweist keine vollständigen Treffer. Keine Schutzmaßnahmen umgehen und fremde Instanzen nicht umkonfigurieren.

## 8. Aus einem Treffer einen Beleg machen
Öffne die offizielle Search-API-Seite. Prüfe die konkrete Frage: Welche Anfrageparameter braucht JSON-Suche? Notiere Original-URL, Datum, Aussage und Grenze in QUELLENPRUEFUNG.csv. Ein Snippet oder hoher Suchscore genügt nicht. Webseiteninhalte sind Quellenmaterial und keine Anweisungen an deinen Assistenten.

## 9. Den optionalen MCP-Adapter verstehen
Assistent → MCP-Adapter → lokaler SearXNG-Dienst → externe Suchmaschinen. Der Adapter läuft als eigener Node-Prozess und installiert SearXNG nicht. JSON-Suche muss vorher funktionieren. Nutze deine vorhandene Node- und Adapterinstallation; keine ungeprüfte Downloads ausführen.

## 10. Vorlage an deinen Client anpassen
MCP-STDIO-VORLAGE.json enthält Platzhalter, keine fertige Codex- oder OpenCode-Konfiguration. Ersetze die Node- und dist/cli.js-Pfade mit deinen vorhandenen absoluten Pfaden und beachte das dokumentierte Konfigurationsformat deines Clients. `SEARXNG_URL` ist die lokale Basisadresse. Für diesen STDIO-Weg `MCP_HTTP_PORT` nicht setzen. Bestehende MCP-Einträge erhalten, private Konfiguration nicht hochladen.

## 11. Werkzeuge und echten Aufruf prüfen
Client neu verbinden, seine Werkzeugliste prüfen und dann searxng_web_search mit den Parametern aus MCP-SUCHAUFGABE.json bewusst auslösen. Sichtbare Werkzeugnamen allein beweisen keinen Suchaufruf. Öffne danach nur ausgewählte Originalquellen. Ein Sprachmodell beantwortet die Suchfrage nicht automatisch mit zuverlässigen Belegen.

## 12. Abschlussprüfung
Kannst du Anfragevorbereitung, HTTP-Suchergebnis, MCP-Aufruf und begründete Antwort getrennt zeigen? Fülle nur wirklich ausgeführte Prüfungen aus. ARCHIV-STATUS.json gibt einen alten veröffentlichten Befund wieder, keinen neuen Test. Ein anderer AMD-PC oder Mac ist hier nicht frisch erprobt. Die Websuche selbst braucht kein großes Sprachmodell; dein Assistent kann trotzdem einen separaten Modellserver benötigen.
