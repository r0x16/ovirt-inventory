import csv
import getpass
import json
from ovirtsdk4 import Connection

# Establecer los detalles de conexión
# Cargar la configuración desde un archivo JSON
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    ovirt_config = config['ovirt']

# Crear una conexión al clúster oVirt
connection = Connection(
    url=ovirt_config['url'],
    username=ovirt_config['username'],
    password=ovirt_config['password'],
    ca_file=ovirt_config['ca_file']
)

# El WWNN del LUN que estás buscando, formateado como aparece en el lun.id
wwnn_deseado = '3' + '604f352100e75c5683dd450a0000001a'  # Asegúrate de agregar el '3' al inicio del WWNN

# Obtener el servicio del sistema
system_service = connection.system_service()

# Obtener la lista de hosts
hosts_service = system_service.hosts_service()
hosts = hosts_service.list()

# Recorrer cada host y verificar los LUNs
for host in hosts:
    host_service = hosts_service.host_service(host.id)
    storage_service = host_service.storage_service()
    storages = storage_service.list()

    # Dado que no hay un método directo para listar LUNs a través de storage_service en este contexto,
    # necesitaremos ajustar este enfoque. El ejemplo proporcionado era más un esqueleto y puede que no funcione como se esperaba.
    # En su lugar, consideraremos un enfoque genérico para ilustrar cómo podrías proceder, pero ten en cuenta que
    # necesitarás acceder a los detalles de los LUNs de una manera que se ajuste a tu configuración específica.

    # Este bloque de código es más bien ilustrativo, ya que acceder directamente a las LUNs de esta manera puede no ser posible
    # sin utilizar alguna extensión específica o comando adicional que te permita listar y filtrar los LUNs en oVirt.

    # Imaginando que podemos acceder a los LUNs directamente (ajusta esto según tu entorno real)
    present = False
    for lun in storages: # Este acceso directo es hipotético y probablemente necesites ajustarlo
        if lun.id.startswith(wwnn_deseado):
            present = True
            break  # Encontrado el LUN deseado, no es necesario seguir buscando en este host
    
    if present:
        print(f'{host.name}: OK')
    else:
        print(f'{host.name}: Not Found')

# Cerrar conexión
connection.close()
