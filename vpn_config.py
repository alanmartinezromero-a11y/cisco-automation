import netmiko
from netmiko import ConnectHandler

# Definición de dispositivos
fortigate = {
    'device_type': 'fortinet',
    'host': '192.168.1.1',
    'username': 'admin',
    'password': 'fortinet',
    'port': 22,
}

palo_alto = {
    'device_type': 'paloalto_panos',
    'host': '192.168.2.1',
    'username': 'admin',
    'password': 'paloalto',
    'port': 22,
}

# Comandos para Fortigate
fortigate_commands = [
    'config vpn ipsec phase1-interface',
    'edit "to-paloalto"',
    'set type static',
    'set interface "wan1"',
    'set remote-gw 192.168.2.1',
    'set psksecret clave_secreta_2025',
    'set proposal aes256-sha256',
    'set dhgrp 14',
    'set authmethod psk',
    'next',
    'end',
    'config vpn ipsec phase2-interface',
    'edit "to-paloalto-p2"',
    'set phase1name "to-paloalto"',
    'set proposal aes128-sha1',
    'set dhgrp 14',
    'set pfs enable',
    'next',
    'end',
    'config router static',
    'edit 1',
    'set dst 10.2.2.0 255.255.255.0',
    'set gateway 169.255.1.2',
    'next',
    'end'
]

# Comandos para Palo Alto
palo_alto_commands = [
    'configure',
    'set network interface tunnel units tunnel.1 ip 169.255.1.2/30',
    'set network ike gateway to-fortigate',
    'set network ike gateway to-fortigate interface ethernet1/1',
    'set network ike gateway to-fortigate peer-ip-address 192.168.1.1',
    'set network ike gateway to-fortigate pre-shared-key clave_secreta_2025',
    'set network ike gateway to-fortigate protocol ikev2',
    'set network ike gateway to-fortigate dh-group group14',
    'set network ike gateway to-fortigate encryption aes-256-cbc',
    'set network ike gateway to-fortigate hash sha256',
    'set network ike gateway to-fortigate lifetime 86400',
    'set network tunnel ipsec to-fortigate phase1-gateway to-fortigate',
    'set network tunnel ipsec to-fortigate ike-gateway to-fortigate',
    'set network tunnel ipsec to-fortigate ipsec-crypto-profile high',
    'set network tunnel ipsec to-fortigate proxy-id local-ip 10.2.2.0',
    'set network tunnel ipsec to-fortigate proxy-id remote-ip 10.1.1.0',
    'set network virtual-router default static-route to-fortigate destination 10.1.1.0/24 nexthop 169.255.1.1',
    'commit'
]

# Función para conectar y configurar
def configure_device(device, commands):
    try:
        connection = ConnectHandler(**device)
        print(f"Conectado a {device['host']}")
        output = connection.send_config_set(commands)
        print(f"Configuración aplicada:\n{output}")
        connection.disconnect()
        print(f"Desconectado de {device['host']}")
    except Exception as e:
        print(f"Error al configurar {device['host']}: {str(e)}")

# Ejecutar configuraciones
if __name__ == "__main__":
    print("Configurando Fortigate...")
    configure_device(fortigate, fortigate_commands)
    print("Configurando Palo Alto...")
    configure_device(palo_alto, palo_alto_commands)
    print("Configuración completada. Verifica los túneles con 'get vpn ipsec tunnel list' (Fortigate) o 'show vpn ipsec-sa' (Palo Alto).")
