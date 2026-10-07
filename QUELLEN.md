# Primary references checked 2026-10-07

- https://docs.searxng.org/dev/search_api.html — GET/POST search, required q, JSON format must be enabled. A 403 may mean the requested format is not permitted.
- https://docs.searxng.org/admin/settings/settings_search.html — own search.formats configuration.
- https://docs.searxng.org/admin/installation.html — official deployment methods and maintenance guidance; this kit is not a universal Windows installer.
- https://github.com/ihor-sokoliuk/mcp-searxng — separate MCP adapter, Node.js 22+, SEARXNG_URL, client-specific configuration and actual search tool validation.

The author's existing Windows adapter package is 2.1.0. Templates use its existing local Node executable and dist/cli.js path, not an implicit network installation. The example mcpServers structure suits compatible clients; other clients need their own documented configuration shape. Paths are placeholders. No private client configuration, tokens, search histories or existing service settings are included.
