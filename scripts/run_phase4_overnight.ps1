param(
    [int]$RepairBatchSize = 25,
    [int]$PopulationBatchSize = 25,
    [string]$Topic = "",
    [string]$Concept = "",
    [int]$ExtraEasy = 0,
    [int]$ExtraMedium = 0
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$python = Join-Path $projectRoot ".venv\Scripts\python.exe"
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$logDir = Join-Path $projectRoot "logs"
$logPath = Join-Path $logDir "phase4-overnight-$timestamp.log"

New-Item -ItemType Directory -Force -Path $logDir | Out-Null
Start-Transcript -Path $logPath

try {
    Set-Location $projectRoot

    if (-not $Topic) {
        $Topic = (& $python -m certcoach.jobs.next_phase4_topic --id-only).Trim()
        if ($LASTEXITCODE -ne 0) { throw "Could not select the next incomplete topic" }
    }
    if (-not $Topic) {
        Write-Output "All syllabus topics are study-ready. No repair or population work required."
        return
    }
    if (-not $Concept) {
        $Concept = (& $python -m certcoach.jobs.next_phase4_topic --topic $Topic --concept-only).Trim()
        if ($LASTEXITCODE -ne 0) { throw "Could not select the next incomplete concept" }
    }
    if (-not $Concept) {
        Write-Output "Topic $Topic is study-ready. No repair or population work required."
        return
    }
    Write-Output "Sequential Phase 4 target: Topic $Topic | Concept: $Concept"

    & $python -m certcoach.jobs.backup_questions
    if ($LASTEXITCODE -ne 0) { throw "Backup failed" }

    $repairArgs = @("-m", "certcoach.jobs.repair_explanations", "--max-questions", $RepairBatchSize)
    $repairArgs += @("--topic", $Topic)
    $repairArgs += @("--concept", $Concept)
    & $python @repairArgs
    if ($LASTEXITCODE -ne 0) { throw "Explanation repair batch failed" }

    $seedArgs = @("-m", "certcoach.jobs.nightly_seed_questions", "--max-questions", $PopulationBatchSize)
    $seedArgs += @("--topic", $Topic)
    $seedArgs += @("--concept", $Concept)
    if ($ExtraEasy -gt 0) { $seedArgs += @("--extra-easy", $ExtraEasy) }
    if ($ExtraMedium -gt 0) { $seedArgs += @("--extra-medium", $ExtraMedium) }
    & $python @seedArgs
    if ($LASTEXITCODE -ne 0) { throw "Population batch failed" }

    & $python -m certcoach.jobs.next_phase4_topic
    if ($LASTEXITCODE -ne 0) { throw "Final readiness report failed" }
}
finally {
    Stop-Transcript
}
