# LABCHAT Security Lab — Fase 1

Projeto desenvolvido para a disciplina de **Laboratório de Redes de Computadores**.

## 1. Objetivo

Este projeto corresponde à **Fase 1 — Criação da Aplicação Alvo e do Sniffer de Tráfego**.

O objetivo é demonstrar, em um ambiente virtual isolado, a vulnerabilidade de confidencialidade existente em um protocolo de aplicação que transmite informações sensíveis em texto claro.

Para realizar a demonstração foram desenvolvidos:

- um servidor TCP;
- um cliente TCP;
- um protocolo de aplicação simples denominado `LABCHAT/1`;
- um interceptador passivo utilizando raw socket;
- um ambiente virtual composto por cliente, servidor e observador;
- capturas utilizando Wireshark para comprovar que os dados trafegam em texto claro.

A aplicação foi desenvolvida propositalmente sem criptografia ou autenticação forte, permitindo que uma terceira máquina presente na rede consiga observar usuário, senha e mensagens transmitidas.

---

## 2. Estrutura do projeto

```text
fase1/
├── cliente.py
├── servidor.py
├── sniffer.py
├── README.md
└── evidencias/
    ├── wireshark-follow-tcp-stream.png
    ├── wireshark-pacote-197-senha.png
    ├── wireshark-stream-credenciais-mensagem.png
    ├── sniffer-raw-socket.png
    └── sniffer-interceptacao-completa.png
```

### Arquivos

- `cliente.py`: cliente TCP da aplicação LABCHAT.
- `servidor.py`: servidor responsável pela autenticação e troca de mensagens.
- `sniffer.py`: interceptador passivo desenvolvido com raw socket.
- `evidencias/`: contém as capturas realizadas durante os testes.

---

## 3. Topologia da rede

O laboratório foi implementado utilizando três máquinas virtuais Ubuntu no VirtualBox.

As três máquinas estão conectadas à mesma rede interna do VirtualBox:

```text
labredes
```

A topologia utilizada é:

```text
                       Rede interna "labredes"

        ┌─────────────────────────────┐
        │          CLIENTE            │
        │       10.10.10.10           │
        │       cliente.py            │
        └──────────────┬──────────────┘
                       │
                       │ TCP
                       │ Porta 5050
                       │
                       ▼
        ┌─────────────────────────────┐
        │         SERVIDOR            │
        │       10.10.10.20           │
        │       servidor.py           │
        └─────────────────────────────┘


        ┌─────────────────────────────┐
        │        OBSERVADOR           │
        │       10.10.10.30           │
        │       sniffer.py            │
        │       Wireshark             │
        └─────────────────────────────┘
```

A máquina observadora utiliza sua interface de rede em **modo promíscuo**, possibilitando a observação do tráfego entre cliente e servidor.

### Endereçamento

| Máquina | Endereço IP | Função |
|---|---|---|
| Cliente | `10.10.10.10` | Executa `cliente.py` |
| Servidor | `10.10.10.20` | Executa `servidor.py` |
| Observador | `10.10.10.30` | Executa `sniffer.py` e Wireshark |

A aplicação utiliza:

```text
Protocolo de transporte: TCP
Porta da aplicação: 5050
```

---

## 4. Protocolo LABCHAT/1

Para o trabalho foi desenvolvido um protocolo de aplicação simples denominado:

```text
LABCHAT/1
```

O protocolo funciona sobre TCP e utiliza mensagens de texto terminadas por uma quebra de linha (`\n`).

Uma sessão típica ocorre da seguinte maneira:

```text
Servidor -> HELLO LABCHAT/1

Cliente  -> USER duda
Cliente  -> PASS redes123

Servidor -> AUTH OK

Cliente  -> MSG mensagem de teste
Servidor -> ECHO mensagem de teste

Cliente  -> QUIT
Servidor -> BYE
```

### Comandos

#### USER

Informa o nome de usuário utilizado na autenticação.

Exemplo:

```text
USER duda
```

#### PASS

Informa a senha utilizada na autenticação.

