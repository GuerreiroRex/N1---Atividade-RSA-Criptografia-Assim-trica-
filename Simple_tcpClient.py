from yaspin import yaspin
from socket import *
from modules.gerar_chaves import RSA
import json


with yaspin(text="Gerando chaves", timer = True) as sp:
    rsa = RSA()
    sp.ok()

    
serverName = "localhost"
serverPort = 1300

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

with yaspin(text="Trocando chaves", timer = True) as sp:
    clientSocket.sendall( bytes( json.dumps(rsa.chave_publica), "utf-8") )
    chave_do_server = clientSocket.recv(65000)
    sp.ok()


chave_do_server_n, chave_do_server_e = json.loads( str(chave_do_server, "utf-8") )

sentence = input("Input lowercase sentence: ")
sentence_encript = RSA.criptografar(0, chave_do_server_e, chave_do_server_n, sentence)
clientSocket.sendall( sentence_encript.to_bytes( (rsa.n.bit_length() + 7) // 8, 'big') )


# sentence_encript = clientSocket.recv(65000)
# sentence_encript = int.from_bytes( sentence_encript , 'big')
# sentence = rsa.descriptografar(sentence_encript)

sentence_encript = clientSocket.recv(65000)
sentence_encript = int.from_bytes( sentence_encript , 'big')

sentence = rsa.descriptografar(sentence_encript)

print("Recebido criptografado: ", sentence_encript)
print("Recebido original: ", sentence)

clientSocket.close()