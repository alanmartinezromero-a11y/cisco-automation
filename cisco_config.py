import netmiko
import tkinter as tk
from tkinter import messagebox
import datetime
import os

# Función para conectar al switch y aplicar configuraciones
def configure_switch(host, username, password, vlan_data, hostname):
    try:
        # Conectar al switch Cisco con ajustes de timeout
        device = {
            'device_type': 'cisco_ios',
            'host': host,
            'username': username,
            'password': password,
            'global_delay_factor': 2,
            'timeout': 30,
        }
        connection = netmiko.ConnectHandler(**device)
        print("Conexión exitosa. Enviando comandos...")

        # Configurar hostname
        config_commands = [f'hostname {hostname}']
        
        # Configurar VLANs
        for vlan_id, vlan_name in vlan_data.items():
            config_commands.extend([
                f'vlan {vlan_id}',
                f'name {vlan_name}',
                'exit'
            ])
        
        # Aplicar configuraciones e imprimir comandos para depuración
        print(f"Comandos enviados: {config_commands}")
        output = connection.send_config_set(config_commands)
        print(f"Salida del switch: {output}")
        
        # Guardar configuración en NVRAM
        connection.send_command('write memory')
        print("Configuración guardada en NVRAM.")
        
        # Realizar backup completo incluyendo VLANs
        backup_filename = f"backup_{hostname}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        # Usar 'show running-config' y 'show vlan brief' para capturar todo
        running_config = connection.send_command('show running-config')
        vlan_config = connection.send_command('show vlan brief')
        with open(backup_filename, 'w') as f:
            f.write("=== Running Configuration ===\n")
            f.write(running_config)
            f.write("\n=== VLAN Configuration ===\n")
            f.write(vlan_config)
        print(f"Backup guardado en {backup_filename}")
        
        # Validar configuración
        vlan_output = connection.send_command('show vlan brief')
        hostname_output = connection.send_command('show running-config | include hostname')
        print(f"Salida de 'show vlan brief': {vlan_output}")
        
        # Verificar VLANs requeridas (10, 20, 50)
        required_vlans = {"10": "VLAN_DATOS", "20": "VLAN_VOZ", "50": "VLAN_SEGURIDAD"}
        validation_errors = []
        for vlan_id, vlan_name in required_vlans.items():
            if vlan_id not in vlan_data or vlan_data.get(vlan_id) != vlan_name:
                validation_errors.append(f"VLAN {vlan_id} ({vlan_name}) no especificada o incorrecta.")
            elif vlan_id not in vlan_output or vlan_name not in vlan_output:
                validation_errors.append(f"VLAN {vlan_id} ({vlan_name}) no configurada correctamente en el switch.")
        
        # Verificar hostname
        if f"hostname {hostname}" not in hostname_output:
            validation_errors.append(f"Hostname {hostname} no configurado correctamente.")
        
        # Desconectar
        connection.disconnect()
        
        # Mostrar resultado de validación
        if validation_errors:
            messagebox.showerror("Error de Validación", "\n".join(validation_errors))
            return False
        else:
            messagebox.showinfo("Éxito", f"Configuración aplicada y guardada. Backup en {backup_filename}")
            return True
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar o configurar: {str(e)}")
        print(f"Error detallado: {str(e)}")
        return False

# Función para obtener datos del frontend y ejecutar la configuración
def apply_config():
    host = entry_host.get()
    username = entry_username.get()
    password = entry_password.get()
    hostname = entry_hostname.get()
    
    # Obtener VLANs desde las entradas del frontend
    vlan_data = {}
    try:
        # Validar que todas las VLANs requeridas (10, 20, 50) estén completas
        vlan10_id = entry_vlan10_id.get()
        vlan10_name = entry_vlan10_name.get()
        vlan20_id = entry_vlan20_id.get()
        vlan20_name = entry_vlan20_name.get()
        vlan50_id = entry_vlan50_id.get()
        vlan50_name = entry_vlan50_name.get()

        # Verificar que los campos requeridos no estén vacíos
        if not (vlan10_id and vlan10_name and vlan20_id and vlan20_name and vlan50_id and vlan50_name):
            messagebox.showerror("Error", "Debes especificar ID y nombre para todas las VLANs (10, 20, 50).")
            return
        # Verificar que los IDs sean números y coincidan con los requeridos
        if vlan10_id != "10" or vlan20_id != "20" or vlan50_id != "50":
            messagebox.showerror("Error", "Los IDs de VLAN deben ser 10, 20 y 50 respectivamente.")
            return
        # Agregar al diccionario de VLANs
        vlan_data[vlan10_id] = vlan10_name
        vlan_data[vlan20_id] = vlan20_name
        vlan_data[vlan50_id] = vlan50_name
    except ValueError:
        messagebox.showerror("Error", "Los IDs de VLAN deben ser números válidos.")
        return
    
    # Ejecutar configuración solo si la validación inicial pasa
    if configure_switch(host, username, password, vlan_data, hostname):
        pass  # La validación posterior en configure_switch manejará el resto

# Crear frontend con Tkinter
root = tk.Tk()
root.title("Configurador de Switch Cisco")
root.geometry("400x400")

# Etiquetas y campos de entrada
tk.Label(root, text="IP del Switch:").pack(pady=5)
entry_host = tk.Entry(root)
entry_host.pack()

tk.Label(root, text="Usuario:").pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack()

tk.Label(root, text="Contraseña:").pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack()

tk.Label(root, text="Hostname:").pack(pady=5)
entry_hostname = tk.Entry(root)
entry_hostname.insert(0, "SWITCH_AUTOMATIZADO")
entry_hostname.pack()

# Entradas para VLAN 10
tk.Label(root, text="VLAN 10 - ID:").pack(pady=5)
entry_vlan10_id = tk.Entry(root)
entry_vlan10_id.insert(0, "10")
entry_vlan10_id.pack()

tk.Label(root, text="VLAN 10 - Nombre:").pack(pady=5)
entry_vlan10_name = tk.Entry(root)
entry_vlan10_name.insert(0, "VLAN_DATOS")
entry_vlan10_name.pack()

# Entradas para VLAN 20
tk.Label(root, text="VLAN 20 - ID:").pack(pady=5)
entry_vlan20_id = tk.Entry(root)
entry_vlan20_id.insert(0, "20")
entry_vlan20_id.pack()

tk.Label(root, text="VLAN 20 - Nombre:").pack(pady=5)
entry_vlan20_name = tk.Entry(root)
entry_vlan20_name.insert(0, "VLAN_VOZ")
entry_vlan20_name.pack()

# Entradas para VLAN 50
tk.Label(root, text="VLAN 50 - ID:").pack(pady=5)
entry_vlan50_id = tk.Entry(root)
entry_vlan50_id.insert(0, "50")
entry_vlan50_id.pack()

tk.Label(root, text="VLAN 50 - Nombre:").pack(pady=5)
entry_vlan50_name = tk.Entry(root)
entry_vlan50_name.insert(0, "VLAN_SEGURIDAD")
entry_vlan50_name.pack()

# Botón para aplicar configuración
tk.Button(root, text="Aplicar Configuración", command=apply_config).pack(pady=20)

# Iniciar la interfaz
root.mainloop()