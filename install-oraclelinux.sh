#!/bin/bash

# Función para verificar si un paquete está instalado
is_package_installed() {
    rpm -q "$1" >/dev/null 2>&1
}

# Verificar si las dependencias están instaladas
dependencies=(
    curl
    libcurl-devel
    libxml2-devel
    openssl
    openssl-devel
    python3-devel
    gcc
)

not_installed=()

for dependency in "${dependencies[@]}"; do
    if ! is_package_installed "$dependency"; then
        not_installed+=("$dependency")
    fi
done

# Instalar las dependencias faltantes
if [ ${#not_installed[@]} -gt 0 ]; then
    echo "Instalando dependencias faltantes: ${not_installed[*]}..."
    dnf install -y "${not_installed[@]}"
else
    echo "Todas las dependencias ya están instaladas."
fi

# Dependencias de Python
python_dependencies=(
    ovirt-engine-sdk-python==4.4.2
)

# Verificar si las dependencias de Python están instaladas
for dependency in "${python_dependencies[@]}"; do
    package=$(echo "$dependency" | awk -F'==' '{print $1}')
    version=$(echo "$dependency" | awk -F'==' '{print $2}')
    if python3 -c "import $package" >/dev/null 2>&1; then
        installed_version=$(python3 -c "import $package; print($package.__version__)")
        if [ "$installed_version" = "$version" ]; then
            echo "$dependency ya está instalado."
        else
            echo "Actualizando $dependency..."
            pip3 install --upgrade "$dependency"
        fi
    else
        echo "Instalando $dependency..."
        pip3 install "$dependency"
    fi
done
