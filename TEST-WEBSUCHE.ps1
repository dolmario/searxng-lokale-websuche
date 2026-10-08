param(
 [Parameter(Mandatory=$true)][string]$OutputFile,
 [string]$BaseUrl='http://127.0.0.1:8080',
 [string]$Query='SearXNG search API documentation'
)
$ErrorActionPreference='Stop'
$taskUri=[uri]$BaseUrl
if (!$taskUri.IsAbsoluteUri -or $taskUri.Scheme -ne 'http' -or $taskUri.Host -notin @('127.0.0.1','localhost','[::1]','::1') -or $taskUri.UserInfo -or $taskUri.Query -or $taskUri.Fragment -or $taskUri.AbsolutePath -ne '/') { throw 'Use your own plain HTTP loopback base URL' }
if ([string]::IsNullOrWhiteSpace($Query)) { throw 'A public query is required' }
$taskPath=[IO.Path]::GetFullPath($OutputFile)
if (Test-Path -LiteralPath $taskPath) { throw 'Output already exists; original result preserved' }
if (!(Test-Path -LiteralPath ([IO.Path]::GetDirectoryName($taskPath)))) { throw 'Choose an existing output directory' }
# This GET sends the public query to external search engines through your local service.
$taskUrl=$BaseUrl.TrimEnd('/')+'/search?q='+[uri]::EscapeDataString($Query)+'&format=json'
$taskResult=Invoke-RestMethod -Uri $taskUrl -TimeoutSec 45
if ($null -eq $taskResult.results) { throw 'Expected a SearXNG JSON response with results' }
$taskBytes=[Text.UTF8Encoding]::new($false).GetBytes(($taskResult | ConvertTo-Json -Depth 50))
# CreateNew also protects against another writer appearing after the initial check.
$taskStream=[IO.File]::Open($taskPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$taskStream.Write($taskBytes,0,$taskBytes.Length)} finally {$taskStream.Dispose()}
$taskResult.results | Select-Object -First 5 title,url
Write-Output 'Engine warnings: inspect alongside usable results'
$taskResult.unresponsive_engines
Get-FileHash -LiteralPath $taskPath -Algorithm SHA256
