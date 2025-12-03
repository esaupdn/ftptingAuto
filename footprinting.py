import socket
import dns.resolver
import datetime

# Dicionário de portas comuns
COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "TELNET",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    111: "RPCBind",
    135: "MS RPC",
    139: "NETBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-Proxy",
}

def dns_lookup(target):
    results = {"A": [], "MX": [], "NS": []}
    for record in results.keys():
        try:
            response = dns.resolver.resolve(target, record)
            results[record] = [str(r) for r in response]
        except:
            results[record] = ["Não encontrado"]
    return results

def scan_ports(target):
    open_ports = []
    print("[*] Varredura de portas iniciada (pode demorar um pouco)...")
    for port, service in COMMON_PORTS.items():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1) # Timeout ajustado para 1 segundo
        try:
            result = sock.connect_ex((target, port))
            if result == 0:
                open_ports.append((port, service))
        except:
            pass
        finally:
            sock.close()
    return open_ports

def grab_banner(target, port):
    try:
        s = socket.socket()
        s.settimeout(2)
        s.connect((target, port))
        
        # MELHORIA: Se for porta WEB, enviamos um "oi" (GET) para o servidor responder
        if port in [80, 8080, 443]:
            try:
                msg = f'GET / HTTP/1.1\r\nHost: {target}\r\n\r\n'
                s.send(msg.encode())
            except:
                pass # Se falhar o envio, tenta ler mesmo assim

        # 'errors=ignore' evita que o script quebre se receber caracteres estranhos
        banner = s.recv(1024).decode(errors='ignore').strip()
        s.close()
        return banner if banner else "Nenhum banner retornado"
    except:
        return "Falha ao coletar banner ou Timeout"

def generate_txt(target, dns_data, ports, banners):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # CORREÇÃO: Indentação alinhada corretamente dentro da função
    filename = f"relatorio_{target}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("=============================================\n")
        f.write("        RELATÓRIO DE FOOTPRINTING\n")
        f.write("=============================================\n\n")
        f.write(f"Alvo: {target}\n")
        f.write(f"Gerado em: {timestamp}\n\n")

        f.write("=========== 1. DNS LOOKUP ===========\n")
        for record, values in dns_data.items():
            f.write(f"\n{record} Records:\n")
            for v in values:
                f.write(f" - {v}\n")

        f.write("\n=========== 2. PORTAS ABERTAS ===========\n")
        if not ports:
            f.write("Nenhuma porta comum detectada como aberta.\n")
        else:
            for port, service in ports:
                f.write(f"\nPorta: {port}\n")
                f.write(f"Serviço: {service}\n")
                # Busca o banner com segurança usando .get()
                b_text = banners.get(port, "N/A")
                f.write(f"Banner: {b_text}\n")

    print(f"[+] Relatório TXT gerado com sucesso: {filename}")

if __name__ == "__main__":
    try:
        target = input("Digite o domínio ou IP do alvo: ")
        
        print("\n[*] Realizando DNS Lookup...")
        dns_result = dns_lookup(target)

        print("[*] Varredura de portas...")
        open_ports = scan_ports(target)

        print("[*] Coletando banners dos serviços encontrados...")
        banner_results = {}
        for port, service in open_ports:
            print(f"    -> Lendo banner da porta {port} ({service})...")
            banner_results[port] = grab_banner(target, port)

        generate_txt(target, dns_result, open_ports, banner_results)
        
    except KeyboardInterrupt:
        print("\n[!] Script interrompido pelo usuário.")
    except Exception as e:
        print(f"\n[!] Ocorreu um erro inesperado: {e}")