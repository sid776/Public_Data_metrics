# Run this in PowerShell to find Python on your system
Write-Host "Searching for Python..."
$paths = @(
    "$env:LOCALAPPDATA\Programs\Python",
    "$env:ProgramFiles\Python*",
    "${env:ProgramFiles(x86)}\Python*",
    "$env:USERPROFILE\AppData\Local\Programs\Python",
    "$env:USERPROFILE\miniconda3",
    "$env:USERPROFILE\anaconda3"
)
foreach ($base in $paths) {
    Get-ChildItem -Path $base -Filter python.exe -Recurse -ErrorAction SilentlyContinue | Select-Object -First 3 -ExpandProperty FullName
}
Write-Host "`nIf you see a path above, use it like:"
Write-Host '  & "C:\path\to\python.exe" -m pip install -r requirements.txt'
Write-Host '  & "C:\path\to\python.exe" run_api.py'
