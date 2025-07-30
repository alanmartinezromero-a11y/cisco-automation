# Plan de Automatización de VPN IPSec entre Fortigate y Palo Alto

## Objetivo
Desarrollar un plan para automatizar la configuración de una VPN IPSec site-to-site que conecte un firewall Fortigate y un firewall Palo Alto, garantizando una comunicación segura entre dos redes locales a través de Internet. El plan incluirá los parámetros necesarios y un enfoque para su automatización.

## Topología y Parámetros de la VPN

### Direcciones IP WAN
- **Fortigate**: Interfaz WAN en `192.168.1.1`
- **Palo Alto**: Interfaz WAN en `192.168.2.1`

### Redes Locales
- **Fortigate**: Red local protegida `10.1.1.0/24` (por ejemplo, una red de oficinas)
- **Palo Alto**: Red local protegida `10.2.2.0/24` (por ejemplo, una sucursal)

### Red de Túnel
- **Subred de túnel**: `169.255.1.0/30`
  - **Fortigate (extremo local)**: `169.255.1.1`
  - **Palo Alto (extremo remoto)**: `169.255.1.2`

### Propuestas de Phase 1
- **Versión IKE**: IKEv2
- **Algoritmo de cifrado**: AES-256
- **Algoritmo de autenticación**: SHA-256
- **Grupo Diffie-Hellman**: Grupo 14
- **Clave precompartida**: `clave_secreta_2025`
- **Lifetime**: 86,400 segundos (24 horas)

### Propuestas de Phase 2
- **Algoritmo de cifrado**: AES-128
- **Algoritmo de autenticación**: SHA-1
- **Perfect Forward Secrecy (PFS)**: Grupo 14
- **Lifetime**: 3,600 segundos (1 hora)

## Plan de Automatización

### Herramientas Propuestas
- **Lenguaje**: Python, por su simplicidad y compatibilidad con bibliotecas de automatización.
- **Fortigate**: Uso de la **FortiOS API** (REST API) o comandos CLI a través de la librería `paramiko` o `netmiko` para configurar la VPN.
- **Palo Alto**: Uso de la **PAN-OS XML API** o comandos CLI mediante `netmiko` para configurar el firewall.
- **Control de versiones**: Git para gestionar el script y este plan en el repositorio.

### Pasos de Automatización
1. **Conexión a dispositivos**:
   - Establecer conexión segura (SSH o API) al Fortigate y al Palo Alto usando credenciales predefinidas.
   - Verificar la accesibilidad de las interfaces WAN (`192.168.1.1` y `192.168.2.1`).

2. **Configuración de Phase 1**:
   - **Fortigate**: Crear un perfil IKE usando la API o CLI con los parámetros de Phase 1 (AES-256, SHA-256, Grupo 14, clave precompartida).
   - **Palo Alto**: Configurar un IKE Gateway con los mismos parámetros usando la API XML o CLI.

3. **Configuración de Phase 2**:
   - **Fortigate**: Definir un túnel IPsec con las redes locales (`10.1.1.0/24` y `10.2.2.0/24`) y la subred de túnel (`169.255.1.0/30`).
   - **Palo Alto**: Configurar un túnel IPsec con Proxy IDs que especifiquen las redes locales y la subred de túnel.

4. **Rutas Estáticas**:
   - Añadir rutas en ambos dispositivos para dirigir el tráfico de las redes remotas a través del túnel IPsec.
   - Ejemplo en Fortigate: `route 10.2.2.0 255.255.255.0 gateway 169.255.1.2`
   - Ejemplo en Palo Alto: `set network virtual-router default route 10.1.1.0/24 nexthop 169.255.1.1`

5. **Validación**:
   - Ejecutar comandos para verificar el estado del túnel:
     - Fortigate: `get vpn ipsec tunnel list`
     - Palo Alto: `show vpn ipsec-sa`
   - Realizar un ping entre las redes locales (`10.1.1.10` a `10.2.2.10`) para confirmar conectividad.
   - Mostrar alertas si el túnel no se establece (por ejemplo, diferencias en parámetros).

6. **Backup**:
   - Guardar la configuración de ambos dispositivos en archivos locales con timestamp (ejemplo: `fortigate_config_20250730.txt`).
   - Opcional: Subir los backups a un servidor remoto usando SCP o FTP.

### Consideraciones de Viabilidad
- **Entornos de prueba**: Usar FortiOS VM (disponible en el sitio de Fortinet) y un emulador de Palo Alto (como PAN-OS en AWS o GNS3 si compatible).
- **Dependencias**: Instalar Python con `paramiko`, `netmiko` y las APIs respectivas (`fortiosapi` para Fortigate, `pan-python` para Palo Alto).
- **Escalabilidad**: El script puede adaptarse para múltiples pares de VPN ajustando los parámetros en un archivo de configuración (por ejemplo, JSON).

## Notas
- Se recomienda probar la configuración en un entorno aislado antes de aplicarla en producción.
- Documentar cualquier error (por ejemplo, incompatibilidad de Phase 1/2) para ajustes futuros.
- Este plan asume que ambos dispositivos tienen acceso a Internet y que las interfaces WAN son públicas o accesibles a través de NAT.