param($Task)

switch ($Task) {
    "run" { py -m tuiapp.main }
    "lint" { ruff check . }
    "format" { ruff format . }
    "fix" { ruff check . --fix }
    "type" { mypy src/ }
    "test" { pytest }
    "build" { py build.py }
    default { Write-Host "Unknown task" }
}