# Local AI Web Search: SearXNG on Windows

Download the current practice kit: [PRACTICE-KIT.zip](downloads/PRACTICE-KIT.zip).

Install a separate local SearXNG service, search for a guide, open the original source and save the real response. Then connect a tool adapter so an assistant can search and read that returned URL.

Start with [the Windows walkthrough](EN/WINDOWS-PRACTICE.md). The new scripts are `install_windows.py` and `suchprobe.py`; both use Python. The installer generates `START-SEARXNG.py`, so the demonstrated route also works when PowerShell scripts are restricted.

Tested on 10 October: fresh Python 3.11 installation, generated launcher, real browser/JSON search and opening the original Search API page. We fixed the Windows template-path error and repeated the search. A freshly installed MCP adapter also completed search → original-page read. The isolated test service was stopped afterwards.

Requirements: Windows, Python 3.11, Internet for downloads/search, and Node 22+ for the optional MCP adapter. Our tested computer was an EVO-X2; setup and timings can differ elsewhere.

The older DE/EN ZIPs under `downloads` contain the earlier search-only kit. The new scripts and walkthrough belong to this revision. Original source: https://github.com/searxng/searxng

Test hardware: [GMKtec EVO-X2 / shop](https://de.gmktec.com/?ref=DolmarioAi) · advertisement / affiliate link.

## Deutsch

Eine eigene SearXNG-Installation anlegen, wirklich suchen, den Originaltreffer öffnen und die Antwort speichern. Danach den Werkzeugadapter mit dem Assistenten verbinden. [Die deutsche Anleitung](DE/WINDOWS-PRAXIS.md) enthält Installation, Python-Starter, Suchprobe, MCP-Verbindung und den tatsächlichen Windows-Fehler.

Am 10. Oktober frisch unter Windows auf dem EVO-X2 geprüft. Der Installer erzeugt einen eigenen Ordner; die bestehende Suche blieb erhalten. Alte ZIPs unter `downloads` sind ältere Suchtest-Pakete. Neue Videos verwenden englischen Ton und deutsche Untertitel.
