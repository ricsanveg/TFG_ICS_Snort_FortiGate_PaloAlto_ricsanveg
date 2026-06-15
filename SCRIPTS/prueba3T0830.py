from scapy.all import *

hmi = "192.168.70.150"
mitm = "192.168.70.200"
plc = "192.168.70.129"

pkts = []

# =====================================================
# HMI <-> MITM
# =====================================================

pkts.append(IP(src=hmi,dst=mitm)/TCP(sport=50000,dport=502,flags="S",seq=100))
pkts.append(IP(src=mitm,dst=hmi)/TCP(sport=502,dport=50000,flags="SA",seq=200,ack=101))
pkts.append(IP(src=hmi,dst=mitm)/TCP(sport=50000,dport=502,flags="A",seq=101,ack=201))

# FC3 Read Holding Registers
query = bytes.fromhex(
    "000100000006010300000001"
)

pkts.append(
    IP(src=hmi,dst=mitm)/
    TCP(sport=50000,dport=502,flags="PA",seq=101,ack=201)/
    Raw(query)
)

# =====================================================
# MITM <-> PLC
# =====================================================

pkts.append(IP(src=mitm,dst=plc)/TCP(sport=50001,dport=502,flags="S",seq=300))
pkts.append(IP(src=plc,dst=mitm)/TCP(sport=502,dport=50001,flags="SA",seq=400,ack=301))
pkts.append(IP(src=mitm,dst=plc)/TCP(sport=50001,dport=502,flags="A",seq=301,ack=401))

pkts.append(
    IP(src=mitm,dst=plc)/
    TCP(sport=50001,dport=502,flags="PA",seq=301,ack=401)/
    Raw(query)
)

# =====================================================
# PLC responde valor = 100 (0x0064)
# =====================================================

response_real = bytes.fromhex(
    "0001000000050103020064"
)

pkts.append(
    IP(src=plc,dst=mitm)/
    TCP(sport=502,dport=50001,flags="PA",seq=401,ack=313)/
    Raw(response_real)
)

# =====================================================
# MITM modifica valor a 50 (0x0032)
# =====================================================

response_modified = bytes.fromhex(
    "0001000000050103020032"
)

pkts.append(
    IP(src=mitm,dst=hmi)/
    TCP(sport=502,dport=50000,flags="PA",seq=201,ack=113)/
    Raw(response_modified)
)

# =====================================================
# Cierre HMI <-> MITM
# =====================================================

pkts.append(
    IP(src=hmi,dst=mitm)/
    TCP(sport=50000,dport=502,flags="FA",seq=113,ack=212)
)

pkts.append(
    IP(src=mitm,dst=hmi)/
    TCP(sport=502,dport=50000,flags="FA",seq=212,ack=114)
)

pkts.append(
    IP(src=hmi,dst=mitm)/
    TCP(sport=50000,dport=502,flags="A",seq=114,ack=213)
)

# =====================================================
# Cierre MITM <-> PLC
# =====================================================

pkts.append(
    IP(src=mitm,dst=plc)/
    TCP(sport=50001,dport=502,flags="FA",seq=313,ack=412)
)

pkts.append(
    IP(src=plc,dst=mitm)/
    TCP(sport=502,dport=50001,flags="FA",seq=412,ack=314)
)

pkts.append(
    IP(src=mitm,dst=plc)/
    TCP(sport=50001,dport=502,flags="A",seq=314,ack=413)
)

wrpcap("T0830_Adversary_in_the_Middle.pcap", pkts)

print("[+] PCAP generado correctamente")
