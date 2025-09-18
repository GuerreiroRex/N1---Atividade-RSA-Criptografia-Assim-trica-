from yaspin import yaspin
from socket import *
from modules.gerar_chaves import RSA
import json


with yaspin(text="Gerando chaves", timer = True) as sp:
    rsa = RSA()
    sp.ok()

serverPort = 1300
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(5) 

connectionSocket, addr = serverSocket.accept()
with yaspin(text="Trocando chaves", timer = True) as sp:
    chave_do_client = connectionSocket.recv(65000)
    connectionSocket.sendall( bytes(json.dumps(rsa.chave_publica), "utf-8") )
    sp.ok()

chave_do_client_n, chave_do_client_e = json.loads( str(chave_do_client, "utf-8") )


sentence_encript = connectionSocket.recv(65000)
sentence_encript = int.from_bytes( sentence_encript , 'big')

sentence = rsa.descriptografar(sentence_encript)

print("Recebido criptografado: ", sentence_encript)
print("Recebido original: ", sentence)

sentence = sentence.upper() 
sentence_encript: int = RSA.criptografar(0, chave_do_client_e, chave_do_client_n, sentence)
connectionSocket.sendall( sentence_encript.to_bytes( (rsa.n.bit_length() + 7) // 8, 'big') )


print("Enviado original: ", sentence)
print("Enviado criptografado: ", sentence_encript)

connectionSocket.close()