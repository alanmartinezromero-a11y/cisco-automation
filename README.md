# Automatización de Switch Cisco

**Autor: Alan Martinez Romero**  
**Fecha: 30 de julio de 2025**

Este proyecto automatiza la configuración de un switch Cisco, incluyendo VLANs y hostname, usando Python con Netmiko y Tkinter para el frontend.

## Requisitos
- Python 3.x
- Librerías: `netmiko`, `tkinter` (instalar con `pip install netmiko tk`)
- Switch Cisco con SSH habilitado (probado en un switch real con IP 192.168.1.77)
- Git y cuenta en GitHub

## Instrucciones
1. Clona el repositorio: `git clone https://github.com/alanmartinezromero-a11y/cisco-automation.git`
2. Instala las dependencias: `pip install netmiko tk`
3. Configura un switch Cisco con SSH (usuario: Alan, contraseña: cisco).
4. Ejecuta el script: `python cisco_config.py`
5. Ingresa la IP del switch, usuario, contraseña y hostname en la interfaz gráfica.
6. Especifica los IDs y nombres de las VLANs (deben ser VLAN 10 "VLAN_DATOS", VLAN 20 "VLAN_VOZ", VLAN 50 "VLAN_SEGURIDAD"). Todos los campos son obligatorios.
7. Haz clic en "Aplicar Configuración".

## Funcionalidades
- Configura VLAN 10 ("VLAN_DATOS"), VLAN 20 ("VLAN_VOZ") y VLAN 50 ("VLAN_SEGURIDAD").
- Cambia el hostname a "SWITCH_AUTOMATIZADO".
- Guarda la configuración en NVRAM.
- Crea un backup de la configuración en un archivo local, incluyendo las VLANs.
- Valida la configuración y muestra alertas si hay errores.

## Evidencia
- Capturas de pantalla en la carpeta `/evidencia`:
  - Frontend con mensaje de éxito.
  - CLI del switch con `show vlan brief`.
  - Archivo de backup generado con VLANs.
- Video comprimido en `/evidencia/cisco_automation.mp4` mostrando la ejecución.

## Simulación
- Revisa el archivo `switch_simulation.pkt` es una simulación en Packet Tracer con una computadora conectada a un switch configurado con ssh.

## Notas
- Asegúrate de que el switch esté accesible vía SSH.
- Usa las credenciales proporcionadas para pruebas.
- Proyecto realizado para el Challenge Networking de Mercado Libre.
- Usé un switch real C9200L-24P-4G-E con la ultima imagen recomendada por cisco, con IP 192.168.1.77 para las pruebas.
- Simular Fortigate y Palo Alto es un complicado, las imágenes para GNS3 son difíciles de conseguir mejor recomiendo usar trials gratis (FortiOS 15 días en support.fortinet.com, PAN-OS en paloaltonetworks.com) en VirtualBox.