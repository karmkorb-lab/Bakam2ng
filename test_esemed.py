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

from esemed import Ese
from seaded import LAIUS, KÕRGUS, FPS
from punktid import kontrolli_kokkuporkeid

def main():
    """Käivitab esemete ja punktisüsteemi testmängu."""

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
    mangija_kiirus = 300
    punktid = 0
    font = pygame.font.SysFont("arial", 28)

    teade = ""
    teate_lopp = 0
    teate_varv = (255, 255, 255)

    while tootab:
        dt = taimer.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tootab = False

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

        # Megabooster ilmub 10 sekundit pärast leveli algust.
        # Märgime selle ilmunuks ka siis, kui mängija seda ei kogu.
        if leveli_aeg >= STIPI_ILMUMISE_AEG and not stipp_ilmunud:

          stipendium = Ese("stipp", 0, -40)

          stipendium.rect.x = random.randint(
              0,
              LAIUS - stipendium.rect.width
          )

          esemed.append(stipendium)

          stipp_ilmunud = True

        
        # Iga 1.0 sekundi tagant ilmub uus ese
        if ilmumise_aeg >= 1.0:
            # Takistuste kogutõenäosus on 70%, boosteritel 30%.
            # Stipendiumi genereeritakse tavapärastest esemetest eraldi.
            liik = random.choices(
                ["kell", "kodutöö", "eksam", "kohv", "redbull"],
                weights=[30, 25, 15, 15, 15],
                k=1
            )[0]

            uus_ese = Ese(liik, 0, -90)

            # Suuname 75% takistustest mängija praegusele liikumisteele,
            # et mängija peaks nende eest aktiivselt põikama.
            if uus_ese.punktid < 0 and random.random() < 0.75:
                x = mangija.centerx - uus_ese.rect.width // 2
            else:
                # Boosterid ja osa takistusi ilmuvad juhuslikult
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

if __name__ == "__main__":
    main