#!/bin/bash

# Función para verificar si un paquete está instalado
is_package_installed() {
    dpkg -s "$1" >/dev/null 2>&1
}

# Verificar si curl, libcurl, libxml2-dev y libssl-dev están instalados
if ! is_package_installed "curl" || ! is_package_installed "libcurl4-openssl-dev" || ! is_package_installed "libxml2-dev" || ! is_package_installed "libssl-dev"; then
    echo "Instalando curl, libcurl, libxml2-dev y libssl-dev..."
    apt-get update
    apt-get install -y curl libcurl4-openssl-dev libxml2-dev libssl-dev
else
    echo "curl, libcurl, libxml2-dev y libssl-dev ya están instalados."
fi

# Verificar si pip está instalado
if ! command -v pip3 &>/dev/null; then
    echo "Instalando pip..."
    apt-get install -y python3-pip
else
    echo "pip ya está instalado."
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
