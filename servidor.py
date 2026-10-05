import socket
import threading

HOST = "0.0.0.0"
PORT = 5050

USUARIOS = {
    "duda": "redes123"
}


def enviar_linha(conexao, mensagem):
    conexao.sendall((mensagem + "\n").encode("utf-8"))


def receber_linha(arquivo):
    dados = arquivo.readline()

    if not dados:
        return None

    return dados.decode("utf-8", errors="replace").rstrip("\r\n")


def atender_cliente(conexao, endereco):
    print(f"[+] Cliente conectado: {endereco}")

    try:
        arquivo = conexao.makefile("rb")

        enviar_linha(conexao, "HELLO LABCHAT/1")

        # Recebe USER
        linha = receber_linha(arquivo)

        if linha is None or not linha.startswith("USER "):
            enviar_linha(conexao, "ERROR esperado USER")
            return

        usuario = linha[5:]

        # Recebe PASS
        linha = receber_linha(arquivo)

        if linha is None or not linha.startswith("PASS "):
            enviar_linha(conexao, "ERROR esperado PASS")
            return

        senha = linha[5:]

        if USUARIOS.get(usuario) != senha:
            enviar_linha(conexao, "AUTH FAIL")
            return

        enviar_linha(conexao, "AUTH OK")

        print(f"[LOGIN] Usuario autenticado: {usuario}")

        # Recebe mensagens
        while True:
            linha = receber_linha(arquivo)

            if linha is None:
                break

            if linha == "QUIT":
                enviar_linha(conexao, "BYE")
                break

            if linha.startswith("MSG "):
                mensagem = linha[4:]

                print(f"[MSG] {usuario}: {mensagem}")

                enviar_linha(
                    conexao,
                    f"ECHO {mensagem}"
                )

            else:
                enviar_linha(
                    conexao,
                    "ERROR comando desconhecido"
                )

    except Exception as erro:
        print(f"[ERRO] {endereco}: {erro}")

    finally:
        conexao.close()
        print(f"[-] Cliente desconectado: {endereco}")


def main():
    servidor = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    servidor.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    servidor.bind((HOST, PORT))
    servidor.listen()

    print(f"LABCHAT ouvindo na porta {PORT}...")

    while True:
        conexao, endereco = servidor.accept()

        thread = threading.Thread(
            target=atender_cliente,
            args=(conexao, endereco),
            daemon=True
        )

        thread.start()


if __name__ == "__main__":
    main()