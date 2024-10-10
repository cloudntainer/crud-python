$envFilePath = ".\.env"

if (Test-Path $envFilePath) {
    Write-Host "Looking for .env file at path: $envFilePath"
    Write-Host "Found .env file, reading content..."

    $lines = Get-Content $envFilePath
    $variables = @{}

    foreach ($line in $lines) {
        # Verifica si la línea está en el formato correcto
        if ($line -notmatch '^\s*#' -and $line -match '^export\s+([^=\s]+)=([^=\s]+)') {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim()

            # Reemplazar variables de entorno
            foreach ($var in $variables.Keys) {
                $value = $value -replace "\$\{$var\}", $variables[$var]
            }

            # Almacenar la variable de entorno
            [System.Environment]::SetEnvironmentVariable($key, $value, [System.EnvironmentVariableTarget]::User)
            $variables[$key] = $value
        }
    }

    # Imprimir las variables de entorno establecidas
    Write-Host "Environment variables set:"
    foreach ($key in $variables.Keys) {
        Write-Host "$key = $($variables[$key])"  # Cambia aquí para imprimir el valor correcto
    }
} else {
    Write-Host "The .env file is not found in the directory."
}
