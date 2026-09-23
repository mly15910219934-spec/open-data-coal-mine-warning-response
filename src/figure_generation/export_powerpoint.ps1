param([Parameter(Mandatory=$true)][string]$Source,[Parameter(Mandatory=$true)][string]$Destination,[int]$Slide=1)
$ErrorActionPreference = 'Stop'
$app = $null
$deck = $null
try {
    $app = New-Object -ComObject PowerPoint.Application
    $deck = $app.Presentations.Open($Source, $true, $false, $false)
    $width = 4500
    $height = [int][Math]::Round($width * $deck.PageSetup.SlideHeight / $deck.PageSetup.SlideWidth)
    $deck.Slides.Item($Slide).Export($Destination, 'PNG', $width, $height)
} finally {
    if ($null -ne $deck) { $deck.Close() }
    if ($null -ne $app) { $app.Quit() }
}
