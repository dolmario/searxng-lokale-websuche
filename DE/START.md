# SearXNG: Suche finden, Originalquelle prüfen

## Was du mitmachst
Wir suchen die offizielle SearXNG-API-Erklärung, öffnen einen echten Treffer und prüfen, welche Parameter JSON-Suche braucht. Diesen kompletten Werkzeugweg haben wir am 8. Oktober tatsächlich ausgeführt. Im alten Video war die Suche ebenfalls belegt; der spätere erfolglose Einzeltest ersetzt diesen Befund nicht.

## 1. Vorhandenen lokalen Suchdienst prüfen
Voraussetzung ist deine bereits laufende eigene SearXNG-Instanz, hier http://127.0.0.1:8080. Öffne die Adresse. Für die JSON-Schnittstelle muss in deiner vorhandenen Konfiguration unter search.formats json erlaubt sein. QUELLEN.md verlinkt die offiziellen Installationswege, falls dir der Dienst fehlt. Dieses Lernpaket startet oder installiert nichts.

## 2. Einen öffentlichen Begriff suchen
Öffne PowerShell im entpackten Lernpaket und lies TEST-WEBSUCHE.ps1. Dann:

```powershell
./TEST-WEBSUCHE.ps1 -OutputFile ./mein-suchergebnis.json
```

Das Skript fragt `SearXNG search API documentation` ab, zeigt Titel/URLs sowie Engine-Warnungen und speichert deine echte JSON-Antwort. Ein vorhandenes Ergebnis bleibt erhalten. Bei einer blockierenden Ausführungsrichtlinie den Inhalt und die eigene Richtlinie prüfen; keine globale Richtlinie blind ändern. Alternativ lautet die reine Anfrage:

```powershell
Invoke-RestMethod 'http://127.0.0.1:8080/search?q=SearXNG%20search%20API%20documentation&format=json'
```

Die JSON-Antwort hat diese Form (gekürzt; Felder aus SearXNG-Search-API):

```json
{
  "query": "SearXNG search API documentation",
  "results": [
    {"title": "...", "url": "https://docs.searxng.org/dev/search_api.html", "content": "...", "engine": "duckduckgo"}
  ],
  "unresponsive_engines": [["brave", "too many requests"], ["qwant", "CAPTCHA"]]
}
```

Die Treffer-URLs holst du so aus der gespeicherten Datei:

```powershell
$r = Get-Content ./mein-suchergebnis.json -Raw | ConvertFrom-Json
$r.results | Select-Object -First 5 title, url, engine
$r.results | Where-Object url -like '*docs.searxng.org/dev/search_api*' | Select-Object -First 1 url
```

Bei unserem Lauf am 8. Oktober kam die offizielle Seite `https://docs.searxng.org/dev/search_api.html` von den Engines `google cse` und `duckduckgo`; `arxiv` (Timeout), `brave` (too many requests), `qwant` und `startpage` (CAPTCHA) meldeten Warnungen. Dein Ergebnis kann abweichen.

## 3. Treffer und Warnungen gemeinsam ansehen
Suche in den Ergebnissen nach docs.searxng.org/dev/search_api.html. Öffne nur die tatsächlich zurückgegebene offizielle URL. Einzelne Engines können CAPTCHA, Zeitüberschreitung oder zu viele Anfragen melden, während andere brauchbare Treffer liefern. Kein Zwang auf eine gerade blockierte Einzelengine. Wenn kein passender Treffer kommt, den Befund erhalten und die Suchfrage eingrenzen. Ein direkter Link aus der Anleitung wäre dann kein erfolgreicher Suchnachweis.

## 4. Mit dem Assistenten über MCP suchen
Dein vorhandener mcp-searxng-Adapter verbindet den Assistenten mit derselben lokalen Suchadresse. MCP-STDIO-VORLAGE.json zeigt Platzhalter für Node und den installierten Adapter. Ersetze nur diese Pfade in deiner passenden Client-Konfiguration; vorhandene andere Einträge erhalten. Für den STDIO-Weg keinen MCP_HTTP_PORT setzen. Die Werkzeugaufrufe in MCP-SUCHAUFGABE.json sind:

```json
{"tool":"searxng_web_search","arguments":{"query":"SearXNG search API documentation","num_results":5,"response_format":"json"}}
```

Danach `web_url_read` mit der passenden URL aus DIESER Trefferliste aufrufen:

```json
{"tool":"web_url_read","arguments":{"url":"https://docs.searxng.org/dev/search_api.html"}}
```

(Die URL stammt hier aus unserem Lauf; nimm die URL aus deiner Liste.) Die sichtbare Werkzeugliste allein ist keine Suche. Ein lokales Sprachmodell braucht die Werkzeuganbindung seines Clients; ein nackter Modellserver sucht nicht von selbst.

## 5. Die konkrete Aussage prüfen
Die geöffnete offizielle API-Seite erklärt: q enthält die Suchfrage, format=json fordert JSON an; das Format muss in search.formats erlaubt sein. Schreibe diese Aussage, Original-URL und dein Prüfdatum in QUELLENPRUEFUNG.csv, zum Beispiel:

```text
date,query,original_url,source_date,claim,source_supports_claim,limitations
2026-10-10,SearXNG search API documentation,https://docs.searxng.org/dev/search_api.html,,"q = Suchfrage; format=json liefert JSON, wenn json in search.formats erlaubt ist",yes,"Engines brave/qwant meldeten Warnungen; andere lieferten Treffer"
```

Ein Snippet oder Suchscore reicht dafür nicht; die Aussage muss auf der geöffneten Seite stehen.

## 6. Deinen eigenen Nachweis behalten
Behalte Suchfrage, gespeicherte Trefferliste (`mein-suchergebnis.json`), die daraus geöffnete URL und die belegte Aussage. TESTS/SUCHWEG-MCP-20261008.json beschreibt unseren ausgeführten MCP-Test; dein eigenes Ergebnis kann abweichen. Es ist kein neuer Qwen-Leistungstest. Lokal betrieben heißt weiterhin mit Internetzugriff: Suchbegriffe erreichen externe Suchmaschinen, keine privaten Daten eingeben.
