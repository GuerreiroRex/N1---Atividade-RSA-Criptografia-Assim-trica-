

import random
from modules.primo_hyper import is_probable_prime

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def mod_inverse(e, phi):
    g, x, y = egcd(e, phi)
    if g != 1:
        raise Exception('Não existe inverso modular')
    else:
        return x % phi

class RSA():

    def __init__(self):
        
        self.p: int
        self.q: int
        self.totiente: int
        self.n: int
        self.d: int


        self.e = 65537

        self.chave_publica = self.gerar_chave_publica()
        self.chave_privada = self.gerar_chave_privada()
    
    def gerar_primo(quant_bits):
        while True:
            num = random.getrandbits(quant_bits)

            if is_probable_prime(num):
                return num

    def gerar_chave_publica(self):           
        p = RSA.gerar_primo(2048)
        q = RSA.gerar_primo(2048)

        n = p * q
        totiente = (p-1)*(q-1)

        self.p = p
        self.q = q
        self.n = n
        self.totiente = totiente

        return (n, self.e)
    
    def gerar_chave_privada(self):

        d = mod_inverse(self.e, self.totiente)
        self.d = d

        return (self.n, self.d)
    
    def criptografar(_, e: int, n: int, msg: str):
        m = int.from_bytes( msg.encode('utf-8') , 'big')

        c = pow(m, e, n)
        return c

    def descriptografar(self, c: int):
        dc = pow(c, self.d, self.n)
        texto_bytes = dc.to_bytes( (self.n.bit_length() + 7) // 8, 'big')

        return texto_bytes.decode('utf-8')
