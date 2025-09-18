
from modules.gerar_chaves import RSA


rsa = RSA()

texto = "Teste"

dm = rsa.criptografar( texto )
dc = RSA.descriptografar(rsa.d, rsa.n, dm)

print( "Mensagem recebida: ", dc )