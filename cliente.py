import socket

SERVIDOR = "10.10.10.20"
PORTA = 5050


def enviar_linha(socket_cliente, mensagem):
    socket_cliente.sendall(
        (mensagem + "\n").encode("utf-8")
    )


def receber_linha(arquivo):
    dados = arquivo.readline()

    if not dados:
        return None

    return dados.decode(
        "utf-8",
        errors="replace"
    ).rstrip("\r\n")


def main():
    print(
        f"Conectando ao servidor "
        f"{SERVIDOR}:{PORTA}..."
    )

    cliente = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    cliente.connect(
        (SERVIDOR, PORTA)
    )

    arquivo = cliente.makefile("rb")

    resposta = receber_linha(arquivo)

    print("Servidor:", resposta)

    usuario = input("Usuario: ")
    senha = input("Senha: ")

    enviar_linha(
        cliente,
        f"USER {usuario}"
    )

    enviar_linha(
        cliente,
        f"PASS {senha}"
    )

    resposta = receber_linha(arquivo)

    print("Servidor:", resposta)

    if resposta != "AUTH OK":
        cliente.close()
        return

    while True:

        mensagem = input(
            "Mensagem (/quit para sair): "
        )

        if mensagem == "/quit":

            enviar_linha(
                cliente,
                "QUIT"
            )

            print(
                "Servidor:",
                receber_linha(arquivo)
            )

            break

        enviar_linha(
            cliente,
            f"MSG {mensagem}"
        )

        resposta = receber_linha(arquivo)

        print(
            "Servidor:",
            resposta
        )

    cliente.close()


if __name__ == "__main__":
    main()