Exemplo:

```text
PASS redes123
```

#### MSG

Envia uma mensagem ao servidor.

Exemplo:

```text
MSG mensagem de teste
```

O servidor responde utilizando o comando:

```text
ECHO mensagem de teste
```

#### QUIT

Solicita o encerramento da conexão.

```text
QUIT
```

O servidor responde:

```text
BYE
```

---

## 5. Vulnerabilidade demonstrada

A versão inicial do LABCHAT não utiliza criptografia.

Dessa forma, dados como:

```text
USER duda
PASS redes123
MSG mensagem de teste
```

são enviados diretamente em texto claro através da rede.

Uma terceira máquina com acesso ao tráfego consegue, portanto, recuperar as credenciais e o conteúdo das mensagens mesmo sem participar diretamente da comunicação.

Esse comportamento é proposital e permite demonstrar a quebra de confidencialidade causada pela utilização de um protocolo de aplicação sem proteção.

---

## 6. Requisitos

Para execução do laboratório são utilizados:

- VirtualBox;
- Ubuntu Linux;
- Python 3;
- Wireshark;
- três máquinas virtuais;
- privilégios administrativos para utilização do raw socket.

Toda a comunicação da aplicação foi implementada diretamente utilizando a biblioteca `socket` do Python.

Não são utilizados frameworks que escondam o funcionamento dos sockets.

---

# 7. Execução

## 7.0 VirtualMachines
Criar 3 Vms, um para o Servidor, um para o Cliente e um para o Observador.

```bash
usar linux ubuntu iso
```

```bash
baixar e configurar python3 em cada vm

sudo apt update
sudo apt install python3 -y
```

```bash
baixar e instalar wireshark no observador

sudo apt update
sudo apt install python3 wireshark -y
```

Em cada ambiente, setar conexao com internet e com a rede interna 'labredes'. Ao iniciar cada vm, configurar o endereço de cada máquina.

Servidor:
```bash
sudo ip addr add 10.10.10.20/24 dev enp0s3
ip -br a
```

Cliente:
```bash
sudo ip addr add 10.10.10.10/24 dev enp0s3
ip -br a
```

Observador:
```bash
sudo ip addr add 10.10.10.30/24 dev enp0s3
ip -br a
```


## 7.1 Verificar a conectividade

Antes de executar a aplicação, é possível testar a comunicação entre as máquinas.

No cliente:

```bash
ping 10.10.10.20
```

Para testar a comunicação com o observador:

```bash
ping 10.10.10.30
```

As três máquinas devem estar conectadas à rede interna `labredes`.

---

## 7.2 Executar o servidor

Na VM Servidor:

```text
IP: 10.10.10.20
```
Crie um diretorio lab-redes

```bash
mkdir -p ~/lab-redes
```

Acesse o diretório onde está o código:

```bash
cd ~/lab-redes
```

E cole lá o arquivo servidor.py

Execute:

```bash
python3 servidor.py
```

A saída esperada é semelhante a:

```text
LABCHAT ouvindo na porta 5050...
```

O servidor ficará aguardando conexões TCP na porta `5050`.

---

## 7.3 Executar o sniffer

Na VM Observador:

```text
IP: 10.10.10.30
```

Crie um diretorio lab-redes

```bash
mkdir -p ~/lab-redes
```

Acesse o diretório onde está o código:

```bash
cd ~/lab-redes
```

E cole lá o arquivo sniffer.py


Acesse o diretório do programa:

```bash
cd ~/lab-redes
```

Primeiro identifique a interface da rede do laboratório:

```bash
ip -br a
```

No ambiente utilizado, a interface da rede `labredes` é:

```text
enp0s3
```

Execute o sniffer com privilégios administrativos:

```bash
sudo python3 sniffer.py enp0s3
```

A saída inicial deverá ser semelhante a:

```text
[+] Sniffer iniciado na interface enp0s3
[+] Monitorando TCP porta 5050
[+] Pressione Ctrl+C para parar.
```

O uso de `sudo` é necessário porque o programa utiliza um raw socket.

