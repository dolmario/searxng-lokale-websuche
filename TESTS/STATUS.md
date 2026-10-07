# Actual connector check — 2026-10-07

An existing Codex MCP connection completed one public query, `site:docs.searxng.org search api`, requesting only three results. All three were outside the requested documentation domain: search.ch and two Google pages. Four engines reported rate limits, CAPTCHA or parsing errors. No protective measure was bypassed.

**The tool call worked; the source-finding goal failed.** The highest result score was 1 and still did not support our documentation question. Do not turn this into a successful search or installation claim. The full returned response and exact scope are retained in SUCHTEST-MCP-20261007.json.

The published preparation-only helper remains separate: it was tested offline, and its generated HTTP request was not run in this check. No new assistant installation, OpenCode connection, model inference or full agent answer was tested. The official documentation URLs in QUELLEN.md were reviewed directly; they were not found in this limited connector result.

Deutsch: Der MCP-Aufruf lieferte eine echte Antwort, aber keinen passenden Beleg. Prüfe bei jedem Treffer Domain und Inhalt, dokumentiere Engine-Fehler und behandle einen Suchscore nicht als Wahrheitsnachweis. Die manuelle HTTP-Übung und dein eigener Client-Aufruf bleiben getrennte Schritte.
