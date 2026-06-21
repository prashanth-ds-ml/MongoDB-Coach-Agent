param(
    [int]$RepairBatchSize = 25,
    [int]$PopulationBatchSize = 25,
    [string]$Topic = "",
    [string]$Concept = "",
    [int]$ExtraEasy = 0,
    [int]$ExtraMedium = 0,
    [switch]$SingleQuestion,
    [switch]$RepeatUntilClean,
    [int]$MaxCycles = 20
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

    $hasExplicitTopic = [bool]$Topic
    $hasExplicitConcept = [bool]$Concept
    $cycle = 0
    $backupDone = $false

    if ($RepeatUntilClean) {
        Write-Output "Repeat-until-clean mode is enabled. The runner will reselect the next incomplete concept after each repair/population pass."
        Write-Output "Max cycles: $MaxCycles"
    }

    if ($SingleQuestion) {
        $RepairBatchSize = 1
        $PopulationBatchSize = 1
        Write-Output "Single-question mode is enabled. Repair and population will process one question per pass."
    }

    # Keep overnight Topic runs local-first only. Remote fallbacks were adding
    # repeated payment / request failures and slowing down long repair loops.
    $env:POPULATION_MODEL_CHAIN = $env:POPULATION_MODEL_CHAIN_LOCAL_ONLY
    $env:REPAIR_MODEL_CHAIN = $env:REPAIR_MODEL_CHAIN_LOCAL_ONLY
    if (-not $env:POPULATION_MODEL_CHAIN) { $env:POPULATION_MODEL_CHAIN = "gemma4:12b" }
    if (-not $env:REPAIR_MODEL_CHAIN) { $env:REPAIR_MODEL_CHAIN = "gemma4:12b" }
    Write-Output "Local-only model chain enforced for this overnight run."

    while ($true) {
        $cycle++
        if ($cycle -gt $MaxCycles) {
            throw "Reached MaxCycles=$MaxCycles before the selected topic became clean"
        }

        $selectedTopic = $Topic
        if (-not $selectedTopic) {
            $selectedTopic = (& $python -m certcoach.jobs.next_phase4_topic --id-only).Trim()
            if ($LASTEXITCODE -ne 0) { throw "Could not select the next incomplete topic" }
        }
        if (-not $selectedTopic) {
            Write-Output "All syllabus topics are study-ready. No repair or population work required."
            break
        }

        $selectedConcept = $Concept
        if (-not $selectedConcept) {
            $selectedConcept = (& $python -m certcoach.jobs.next_phase4_topic --topic $selectedTopic --concept-only).Trim()
            if ($LASTEXITCODE -ne 0) { throw "Could not select the next incomplete concept" }
        }
        if (-not $selectedConcept) {
            Write-Output "Topic $selectedTopic is study-ready. No repair or population work required."
            break
        }

        Write-Output "Cycle $cycle target: Topic $selectedTopic | Concept: $selectedConcept"

        if (-not $backupDone) {
            & $python -m certcoach.jobs.backup_questions
            if ($LASTEXITCODE -ne 0) { throw "Backup failed" }
            $backupDone = $true
        }

        & $python -m certcoach.jobs.mark_scope_leaks --apply --topic $selectedTopic --concept $selectedConcept
        if ($LASTEXITCODE -ne 0) { throw "Scope audit failed" }

        $triageArgs = @("-m", "certcoach.jobs.triage_quarantined_questions", "--apply")
        $triageArgs += @("--topic", $selectedTopic)
        $triageArgs += @("--concept", $selectedConcept)
        & $python @triageArgs
        if ($LASTEXITCODE -ne 0) {
            Write-Output "[!] Quarantine triage failed for Topic $selectedTopic | Concept: $selectedConcept"
            Write-Output "    See the transcript for the exact mapping issues."
            if (-not $RepeatUntilClean) { throw "Quarantine triage failed" }
            continue
        }

        $repairArgs = @("-m", "certcoach.jobs.repair_explanations", "--max-questions", $RepairBatchSize)
        $repairArgs += @("--topic", $selectedTopic)
        $repairArgs += @("--concept", $selectedConcept)
        & $python @repairArgs
        if ($LASTEXITCODE -ne 0) {
            Write-Output "[!] Explanation repair batch failed for Topic $selectedTopic | Concept: $selectedConcept"
            Write-Output "    See the transcript and model-quality log for the exact quality issues."
            if (-not $RepeatUntilClean) { throw "Explanation repair batch failed" }
            continue
        }

        $seedArgs = @("-m", "certcoach.jobs.nightly_seed_questions", "--max-questions", $PopulationBatchSize)
        $seedArgs += @("--topic", $selectedTopic)
        $seedArgs += @("--concept", $selectedConcept)
        if ($ExtraEasy -gt 0) { $seedArgs += @("--extra-easy", $ExtraEasy) }
        if ($ExtraMedium -gt 0) { $seedArgs += @("--extra-medium", $ExtraMedium) }
        & $python @seedArgs
        if ($LASTEXITCODE -ne 0) {
            Write-Output "[!] Population batch failed for Topic $selectedTopic | Concept: $selectedConcept"
            Write-Output "    See the transcript and model-quality log for the exact quality issues."
            if (-not $RepeatUntilClean) { throw "Population batch failed" }
            continue
        }

        & $python -m certcoach.jobs.mark_scope_leaks --apply --topic $selectedTopic --concept $selectedConcept
        if ($LASTEXITCODE -ne 0) {
            Write-Output "[!] Post-population scope audit failed for Topic $selectedTopic | Concept: $selectedConcept"
            if (-not $RepeatUntilClean) { throw "Post-population scope audit failed" }
            continue
        }

        & $python -m certcoach.jobs.next_phase4_topic --topic $selectedTopic
        if ($LASTEXITCODE -ne 0) {
            Write-Output "[!] Final readiness report failed for Topic $selectedTopic | Concept: $selectedConcept"
            if (-not $RepeatUntilClean) { throw "Final readiness report failed" }
            continue
        }

        if (-not $RepeatUntilClean) {
            break
        }
        if ($hasExplicitConcept) {
            break
        }
        $Concept = ""
        if (-not $hasExplicitTopic) {
            $Topic = ""
        }
    }
}
finally {
    Stop-Transcript
}
