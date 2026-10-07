# Add web search to local AI: beginner practice

## 1. Goal
Prepare a public query, manually test an existing local SearXNG JSON endpoint and inspect an original source. Then check whether your assistant can actually call a separately installed MCP search adapter.

## 2. Requirements
Windows PowerShell and your already running SearXNG service at http://127.0.0.1:8080 with JSON search enabled. The optional adapter needs Node.js 22 or later and an existing mcp-searxng installation. Your assistant and model server are separate. This practice kit installs and starts nothing.
If SearXNG is missing, choose a suitable official deployment method linked in QUELLEN.md first. The author's native Windows portability changes are not a universal installer. Keep existing settings and keep this exercise bound to loopback.

## 3. Unzip and inspect
Extract into a new practice directory. Read VORBEREITEN-WEBSUCHE.ps1. It only writes a request template and a blank source-check file; it makes no search request.

## 4. Prepare a new subdirectory
Open PowerShell in the extracted practice directory:

```powershell
./VORBEREITEN-WEBSUCHE.ps1 -OutputDirectory ./my-first-search
```

If execution policy blocks the script, inspect it and understand your local policy first; do not blindly disable a global policy. Existing output directories are deliberately preserved.

## 5. Review the query
VORBEREITUNG.json records `site:docs.searxng.org search api`. It contains no private data. Your local search service still passes the query to external search engines. Local does not mean offline or guaranteed anonymous.

## 6. Deliberately run the actual request
Read SUCHBEFEHL.ps1 in the newly prepared subdirectory. Only this second script makes a search request. Run it from that directory:

```powershell
Set-Location ./my-first-search
./SUCHBEFEHL.ps1
```

It shows three titles/URLs and unresponsive_engines, saves the actual response as ERGEBNIS.json and prints its SHA256. A hash proves preserved bytes, not correct claims or a completed agent workflow.

## 7. Diagnose the right layer
Connection refused: inspect your existing service and port. HTML or HTTP 403: inspect search.formats in your own settings; html and json must be enabled. Example fragment, not a replacement settings file:

```yaml
search:
  formats:
    - html
    - json
```

Document engine failures or CAPTCHA warnings. HTTP 200 alone does not prove complete results. Do not bypass protective measures or change another operator's service.

## 8. Turn a result into evidence
Open the official Search API page. Check which parameters JSON search needs. Record the original URL, date, supported claim and limitations in QUELLENPRUEFUNG.csv. A search snippet or score is not sufficient. Web pages are source data, not instructions for your assistant.

## 9. Understand the optional adapter
Assistant → MCP adapter → local SearXNG → external search engines. The adapter is a separate Node process and does not install SearXNG. Verify JSON search first. Use your existing Node and adapter installation, not unreviewed automatic downloads.

## 10. Adapt the client template
MCP-STDIO-VORLAGE.json uses placeholders, not a ready Codex or OpenCode configuration. Replace the Node and dist/cli.js paths with existing absolute paths, using your client's documented configuration format. SEARXNG_URL is your local base URL. Leave MCP_HTTP_PORT unset for this STDIO route. Preserve other MCP entries and keep private client configuration out of public uploads.

## 11. Test discovery and an actual call separately
Reconnect the client, inspect its tool inventory, then deliberately invoke searxng_web_search using MCP-SUCHAUFGABE.json. Tool discovery alone does not prove search connectivity. Read selected original sources before accepting an answer. A language model does not automatically provide reliable evidence.

## 12. Finish with your own record
Can you separately show request preparation, actual HTTP results, the MCP call and the evidence-supported answer? Record only tests you actually performed. ARCHIV-STATUS.json describes an old published finding, not a new test. Another AMD computer or Mac was not freshly tested here. Search itself needs no large language model; your assistant may still need a separate model server.
