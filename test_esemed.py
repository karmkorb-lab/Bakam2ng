"""
Projekt: Bakamäng
Autorid: Merilin-Grete Kakko, Karm Korb
Fail: test_esemed.py

Kirjeldus:
Testprogramm takistuste ja boosterite funktsionaalsuse
kontrollimiseks. Võimaldab testida esemete juhuslikku ilmumist,
liikumist, mängijaga kokkupõrkeid ja punktiarvestust.
Sisaldab ka stipendiumi ühekordse ilmumise kontrolli.

Testprogramm töötab põhimängust eraldiseisvalt.
"""

import random

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

# Stipendiumi ilmumise kontroll
leveli_aeg = 0
stipp_ilmunud = False
STIPI_ILMUMISE_AEG = 10

tootab = True


# Ajutine mängija kokkupõrgete testimiseks
mangija = pygame.Rect(375, 500, 40, 40)

# Mängija liikumiskiirus
mangija_kiirus = 300

# Algne punktisumma
punktid = 0

# Punktide kuvamiseks kasutatav font
font = pygame.font.SysFont("arial", 28)

teade = ""
teate_lopp = 0
teate_varv = (255, 255, 255)

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
    leveli_aeg += dt

    # Stipendium ilmub ainult üks kord
    if leveli_aeg >= STIPI_ILMUMISE_AEG and not stipp_ilmunud:

      # Loome stipendiumi
      stipendium = Ese("stipp", 0, -40)

      # Valime juhusliku asukoha
      stipendium.rect.x = random.randint(
          0,
          LAIUS - stipendium.rect.width
      )

      # Lisame stipendiumi mängu
      esemed.append(stipendium)

      # Märgime, et stipendium on juba ilmunud
      stipp_ilmunud = True

    
    # Iga 1.0 sekundi tagant ilmub uus ese
    if ilmumise_aeg >= 1.0:
        liik = random.choices(
            ["kell", "kodutöö", "eksam", "kohv", "redbull"],
            weights=[30, 25, 15, 15, 15],
            k=1
        )[0]

        uus_ese = Ese(liik, 0, -90)

        # Takistused ilmuvad enamasti mängija teele
        if uus_ese.punktid < 0 and random.random() < 0.75:
            x = mangija.centerx - uus_ese.rect.width // 2
        else:
            # Booster'id ja osa takistusi ilmuvad juhuslikult
            x = random.randint(
                0, LAIUS - uus_ese.rect.width
            )

        # Hoiame eseme täielikult mänguakna sees
        uus_ese.rect.x = max(
            0,
            min(x, LAIUS - uus_ese.rect.width)
        )

        esemed.append(uus_ese)
        ilmumise_aeg = 0

    ekraan.fill((20, 20, 20))

    # Liigutame ja joonistame koik esemed
    for ese in esemed[:]:
        ese.liiguta(300, dt)
        ese.joonista(ekraan)

        # Eemaldame ekraanilt kadunud esemed
        if ese.ekraanilt_valjas():
            esemed.remove(ese)

    # Kontrollime kokkupõrkeid
    muutus, uus_teade = kontrolli_kokkuporkeid(
      mangija, esemed
    )

    punktid += muutus

    if uus_teade is not None:
        teade = uus_teade

        # Näitame teadet ühe sekundi
        teate_lopp = pygame.time.get_ticks() + 1000

        if muutus >= 0:
            teate_varv = (80, 220, 120)
        else:
            teate_varv = (255, 80, 80)

    # Joonistame mängija valge ruuduna
    pygame.draw.rect(ekraan, (255, 255, 255), mangija)

    # Kuvame punktisumma
    punktide_tekst = font.render(
        f"Punktid: {punktid}",
        True,
        (255, 255, 255)
    )

    ekraan.blit(punktide_tekst, (20, 20)) 

    # Kuvame viimase kokkupõrke teadet ühe sekundi
    if pygame.time.get_ticks() < teate_lopp:
        teate_tekst = font.render(
            teade,
            True,
            teate_varv
        )

        ekraan.blit(teate_tekst, (20, 60))

    pygame.display.flip()


pygame.quit()
