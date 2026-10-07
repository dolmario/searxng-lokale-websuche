param(
 [Parameter(Mandatory=$true)][string]$OutputDirectory,
 [string]$BaseUrl='http://127.0.0.1:8080',
 [string]$Query='site:docs.searxng.org search api'
)
$ErrorActionPreference='Stop'
$taskUri=[uri]$BaseUrl
if (!$taskUri.IsAbsoluteUri -or $taskUri.Scheme -ne 'http' -or $taskUri.Host -notin @('127.0.0.1','localhost','[::1]','::1') -or $taskUri.UserInfo -or $taskUri.Query -or $taskUri.Fragment -or $taskUri.AbsolutePath -ne '/') { throw 'Use a plain local loopback base URL, e.g. http://127.0.0.1:8080' }
if ([string]::IsNullOrWhiteSpace($Query)) { throw 'A public search query is required' }
$taskOut=[IO.Path]::GetFullPath($OutputDirectory)
if (Test-Path -LiteralPath $taskOut) { throw 'Output already exists; keep it and choose a new empty directory' }
$taskUrl=$BaseUrl.TrimEnd('/')+'/search?q='+[uri]::EscapeDataString($Query)+'&format=json'
$taskCommand=@"
`$ErrorActionPreference='Stop'
# This command DOES make a search request. The query reaches external search services.
`$r=Invoke-RestMethod -Uri '$taskUrl' -TimeoutSec 30
`$r.results | Select-Object -First 3 title,url
`$r.unresponsive_engines
`$r | ConvertTo-Json -Depth 30 | Set-Content -LiteralPath 'ERGEBNIS.json' -Encoding utf8
Get-FileHash -LiteralPath 'ERGEBNIS.json' -Algorithm SHA256
"@
New-Item -ItemType Directory -Path $taskOut | Out-Null
[IO.File]::WriteAllText((Join-Path $taskOut 'SUCHBEFEHL.ps1'),$taskCommand,[Text.UTF8Encoding]::new($false))
@{query=$Query;request_url=$taskUrl;search_executed=$false;server_started=$false;model_started=$false;downloads=$false} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $taskOut 'VORBEREITUNG.json') -Encoding utf8
[IO.File]::WriteAllText((Join-Path $taskOut 'QUELLENPRUEFUNG.csv'),"date,query,original_url,source_date,claim,source_supports_claim,limitations`r`n",[Text.UTF8Encoding]::new($false))
Write-Output 'Prepared only. Read SUCHBEFEHL.ps1 before manually running it in its own output directory.'
