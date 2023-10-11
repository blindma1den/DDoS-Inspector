import socket
import os

# Configura el host y puerto para monitorear
host = '0.0.0.0'  # Escucha en todas las interfaces de red
port = 80

# Configura el umbral de tráfico y la dirección IP a bloquear
umbral = 100  # Puedes ajustar este valor según tus necesidades
ip_a_bloquear = None

def main():
    # Crea un socket para escuchar el tráfico en el puerto especificado
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    # Inicializa un contador para el tráfico
    contador = 0

    print(f"Monitoreando el tráfico en {host}:{port}...")

    while True:
        data, addr = s.recvfrom(1024)
        contador += len(data)

        # Comprueba si el contador supera el umbral
        if contador > umbral:
            print(f"Posible ataque DDoS detectado desde {addr}")

            # Pregunta al usuario si desea bloquear la dirección IP
            respuesta = input("¿Desea bloquear esta dirección IP? (S/N): ").strip().lower()
            
            if respuesta == 's':
                bloquear_ip(addr[0])
                print(f"Dirección IP {addr[0]} bloqueada.")
                break

def bloquear_ip(ip):
    # Ejecuta un comando para bloquear la dirección IP en iptables (solo funciona con permisos de superusuario)
    os.system(f"sudo iptables -A INPUT -s {ip} -j DROP")

if __name__ == '__main__':
    main()