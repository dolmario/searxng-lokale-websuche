# Actual search evidence, 8 October 2026

The existing MCP connector returned the official SearXNG Search API page for `SearXNG search API documentation`. The returned URL was subsequently opened through `web_url_read`; the page supports the explanation of q, format=json and enabled search formats. No direct pre-known URL was substituted for finding the source. A separate query `Python documentation` returned docs.python.org and its tutorial; the tutorial result was also opened.

Default engine selection succeeded. Earlier explicit Google/Bing and Brave queries returned no usable results. Some default engines still reported timeout/CAPTCHA/rate-limit warnings while other engines supplied the correct source. Therefore a warning is not proof that the entire search service fails, and the presence of a result is not proof of a correct answer.

The earlier failed test remains in SUCHTEST-MCP-20261007.json. No fresh installation, server restart, universal search reliability or new local Qwen inference is claimed. This is a real assistant MCP search and source-read demonstration.
