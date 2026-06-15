from scapy.all import *

attacker = "192.168.70.150"
plc = "192.168.70.129"

sport = 51000
dport = 502

pkts = []

# =====================================================
# TCP Handshake
# =====================================================

pkts.append(
    IP(src=attacker,dst=plc)/
    TCP(sport=sport,dport=dport,flags="S",seq=100)
)

pkts.append(
    IP(src=plc,dst=attacker)/
    TCP(sport=dport,dport=sport,flags="SA",seq=200,ack=101)
)

pkts.append(
    IP(src=attacker,dst=plc)/
    TCP(sport=sport,dport=dport,flags="A",seq=101,ack=201)
)

client_seq = 101
server_seq = 201

# =====================================================
# Brute Force I/O
# Recorrido de coils 0-7
# =====================================================

for coil in range(8):

    transaction_id = coil + 1

    payload = (
        transaction_id.to_bytes(2, "big") +
        b"\x00\x00" +          # Protocol ID
        b"\x00\x06" +          # Length
        b"\x01" +              # Unit ID
        b"\x05" +              # FC05
        coil.to_bytes(2,"big") +
        b"\xFF\x00"            # ON
    )

    pkts.append(
        IP(src=attacker,dst=plc)/
        TCP(
            sport=sport,
            dport=dport,
            flags="PA",
            seq=client_seq,
            ack=server_seq
        )/
        Raw(payload)
    )

    client_seq += len(payload)

    # PLC responde eco de la escritura
    pkts.append(
        IP(src=plc,dst=attacker)/
        TCP(
            sport=dport,
            dport=sport,
            flags="PA",
            seq=server_seq,
            ack=client_seq
        )/
        Raw(payload)
    )

    server_seq += len(payload)

# =====================================================
# TCP Close
# =====================================================

pkts.append(
    IP(src=attacker,dst=plc)/
    TCP(
        sport=sport,
        dport=dport,
        flags="FA",
        seq=client_seq,
        ack=server_seq
    )
)

client_seq += 1

pkts.append(
    IP(src=plc,dst=attacker)/
    TCP(
        sport=dport,
        dport=sport,
        flags="FA",
        seq=server_seq,
        ack=client_seq
    )
)

server_seq += 1

pkts.append(
    IP(src=attacker,dst=plc)/
    TCP(
        sport=sport,
        dport=dport,
        flags="A",
        seq=client_seq,
        ack=server_seq
    )
)

wrpcap("T0806_Brute_Force_IO.pcap", pkts)

print("[+] PCAP generado: T0806_Brute_Force_IO.pcap")