---

## 7.4 Executar o cliente

Na VM Cliente:

```text
IP: 10.10.10.10
```

Crie um diretorio lab-redes

```bash
mkdir -p ~/lab-redes
```

Acesse o diretório onde está o código:

```bash
cd ~/lab-redes
```

E cole lá o arquivo cliente.py


Acesse:

```bash
cd ~/lab-redes
```

Execute:

```bash
python3 cliente.py
```

O cliente tentará estabelecer conexão com:

```text
10.10.10.20:5050
```

A saída inicial deverá ser semelhante a:

```text
Conectando ao servidor 10.10.10.20:5050...
Servidor: HELLO LABCHAT/1
Usuario:
```

Para o teste realizado foram utilizadas as credenciais:

```text
Usuario: duda
Senha: redes123
```

Após a autenticação:

```text
Servidor: AUTH OK
```

Uma mensagem pode então ser enviada:

```text
Mensagem (/quit para sair): teste do sniffer raw socket
```

O servidor responde:

```text
Servidor: ECHO teste do sniffer raw socket
```

Para finalizar a sessão:

```text
/quit
```

O servidor responde:

```text
Servidor: BYE
```

---

# 8. Interceptador passivo

O programa `sniffer.py` implementa um interceptador passivo utilizando raw socket.

A criação do socket é realizada com:

```python
socket.socket(
    socket.AF_PACKET,
    socket.SOCK_RAW,
    socket.ntohs(0x0003)
)
```

O uso de `AF_PACKET` permite capturar diretamente os quadros recebidos pela interface de rede em sistemas Linux.

O programa interpreta manualmente os protocolos necessários para chegar até os dados da aplicação.

A estrutura analisada é:

```text
Ethernet
   ↓
IPv4
   ↓
TCP
   ↓
LABCHAT/1
```

Primeiramente é analisado o cabeçalho Ethernet.

Depois é verificado se o quadro transporta IPv4.

O cabeçalho IPv4 é então processado para verificar se o protocolo da camada de transporte é TCP.

Em seguida são obtidas as portas TCP.

O sniffer ignora tráfego que não tenha relação com a porta:

```text
5050
```

Por fim, o payload TCP é extraído e processado como uma mensagem do protocolo LABCHAT.

---

## 8.1 Informações interceptadas

Durante uma execução, o sniffer apresentou uma saída semelhante a:

```text
10.10.10.20:5050 -> 10.10.10.10:55826 | HELLO LABCHAT/1

10.10.10.10:55826 -> 10.10.10.20:5050 | USER duda
    [INTERCEPTADO] Usuario: duda

10.10.10.10:55826 -> 10.10.10.20:5050 | PASS redes123
    [INTERCEPTADO] Senha: redes123

10.10.10.20:5050 -> 10.10.10.10:55826 | AUTH OK

10.10.10.10:55826 -> 10.10.10.20:5050 | MSG teste do sniffer raw socket
    [INTERCEPTADO] Mensagem: teste do sniffer raw socket

10.10.10.20:5050 -> 10.10.10.10:55826 | ECHO teste do sniffer raw socket
```

O resultado demonstra que o observador consegue recuperar:

- nome do usuário;
- senha;
- conteúdo da mensagem.

Isso ocorre sem que o observador participe diretamente da conexão TCP.

---

# 9. Reconstrução das mensagens TCP

TCP fornece um fluxo contínuo de bytes e não preserva as fronteiras das mensagens criadas pela aplicação.

Por exemplo, duas mensagens enviadas separadamente:

```text
USER duda\n
PASS redes123\n
```

não possuem garantia de serem recebidas em dois segmentos separados.

Elas poderiam ser recebidas juntas:

```text
USER duda\nPASS redes123\n
```

ou divididas em diferentes segmentos.

Por esse motivo, o protocolo LABCHAT utiliza:

```text
\n
```

como delimitador das mensagens.

O sniffer mantém buffers para os fluxos TCP observados e acumula os dados até encontrar uma quebra de linha.

