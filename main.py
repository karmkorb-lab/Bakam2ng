"""
Projekt: Bakamäng
Autorid: Merilin-Grete Kakko, Karm Korb
Fail: main.py

Kirjeldus:
Informaatikatudengi ellujäämismäng (Bakamäng) - Peamoodul
Käivitab mänguakna, haldab mängutsüklit, sündmusi ja ekraani HUD-päist.
"""

import pygame
import random

from seaded import *
from mangija import Mangija
from esemed import Ese
from punktid import kontrolli_kokkuporkeid


def main():
    pygame.init()

    ekraan = pygame.display.set_mode((LAIUS, KÕRGUS))
    pygame.display.set_caption("Bakamäng")

    kell = pygame.time.Clock()

    font = pygame.font.SysFont("arial", 28)
    suur_font = pygame.font.SysFont("arial", 48)

    # Mängija algpositsioon
    algne_x = LAIUS // 2 - MANGIJA_LAIUS // 2
    algne_y = KÕRGUS - MANGIJA_KORGUS - 20

    mangija = Mangija(algne_x, algne_y)

    esemed = []
    punktid = 0

    ilmumise_aeg = 0
    leveli_aeg = 0
    stipp_ilmunud = False

    teade = ""
    teate_lopp = 0
    teate_varv = VALGE

    mang_tootab = True
    mang_labi = False

    while mang_tootab:
        dt = kell.tick(FPS) / 1000

        # Sündmuste kontroll
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mang_tootab = False

            if event.type == pygame.KEYDOWN:
                if mang_labi and event.key == pygame.K_r:
                    mangija = Mangija(algne_x, algne_y)
                    esemed = []
                    punktid = 0
                    ilmumise_aeg = 0
                    leveli_aeg = 0
                    stipp_ilmunud = False
                    teade = ""
                    mang_labi = False

        # 1. Puhastame ekraani igal kaadril uuesti
        ekraan.fill(MUST)

        if not mang_labi:
            # Mängija liikumine
            mangija.uuenda()

            # Aja arvestamine
            ilmumise_aeg += dt
            leveli_aeg += dt

            # Stipendiumi ilmumine pärast 10 sekundit
            if leveli_aeg >= 10 and not stipp_ilmunud:
                stipendium = Ese("stipp", 0, -40)
                stipendium.rect.x = random.randint(
                    0, LAIUS - stipendium.rect.width
                )
                esemed.append(stipendium)
                stipp_ilmunud = True

            # Uue eseme genereerimine iga sekundi järel
            if ilmumise_aeg >= 1.0:
                liik = random.choices(
                    ["kell", "kodutöö", "eksam", "kohv", "redbull"],
                    weights=[30, 25, 15, 15, 15],
                    k=1
                )[0]

                uus_ese = Ese(liik, 0, -90)

                # Enamik takistusi suunatakse mängija poole
                if uus_ese.punktid < 0 and random.random() < 0.75:
                    x = mangija.rect.centerx - uus_ese.rect.width // 2
                else:
                    x = random.randint(0, LAIUS - uus_ese.rect.width)

                uus_ese.rect.x = max(0, min(x, LAIUS - uus_ese.rect.width))
                esemed.append(uus_ese)
                ilmumise_aeg = 0

            # Esemete liigutamine ja joonistamine
            for ese in esemed[:]:
                ese.liiguta(300, dt)
                ese.joonista(ekraan)

                if ese.ekraanilt_valjas():
                    esemed.remove(ese)

            # Kokkupõrgete kontroll
            muutus, uus_teade = kontrolli_kokkuporkeid(
                mangija.rect, esemed
            )

            punktid += muutus

            if uus_teade is not None:
                teade = uus_teade
                teate_lopp = pygame.time.get_ticks() + 1000

                if muutus >= 0:
                    teate_varv = ROHELINE
                else:
                    teate_varv = PUNANE
                    mangija.kaota_elu()

            # Mängija joonistamine
            mangija.joonista(ekraan)

            # Mängu lõpu kontroll
            if mangija.elud <= 0:
                mang_labi = True

            # --- VISUAALNE PÄIS (HUD Paneel ekraani ülaosas) ---
            pygame.draw.rect(ekraan, (30, 30, 30), (0, 0, LAIUS, 120))
            pygame.draw.line(ekraan, VALGE, (0, 120), (LAIUS, 120), 2)

            punktide_tekst = font.render(f"Punktid: {punktid}", True, VALGE)
            elude_tekst = font.render(f"Elud: {mangija.elud}", True, VALGE)

            ekraan.blit(punktide_tekst, (20, 15))
            ekraan.blit(elude_tekst, (20, 50))

            if pygame.time.get_ticks() < teate_lopp:
                teate_tekst = font.render(teade, True, teate_varv)
                ekraan.blit(teate_tekst, (20, 85))

        else:
            # Mängu lõpu ekraan
            lopp_tekst = suur_font.render("MÄNG LÄBI!", True, PUNANE)
            punkt_tekst = font.render(f"Lõppskoor: {punktid}", True, VALGE)
            uuesti_tekst = font.render("Vajuta R, et uuesti alustada", True, VALGE)

            ekraan.blit(
                lopp_tekst,
                lopp_tekst.get_rect(center=(LAIUS // 2, KÕRGUS // 2 - 60))
            )
            ekraan.blit(
                punkt_tekst,
                punkt_tekst.get_rect(center=(LAIUS // 2, KÕRGUS // 2))
            )
            ekraan.blit(
                uuesti_tekst,
                uuesti_tekst.get_rect(center=(LAIUS // 2, KÕRGUS // 2 + 60))
            )

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()