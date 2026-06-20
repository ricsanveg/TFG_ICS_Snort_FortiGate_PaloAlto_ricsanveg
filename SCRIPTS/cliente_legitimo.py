from pymodbus.client import ModbusTcpClient
import time

# Configuración del PLC objetivo
PLC_IP = "192.168.70.129" 

def generar_trafico_legitimo():
    client = ModbusTcpClient(PLC_IP)
    
    if client.connect():
        print(f"[+] Conectado al PLC {PLC_IP}. Generando tráfico Modbus legítimo de fondo...")
        try:
            while True:
                # La sintaxis infalible: usar kwargs solo para 'address' y 'count'
                client.read_holding_registers(address=0, count=1)
                time.sleep(1) # Espera 1 segundo entre peticiones
        except KeyboardInterrupt:
            print("\n[*] Tráfico legítimo detenido por el usuario.")
        except Exception as e:
            print(f"\n[-] Ocurrió un error en la lectura: {e}")
        finally:
            client.close()
            print("[*] Conexión cerrada.")
    else:
        print("[-] Error al conectar. Revisa la IP o si el PLC está encendido.")

if __name__ == "__main__":
    generar_trafico_legitimo()