Somente após encontrar o delimitador a mensagem é interpretada.

---

# 10. Análise utilizando Wireshark

Além do sniffer próprio, o Wireshark foi utilizado como ferramenta auxiliar para observar e comprovar o conteúdo transmitido pelo protocolo.

A captura foi realizada na VM Observador.

Interface utilizada:

```text
enp0s3
```

Foi aplicado o seguinte filtro de exibição:

```text
tcp.port == 5050
```

Dessa maneira, apenas o tráfego referente à aplicação LABCHAT foi exibido.

---

## 10.1 Follow TCP Stream

O recurso:

```text
Follow
→ TCP Stream
```

permitiu reconstruir a comunicação completa entre cliente e servidor.

Na captura foi possível visualizar diretamente:

```text
HELLO LABCHAT/1
USER duda
PASS redes123
AUTH OK
MSG mensagem de teste
ECHO mensagem de teste
QUIT
BYE
```

A captura demonstra que todo o conteúdo da aplicação pode ser lido diretamente por um observador da rede.

A evidência correspondente está armazenada em:

```text
evidencias/wireshark-follow-tcp-stream.png
```

---

## 10.2 Credencial em texto claro

Durante a captura realizada no Wireshark, foi identificado o pacote:

```text
197
```

contendo a senha enviada pelo cliente.

Informações observadas:

```text
Número do pacote: 197

Origem:
10.10.10.10

Destino:
10.10.10.20

Protocolo de transporte:
TCP

Porta de destino:
5050
```

O payload do pacote contém:

```text
PASS redes123
```

Isso comprova que a senha é transmitida sem qualquer mecanismo de cifragem.

A evidência correspondente está armazenada em:

```text
evidencias/wireshark-pacote-197-senha.png
```

---

# 11. Evidências

As capturas realizadas durante os testes estão armazenadas no diretório:

```text
evidencias/
```

## wireshark-follow-tcp-stream.png

Demonstra a utilização do recurso `Follow TCP Stream` para reconstruir a sessão completa do LABCHAT.

É possível observar diretamente usuário, senha e mensagens transmitidas.

---

## wireshark-pacote-197-senha.png

Demonstra o pacote número `197`, contendo:

```text
PASS redes123
```

em texto claro.

---

## wireshark-stream-credenciais-mensagem.png

Demonstra a visualização das credenciais e mensagens da aplicação através da captura TCP.

---

## sniffer-raw-socket.png

Demonstra o interceptador passivo desenvolvido utilizando raw socket.

O programa consegue identificar e extrair:

```text
USER
PASS
MSG
```

diretamente do tráfego capturado.

---

## sniffer-interceptacao-completa.png

Demonstra uma sessão completa capturada pelo sniffer desenvolvido para o trabalho, incluindo:

```text
HELLO LABCHAT/1
USER duda
PASS redes123
AUTH OK
MSG
ECHO
```

---

# 12. Resultado

Os testes realizados demonstraram que o protocolo `LABCHAT/1`, em sua versão inicial, não oferece proteção de confidencialidade.

A máquina observadora conseguiu recuperar diretamente do tráfego:

```text
Usuario: duda
Senha: redes123
Mensagem: teste do sniffer raw socket
```

O comportamento foi comprovado de duas maneiras:

1. através do interceptador passivo desenvolvido com raw socket;
2. através da análise do tráfego utilizando Wireshark.

O pacote número `197`, por exemplo, contém explicitamente:

```text
PASS redes123
```

demonstrando que a senha trafega em texto claro entre cliente e servidor.

Dessa forma, a implementação comprova que um protocolo de aplicação que transmite informações sensíveis sem proteção permite que terceiros com acesso ao tráfego da rede obtenham seu conteúdo, caracterizando uma quebra de confidencialidade.

---

# 13. Observação

Este projeto foi desenvolvido exclusivamente para fins acadêmicos e executado em ambiente virtual isolado.

O interceptador implementado tem como objetivo demonstrar as vulnerabilidades de um protocolo de aplicação sem proteção dentro do ambiente controlado do laboratório.