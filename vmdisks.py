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

# Obtener una referencia al servicio de máquinas virtuales
vms_service = connection.system_service().vms_service()

# Obtener una referencia al servicio de clústeres
clusters_service = connection.system_service().clusters_service()

# clusters = clusters_service.list()
# print(clusters[0].__dict__)
# quit()

# Recuperar la lista de máquinas virtuales
vms = vms_service.list()

# Imprimir la información de las máquinas virtuales
""" for vm in vms:
    attachments = connection.follow_link(vm.disk_attachments)
    for attachment in attachments:
        disk = connection.follow_link(attachment.disk)
        stdom = connection.follow_link(disk.storage_domains[0])
        print(stdom.__dict__)

quit() """

# Ruta del archivo CSV de salida
csv_file = 'vms.csv'

# Abrir el archivo CSV en modo escritura
with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)

    # Escribir la cabecera del archivo CSV
    writer.writerow(['Nombre', 'Sistema Operativo', 'IP', 'CPU', 'RAM', 'VLAN', 'FQDN', 'Cluster', 'Uptime', 'Host', 'Disco', 'Total', 'Utilizado', 'Domain'])

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
                if nic.reported_devices and nic.reported_devices[0].ips:
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
        
        # Obtener el nombre del host
        host = ''
        if vm.host:
            host = connection.follow_link(vm.host).name

        attachments = connection.follow_link(vm.disk_attachments)
        for attachment in attachments:
            disk = connection.follow_link(attachment.disk)
            stdom = connection.follow_link(disk.storage_domains[0])
            totalsize = int(disk.total_size / 1024 / 1024 /1024)
            actualsize = int(disk.actual_size / 1024 / 1024 /1024)
            writer.writerow([name, os, ip, cpu, ram, vlan, fqdn, cluster, uptime, host, disk.name, totalsize, actualsize, stdom.name])

        

# Cerrar la conexión
connection.close()
