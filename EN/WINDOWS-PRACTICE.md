# Install local SearXNG and open an original source

Tested on Windows on our EVO-X2. Extract the complete companion folder. The older ZIPs under `downloads` predate this installer; use the scripts in this revision.

## Install

Install Python 3.11 from https://www.python.org/downloads/windows/ if needed. Open a terminal in the companion folder:

```powershell
py -3.11 .\install_windows.py --target .\MY-SEARX-SEARCH --port 18080
```

The installer creates a new folder and a separate Python environment, downloads the pinned official SearXNG source and installs its requirements. It records commands in `INSTALLATION.log`. An existing destination is preserved.

## Start and search

```powershell
py -3.11 .\MY-SEARX-SEARCH\START-SEARXNG.py
```

Leave that terminal open. Open `http://127.0.0.1:18080` and search for `SearXNG search API documentation`. Open the returned official `docs.searxng.org/dev/search_api.html` link. Queries are passed to external search engines.

`settings-ANSICHT.yml` is the shareable configuration view. The actual `settings.yml` contains a newly generated local secret. `search.formats: [html, json]` enables browser and structured responses.

## Save the real response

In another terminal:

```powershell
py -3.11 .\suchprobe.py --base-url http://127.0.0.1:18080 --output .\my-search-result.json
```

Open the saved file. It contains the titles, URLs, excerpts and engine messages. This Python script needs only the standard library and works even when PowerShell scripts are restricted. It does not change the system’s script policy.

To repeat with another query, use a new output name:

```powershell
py -3.11 .\suchprobe.py --base-url http://127.0.0.1:18080 --query 'SearXNG settings formats' --output .\second-search.json
```

Stop your own server terminal with Ctrl+C; restart with the same Python launcher.

## Connect the assistant

Install Node.js 22 or newer from https://nodejs.org/ if needed. We tested Node 24.19.0 and adapter 2.1.0:

```powershell
npm install --prefix .\MY-MCP --no-audit --no-fund mcp-searxng@2.1.0
```

Open `MCP-STDIO-VORLAGE.json`. Enter your complete Node executable path, the path to `MY-MCP\node_modules\mcp-searxng\dist\cli.js`, and `SEARXNG_URL=http://127.0.0.1:18080`. Add this stdio entry to your assistant’s MCP configuration and reload its connection.

The fresh adapter exposed `searxng_web_search`, `searxng_search_suggestions`, `searxng_instance_info` and `web_url_read`. Our actual test called search, then passed a URL from that response to `web_url_read`, which returned the original Search API page. This adapter test used our existing service on port 8080; the fresh installation used 18080.

## The Windows error we fixed

Our first search returned 500 although the start page worked. Windows template paths contained backslashes. The installer now applies `result_templates.add(f.replace(os.sep, "/"))` to the pinned source, records its before/after hashes, and refuses an unexpected source layout. After the fix, browser and JSON searches worked.

Connection error: check the running terminal and port. JSON 403: check `search.formats`. Engine CAPTCHA/rate-limit messages are retained alongside usable results. Other computers can differ in setup and timings.
