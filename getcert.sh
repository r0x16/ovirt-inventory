#!/bin/bash
read -p "oVirt hostname: " hostname
read -p "oVirt port (default: 443):" -e port

port=${port:-443}

echo "Obteniendo certificado desde la url [$hostname:$port]..."

openssl s_client -showcerts -connect $hostname:$port </dev/null 2>/dev/null | openssl x509 -outform PEM > cert.pem

echo "Finalizado, verifique archivo 'cert.pem'"