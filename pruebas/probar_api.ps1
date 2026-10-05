# Pruebas de la API con curl (ES3)
# Uso, con el servidor corriendo (python manage.py runserver) en otra terminal:
#   powershell -ExecutionPolicy Bypass -File pruebas\probar_api.ps1
# La contraseña se pide oculta y los tokens quedan truncados en pruebas\resultados_curl.txt.
# Si lo ejecutas dos veces en menos de un minuto, /api/token/ responde 429 (límite de intentos).

param(
    [string]$Base = "http://127.0.0.1:8000",
    [string]$Prefijo = "usuario_"
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$salida = Join-Path $PSScriptRoot "resultados_curl.txt"
$tmp = Join-Path $env:TEMP "es3_cuerpo.json"
$utf8 = New-Object Text.UTF8Encoding $false

$seguro = Read-Host "Contraseña de los usuarios $($Prefijo)* (no se muestra)" -AsSecureString
$clave = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($seguro))

$log = New-Object System.Collections.Generic.List[string]
$resumen = New-Object System.Collections.Generic.List[string]
$script:n = 0

function Truncar([string]$texto) {
    # Un JWT tiene tres partes separadas por puntos y empieza con "eyJ".
    [regex]::Replace($texto, 'eyJ[\w-]+\.[\w-]+\.[\w-]+', { param($m) $m.Value.Substring(0, 12) + '...' })
}

function Seccion([string]$titulo) {
    $log.Add(""); $log.Add("=" * 70); $log.Add($titulo); $log.Add("=" * 70)
}

# Ejecuta una petición con curl, la registra y devuelve el cuerpo de la respuesta.
function Probar {
    param(
        [string]$Titulo, [int]$Esperado, [string]$Metodo, [string]$Ruta,
        [string]$Auth = "", [string]$Cuerpo = "", [string]$CuerpoVisible = ""
    )
    $script:n++
    $a = @("-s", "-X", $Metodo, "-w", '\nHTTP %{http_code}')
    $cmd = "curl -X $Metodo"
    if ($Auth) {
        $a += @("-H", "Authorization: $Auth")
        $cmd += " -H `"Authorization: $(Truncar $Auth)`""
    }
    if ($Cuerpo) {
        [IO.File]::WriteAllText($tmp, $Cuerpo, $utf8)
        $a += @("-H", "Content-Type: application/json", "--data-binary", "@$tmp")
        if (-not $CuerpoVisible) { $CuerpoVisible = $Cuerpo }
        $cmd += " -H `"Content-Type: application/json`" -d '$(Truncar $CuerpoVisible)'"
    }
    $a += "$Base$Ruta"
    $cmd += " $Base$Ruta"

    $lineas = @(& curl.exe @a)
    $codigo = [int](($lineas[-1]) -replace 'HTTP ', '')
    $cuerpoResp = ($lineas[0..($lineas.Count - 2)] -join "`n")
    $estado = if ($codigo -eq $Esperado) { "OK" } else { "FALLA" }

    $log.Add("")
    $log.Add("[$($script:n)] $Titulo")
    $log.Add("`$ $cmd")
    $log.Add("-> HTTP $codigo (esperado $Esperado) $estado")
    if ($cuerpoResp) { $log.Add((Truncar $cuerpoResp)) } else { $log.Add("(sin cuerpo)") }
    $resumen.Add(("{0,-4} {1,-6} {2,3}  {3}" -f "[$($script:n)]", $estado, $codigo, $Titulo))
    Write-Host ("[{0}] {1} {2} {3}" -f $script:n, $estado, $codigo, $Titulo)
    return $cuerpoResp
}

function PedirToken([string]$rol) {
    $u = "$Prefijo$rol"
    $json = @{ username = $u; password = $clave } | ConvertTo-Json -Compress
    $visible = @{ username = $u; password = "***" } | ConvertTo-Json -Compress
    $r = Probar "Token para $u" 200 POST "/api/token/" -Cuerpo $json -CuerpoVisible $visible
    try { return ($r | ConvertFrom-Json) } catch { return $null }
}

$log.Add("Pruebas de la API ES3 con curl - $(Get-Date -Format 'yyyy-MM-dd HH:mm')")
$log.Add("Servidor: $Base")
$log.Add("Los tokens aparecen truncados (12 caracteres + ...) y la contraseña como ***.")

# ---------------------------------------------------------------- tokens
Seccion "1. AUTENTICACION JWT"
$tAdmin = PedirToken "admin"
$tNormal = PedirToken "normal"
$tViewer = PedirToken "viewer"
if (-not ($tAdmin.access -and $tNormal.access -and $tViewer.access)) {
    Remove-Item $tmp -ErrorAction SilentlyContinue
    Write-Host "No se obtuvieron los tres tokens: revisa la contraseña, que el servidor esté corriendo, o espera 1 minuto (límite de intentos)."
    exit 1
}
$admin = "Bearer $($tAdmin.access)"
$normal = "Bearer $($tNormal.access)"
$viewer = "Bearer $($tViewer.access)"

Probar "GET lista SIN token" 401 GET "/api/pacientes/" | Out-Null
Probar "GET lista con prefijo 'Token' en vez de 'Bearer'" 401 GET "/api/pacientes/" -Auth "Token $($tAdmin.access)" | Out-Null
Probar "GET lista con token falso" 401 GET "/api/pacientes/" -Auth "Bearer abc.def.ghi" | Out-Null

