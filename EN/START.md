# SearXNG: find a result and check its original source

## The practical task
Find the official SearXNG Search API page, open a real returned result and check the parameters needed for JSON search. The assistant actually completed this tool chain on 8 October 2026. The old video also had search evidence; a later unsuccessful isolated test did not invalidate it.

## 1. Check your existing local service
Use your own already running SearXNG instance, here http://127.0.0.1:8080. JSON must be enabled under search.formats in your own configuration. QUELLEN.md links official deployment instructions if the service is missing. This practice kit does not install or start services or models.

## 2. Search for a public topic
Read TEST-WEBSUCHE.ps1 in the extracted kit, then run:

```powershell
./TEST-WEBSUCHE.ps1 -OutputFile ./my-search-result.json
```

The query is `SearXNG search API documentation`. The script shows result titles/URLs and engine warnings, then preserves the actual JSON response. It never overwrites an existing result. If execution policy blocks it, inspect the script and understand your own policy rather than blindly changing global settings. The direct request is:

```powershell
Invoke-RestMethod 'http://127.0.0.1:8080/search?q=SearXNG%20search%20API%20documentation&format=json'
```

The JSON response has this shape (shortened; fields of the SearXNG Search API):

```json
{
  "query": "SearXNG search API documentation",
  "results": [
    {"title": "...", "url": "https://docs.searxng.org/dev/search_api.html", "content": "...", "engine": "duckduckgo"}
  ],
  "unresponsive_engines": [["brave", "too many requests"], ["qwant", "CAPTCHA"]]
}
```

Pull the result URLs out of the saved file:

```powershell
$r = Get-Content ./my-search-result.json -Raw | ConvertFrom-Json
$r.results | Select-Object -First 5 title, url, engine
$r.results | Where-Object url -like '*docs.searxng.org/dev/search_api*' | Select-Object -First 1 url
```

In our run on 8 October the official page `https://docs.searxng.org/dev/search_api.html` came from the engines `google cse` and `duckduckgo`; `arxiv` (timeout), `brave` (too many requests), `qwant` and `startpage` (CAPTCHA) reported warnings. Your result may differ.

## 3. Inspect results alongside engine warnings
Find docs.searxng.org/dev/search_api.html in the actual returned results. Open that official returned URL. Some engines may report CAPTCHA, timeout or rate limits while other engines supply usable results. Do not force the query through an unavailable engine. If the source is missing, preserve that finding and refine your query; opening a pre-known URL from this guide would not prove successful searching.

## 4. Use the assistant's MCP connection
Your already installed mcp-searxng adapter connects the assistant to the same endpoint. MCP-STDIO-VORLAGE.json contains placeholders for the existing Node and adapter paths. Adapt these to your client's documented configuration format, preserving other entries. Do not set MCP_HTTP_PORT for this STDIO route. MCP-SUCHAUFGABE.json supplies:

```json
{"tool":"searxng_web_search","arguments":{"query":"SearXNG search API documentation","num_results":5,"response_format":"json"}}
```

Next call `web_url_read` with the relevant URL from THAT result list:

```json
{"tool":"web_url_read","arguments":{"url":"https://docs.searxng.org/dev/search_api.html"}}
```

(The URL here comes from our run; use the one from your list.) A tool inventory alone is not a search. A local language model needs its client's tool connection; a bare model server does not search on its own.

## 5. Check the supported claim
The original API page explains that q carries the query and format=json requests JSON, which must be enabled under search.formats. Record this claim, original URL and your check date in QUELLENPRUEFUNG.csv, for example:

```text
date,query,original_url,source_date,claim,source_supports_claim,limitations
2026-10-10,SearXNG search API documentation,https://docs.searxng.org/dev/search_api.html,,"q = query; format=json returns JSON if json is enabled in search.formats",yes,"brave/qwant reported warnings; other engines returned results"
```

A search score or snippet is insufficient; the claim must appear on the opened page.

## 6. Preserve your own evidence
Keep your query, saved result list (`my-search-result.json`), opened result URL and source-supported claim. TESTS/SUCHWEG-MCP-20261008.json is the author's real MCP example; your own results may differ. This is not a fresh Qwen performance test. Local hosting still uses the internet: queries reach external engines, so use public topics.
