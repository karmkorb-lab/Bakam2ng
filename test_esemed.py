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


# Ajutine mängija kokkupõrgete testimiseks
mangija = pygame.Rect(375, 500, 40, 40)

# Mängija liikumiskiirus
mangija_kiirus = 300

# Algne punktisumma
punktid = 0

# Punktide kuvamiseks kasutatav font
font = pygame.font.SysFont("arial", 28)


while tootab:
    dt = taimer.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            tootab = False

    # Kontrollime, milliseid klahve vajutatakse
    klahvid = pygame.key.get_pressed()

    if klahvid[pygame.K_LEFT] or klahvid[pygame.K_a]:
        mangija.x -= round(mangija_kiirus * dt)

    if klahvid[pygame.K_RIGHT] or klahvid[pygame.K_d]:
        mangija.x += round(mangija_kiirus * dt)

    # Hoiame mängija ekraani piirides
    mangija.clamp_ip(ekraan.get_rect())


    # Loendame, kui palju aega on möödunud
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

    # Kontrollime kokkupõrkeid
    punktid += kontrolli_kokkuporkeid(mangija, esemed)

    # Joonistame mängija valge ruuduna
    pygame.draw.rect(ekraan, (255, 255, 255), mangija)

    # Kuvame punktisumma
    punktide_tekst = font.render(
        f"Punktid: {punktid}",
        True,
        (255, 255, 255)
    )

    ekraan.blit(punktide_tekst, (20, 20)) 

    pygame.display.flip()


pygame.quit()
