# Rename Python scripts based on content analysis

Get-ChildItem -Path .\*.py | ForEach-Object {
  $content = Get-Content $_.FullName -Raw
  # Simple heuristic: try to extract a descriptive name from the first docstring or function name
  if ($content -match "#.*?\n(.*?)\n") {
    $description = $matches[1].Trim() -replace '\s+', '_'
    $newName = "$($description).py"
  } elseif ($content -match "def\s+(\w+)\s*\(") {
    $description = $matches[1]
    $newName = "$($description).py"
  } else {
    $newName = "unnamed_{0}.py" -f ([System.Security.Cryptography.SHA256]::Create().ComputeHash([System.Text.Encoding]::UTF8.GetBytes($_.Name)) | ForEach-Object {$_.ToString("X2")})
  }

  Rename-Item -Path $_.FullName -NewName $newName -WhatIf
}

# Remove -WhatIf to actually rename files.
