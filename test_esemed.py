import pygame
import random
from esemed import Ese
from seaded import LAIUS, KÕRGUS, FPS
from punktid import kontrolli_kokkuporkeid

pygame.init()

ekraan = pygame.display.set_mode((LAIUS, KÕRGUS))
pygame.display.set_caption("Esemete test")

taimer = pygame.time.Clock()

esemed = []
ilmumise_aeg = 0

tootab = True


while tootab:
    dt = taimer.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            tootab = False

    # Loendame, kui palju aega on moodunud
    ilmumise_aeg += dt

    # Iga 1.5 sekundi tagant ilmub uus ese
    if ilmumise_aeg >= 1.5:
        liik = random.choice([
            "kell", "kodutöö", "eksam",
            "kohv", "redbull", "stipp"
        ])

        # Juhuslik horisontaalne asukoht
        x = random.randint(0, LAIUS - 50)

        uus_ese = Ese(liik, x, -50)
        esemed.append(uus_ese)

        ilmumise_aeg = 0

    ekraan.fill((20, 20, 20))

    # Liigutame ja joonistame koik esemed
    for ese in esemed[:]:
        ese.liiguta(200, dt)
        ese.joonista(ekraan)

        # Eemaldame ekraanilt kadunud esemed
        if ese.ekraanilt_valjas():
            esemed.remove(ese)

    pygame.display.flip()


pygame.quit()
