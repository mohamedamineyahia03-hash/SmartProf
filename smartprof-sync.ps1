$ErrorActionPreference = "Stop"

$Repo = "C:\Users\NITRO\Desktop\SmartProf"
$Log = Join-Path $Repo ".smartprof-sync.log"

Set-Location $Repo

function Log($Message) {
    Add-Content -Path $Log -Value "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | $Message"
}

try {
    Log "SYNC START"

    # Récupérer l'état distant sans modifier les fichiers locaux
    git fetch origin

    # Vérifier s'il existe des modifications locales
    $status = git status --porcelain

    if ($status) {
        git add data web server mobile

        $statusAfterAdd = git status --porcelain

        if ($statusAfterAdd) {
            $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
            git commit -m "auto: SmartProf sync $timestamp"
            Log "LOCAL COMMIT CREATED"
        }
    }

    # Synchroniser avec GitHub sans force-push
    git pull --rebase origin main

    # Envoyer les modifications locales
    git push origin main

    Log "SYNC SUCCESS"
}
catch {
    Log "SYNC ERROR: $($_.Exception.Message)"
}
