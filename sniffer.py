import socket
import struct
import sys

PORTA_ALVO = 5050
buffers = {}


def processar_linha(chave, linha):
    texto = linha.decode("utf-8", errors="replace")

    src_ip, src_port, dst_ip, dst_port = chave

    print(
        f"{src_ip}:{src_port} -> "
        f"{dst_ip}:{dst_port} | {texto}"
    )

    if texto.startswith("USER "):
        print(
            f"    [INTERCEPTADO] Usuario: {texto[5:]}"
        )

    elif texto.startswith("PASS "):
        print(
            f"    [INTERCEPTADO] Senha: {texto[5:]}"
        )

    elif texto.startswith("MSG "):
        print(
            f"    [INTERCEPTADO] Mensagem: {texto[4:]}"
        )


def processar_payload(
    src_ip,
    src_port,
    dst_ip,
    dst_port,
    payload
):
    chave = (
        src_ip,
        src_port,
        dst_ip,
        dst_port
    )

    if chave not in buffers:
        buffers[chave] = bytearray()

    buffers[chave].extend(payload)

    while b"\n" in buffers[chave]:
        linha, restante = buffers[chave].split(
            b"\n",
            1
        )

        buffers[chave] = bytearray(restante)

        linha = linha.rstrip(b"\r")

        processar_linha(chave, linha)


def main():
    if len(sys.argv) != 2:
        print(
            "Uso: sudo python3 sniffer.py <interface>"
        )
        print(
            "Exemplo: sudo python3 sniffer.py enp0s3"
        )
        sys.exit(1)

    interface = sys.argv[1]

    sniffer = socket.socket(
        socket.AF_PACKET,
        socket.SOCK_RAW,
        socket.ntohs(0x0003)
    )

    sniffer.bind((interface, 0))

    print(
        f"[+] Sniffer iniciado na interface {interface}"
    )
    print(
        f"[+] Monitorando TCP porta {PORTA_ALVO}"
    )
    print(
        "[+] Pressione Ctrl+C para parar.\n"
    )

    while True:
        pacote, _ = sniffer.recvfrom(65535)

        if len(pacote) < 14:
            continue

        ethertype = struct.unpack(
            "!H",
            pacote[12:14]
        )[0]

        if ethertype != 0x0800:
            continue

        ip_inicio = 14

        if len(pacote) < ip_inicio + 20:
            continue

        versao_ihl = pacote[ip_inicio]

        versao = versao_ihl >> 4
        ihl = (versao_ihl & 0x0F) * 4

        if versao != 4:
            continue

        protocolo = pacote[ip_inicio + 9]

        if protocolo != 6:
            continue

        tamanho_total = struct.unpack(
            "!H",
            pacote[
                ip_inicio + 2:
                ip_inicio + 4
            ]
        )[0]

        src_ip = socket.inet_ntoa(
            pacote[
                ip_inicio + 12:
                ip_inicio + 16
            ]
        )

        dst_ip = socket.inet_ntoa(
            pacote[
                ip_inicio + 16:
                ip_inicio + 20
            ]
        )

        tcp_inicio = ip_inicio + ihl

        if len(pacote) < tcp_inicio + 20:
            continue

        src_port, dst_port = struct.unpack(
            "!HH",
            pacote[
                tcp_inicio:
                tcp_inicio + 4
            ]
        )

        if (
            src_port != PORTA_ALVO
            and dst_port != PORTA_ALVO
        ):
            continue

        data_offset = (
            pacote[tcp_inicio + 12] >> 4
        ) * 4

        payload_inicio = tcp_inicio + data_offset
        payload_fim = ip_inicio + tamanho_total

        if payload_inicio >= payload_fim:
            continue

        payload = pacote[
            payload_inicio:
            payload_fim
        ]

        processar_payload(
            src_ip,
            src_port,
            dst_ip,
            dst_port,
            payload
        )


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("\n[-] Sniffer encerrado.")