import csv
import getpass
from ovirtsdk4 import Connection

# Establecer los detalles de conexión
url = input('oVirt API URL: (e.g.: https://HOSTNAME:PORT/ovirt-engine/api): ')
username = input('Username: (e.g.: admin@internal): ')
password = getpass.getpass('Password: ')
ca_file = input('CA File: (e.g.: ./cert.pem): ')

# Crear una conexión al clúster oVirt
connection = Connection(
    url=url,
    username=username,
    password=password,
    ca_file=ca_file
)

# Obtener una referencia al servicio de máquinas virtuales
vms_service = connection.system_service().vms_service()

# Obtener una referencia al servicio de clústeres
clusters_service = connection.system_service().clusters_service()

# Recuperar la lista de máquinas virtuales
vms = vms_service.list()

# Ruta del archivo CSV de salida
csv_file = 'vms.csv'

# Abrir el archivo CSV en modo escritura
with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)

    # Escribir la cabecera del archivo CSV
    writer.writerow(['Nombre', 'Sistema Operativo', 'IP', 'CPU', 'RAM', 'VLAN', 'FQDN', 'Cluster', 'Uptime'])

    # Obtener y escribir la información de las máquinas virtuales en el archivo CSV
    for vm in vms:
        vm_service = vms_service.vm_service(vm.id)
        vm = vm_service.get(all_content=True)
        # Obtener una referencia al servicio de interfaces de red
        nics_service = vm_service.nics_service()
        rep_dev_service = vm_service.reported_devices_service()
        name = vm.name
        os = vm.os.type
        ip = ''
        vlan = ''
        fqdn = vm.fqdn if vm.fqdn else ''

        # Obtener las interfaces de red de la máquina virtual
        vm_nics = nics_service.list(search='vm.id={}'.format(vm.id))

        # Obtener las estadísticas de la máquina virtual
        vm_stats = vm_service.statistics_service().list(search='vm.id={}'.format(vm.id))

        if vm_nics:
            for nic in vm_nics:
                # Obtiene la red y número de vlan. Solo si tiene una tarjeta de red válida
                if nic.vnic_profile:
                    nic.vnic_profile = connection.follow_link(nic.vnic_profile)
                    vlan = connection.follow_link(nic.vnic_profile.network).vlan
                    if vlan:
                        vlan = vlan.id
                # Obtiene la dirección IP del primer dispositivo de red detectado
                if nic.reported_devices:
                    ip = nic.reported_devices[0].ips[0].address

        # Obtiene la cantidad total de CPUs
        cpu = vm.cpu.topology.cores * vm.cpu.topology.sockets
        # Calcula la memoria RAM en GiB
        ram = int(vm.memory/1024/1024/1024)

        # Obtener el nombre del clúster
        cluster = ''
        if vm.cluster:
            cluster = clusters_service.cluster_service(vm.cluster.id).get().name

        # Obtener el uptime de la máquina virtual
        uptime = ''
        for statistic in vm_stats:
            if statistic.name == 'elapsed.time':
                uptime = int(statistic.values[0].datum / 86400)
                break

        writer.writerow([name, os, ip, cpu, ram, vlan, fqdn, cluster, uptime])

# Cerrar la conexión
connection.close()
