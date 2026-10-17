$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$env:PATH = 'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.9\bin;' + $env:PATH
$env:GRADIO_ANALYTICS_ENABLED = 'False'
& "$PSScriptRoot\.venv\Scripts\python.exe" facefusion.py run --execution-providers cuda --open-browser
