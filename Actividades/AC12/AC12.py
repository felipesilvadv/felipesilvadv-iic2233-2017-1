def get_primes(n):
    numbers = set(range(n, 1, -1))
    primes = []
    while numbers:
        p = numbers.pop()
        primes.append(p)
        numbers.difference_update(set(range(p * 2, n + 1, p)))
    return primes


def numeros_malvados():
    i = 0
    while True:
        if bin(i).count("1") % 2 == 0:
            yield i
        i += 1


malvados = numeros_malvados()
next(malvados)

with open('chatayudantes.iic2233', 'rb') as file:
    datos = file.read()

primero = bytearray()

contador = 0
b = 0
for num in datos:
    if contador <= 3:
        b += int(num)
        contador += 1
    else:
        b = str(b)
        final = ""
        if len(b) < 3:
            b = "0" * (3 - len(b)) + b
        for bit in b:
            if bit == "0":
                final += "5"
            elif bit == "5":
                final += "0"
            else:
                final += str(10 - int(bit))

        final = [letra for letra in final]
        final.reverse()
        final = "".join(final)
        final = int(final)
        primero += bytes(final)
        b = 0
        contador = 0

audio = bytearray()
gif = bytearray()

pos = 0
terminado = False
i = 0
par = 0
primos = get_primes(10000)
n = primos[i]
print(len(primero))
while not terminado:
    if 9783 < len(audio):
        terminado = True
        n = len(primero) - pos
    if par % 2 == 0:  # AUDIO
        audio += primero[pos:pos + n]
        pos += n
        n = next(malvados)


    else:  # Imagen
        gif += primero[pos:pos + n]
        pos += n
        n = primos[i]
        i += 1
        # try:
        #     n = primos[i]
        # except IndexError:
        #     terminado = True
        #     gif += primero[pos:]

    par += 1

gif += primero[pos:]
archivo1 = open("Audio.wav", "wb")
archivo1.close()
archivo2 = open("Imagen.gif", "wb")
archivo2.close()
archivo1 = open("Audio.wav", "ab")
archivo2 = open("Imagen.gif", "ab")

for i in range(0, len(audio), 512):
    archivo1.write(audio[i: i + 512])
archivo1.close()

for i in range(0, len(gif), 1024):
    archivo2.write(gif[i: i + 1024])
archivo2.close()