# ---------------------------------------------------------------- CRUD
Seccion "2. CRUD CORRECTO (usuario normal)"
Probar "GET lista paginada" 200 GET "/api/pacientes/" -Auth $normal | Out-Null
$creado = Probar "POST crear (manda gravedad 'Verde': debe ignorarse)" 201 POST "/api/pacientes/" -Auth $normal `
    -Cuerpo '{"nombre": "Paciente prueba API", "dificultad_respiracion": "No", "dolor": 7, "gravedad": "Verde"}'
$id = ($creado | ConvertFrom-Json).id
Probar "GET detalle del creado" 200 GET "/api/pacientes/$id/" -Auth $normal | Out-Null
Probar "PATCH dificultad_respiracion = Sí (gravedad pasa a Rojo)" 200 PATCH "/api/pacientes/$id/" -Auth $normal `
    -Cuerpo '{"dificultad_respiracion": "Sí"}' | Out-Null
Probar "PUT reemplazo completo" 200 PUT "/api/pacientes/$id/" -Auth $normal `
    -Cuerpo '{"nombre": "Paciente prueba API", "dificultad_respiracion": "No", "dolor": 2}' | Out-Null
Probar "GET filtro ?gravedad=verde" 200 GET "/api/pacientes/?gravedad=verde" -Auth $normal | Out-Null

# ---------------------------------------------------------------- errores
Seccion "3. ERRORES Y VALIDACIONES"
Probar "POST dolor negativo" 400 POST "/api/pacientes/" -Auth $normal `
    -Cuerpo '{"nombre": "Ana", "dificultad_respiracion": "No", "dolor": -1}' | Out-Null
Probar "POST varios campos malos a la vez" 400 POST "/api/pacientes/" -Auth $normal `
    -Cuerpo '{"nombre": "", "dificultad_respiracion": "Talvez", "dolor": "mucho"}' | Out-Null
Probar "POST JSON mal formado" 400 POST "/api/pacientes/" -Auth $normal -Cuerpo '{nombre: Ana' | Out-Null
Probar "PUT incompleto" 400 PUT "/api/pacientes/$id/" -Auth $normal -Cuerpo '{"nombre": "Ana"}' | Out-Null
Probar "GET filtro con gravedad inexistente" 400 GET "/api/pacientes/?gravedad=Azul" -Auth $normal | Out-Null
Probar "GET id que no existe" 404 GET "/api/pacientes/99999/" -Auth $normal | Out-Null
Probar "GET página que no existe" 404 GET "/api/pacientes/?page=999" -Auth $normal | Out-Null
Probar "POST sobre un detalle (verbo no permitido)" 405 POST "/api/pacientes/$id/" -Auth $normal -Cuerpo '{}' | Out-Null

# ---------------------------------------------------------------- permisos
Seccion "4. PERMISOS POR ROL"
Probar "viewer GET lista" 200 GET "/api/pacientes/" -Auth $viewer | Out-Null
Probar "viewer POST" 403 POST "/api/pacientes/" -Auth $viewer `
    -Cuerpo '{"nombre": "Intruso", "dificultad_respiracion": "No", "dolor": 1}' | Out-Null
Probar "viewer PATCH" 403 PATCH "/api/pacientes/$id/" -Auth $viewer -Cuerpo '{"dolor": 9}' | Out-Null
Probar "normal DELETE" 403 DELETE "/api/pacientes/$id/" -Auth $normal | Out-Null
Probar "admin DELETE (borrado lógico)" 204 DELETE "/api/pacientes/$id/" -Auth $admin | Out-Null
Probar "GET del paciente borrado" 404 GET "/api/pacientes/$id/" -Auth $admin | Out-Null

# ---------------------------------------------------------------- refresco
Seccion "5. REFRESCO DEL TOKEN"
$refrescoJson = @{ refresh = $tViewer.refresh } | ConvertTo-Json -Compress
Probar "Refresh válido entrega un access nuevo" 200 POST "/api/token/refresh/" -Cuerpo $refrescoJson | Out-Null
Probar "Refresh inválido" 401 POST "/api/token/refresh/" -Cuerpo '{"refresh": "basura"}' | Out-Null

# ---------------------------------------------------------------- fuerza bruta
Seccion "6. LIMITE DE INTENTOS EN /api/token/ (5 por minuto; ya se usaron 3)"
$malo = @{ username = "$($Prefijo)admin"; password = "clave-incorrecta" } | ConvertTo-Json -Compress
Probar "Clave incorrecta (intento 4)" 401 POST "/api/token/" -Cuerpo $malo | Out-Null
Probar "Clave incorrecta (intento 5)" 401 POST "/api/token/" -Cuerpo $malo | Out-Null
Probar "Clave incorrecta (intento 6: bloqueado)" 429 POST "/api/token/" -Cuerpo $malo | Out-Null

Remove-Item $tmp -ErrorAction SilentlyContinue

$fallas = @($resumen | Where-Object { $_ -match 'FALLA' }).Count
Seccion "RESUMEN: $($script:n - $fallas) de $($script:n) pruebas con el código esperado"
$resumen | ForEach-Object { $log.Add($_) }

[IO.File]::WriteAllLines($salida, $log, $utf8)
Write-Host ""
Write-Host "$($script:n - $fallas) de $($script:n) OK. Resultados en $salida"
