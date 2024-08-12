# Define las opciones y los comandos correspondientes
$options = @{
    1 = "runserver 8080"
    2 = "makemigrations"  
    3 = "migrate"
    # Agrega más opciones según sea necesario
}

# Muestra las opciones disponibles
Write-Host "Seleccione una opcion:"
#foreach ($key in $options.Keys) {
    #Write-Host "$key. $($options[$key])"
#}
for ($i = 1; $i -le $options.Keys.Count; $i++) {
    Write-Host "$i. $($options[$i])"
}

# Solicita al usuario que ingrese un número de opción
$opcion = Read-Host "Ingrese el numero de la opcion deseada"

$opcion = [int]$opcion

# Verifica si la opción seleccionada está definida
if ($options.ContainsKey($opcion)) {    
    $comando = "python manage.py " + $options[$opcion]
    Write-Host "Ejecutando $comando"
    Invoke-Expression -Command $comando
} else {
    Write-Host "Opcion invalida."
}