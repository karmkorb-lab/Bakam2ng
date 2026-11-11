"""
Projekt: Bakamäng
Autorid: Merilin-Grete Kakko, Karm Korb
Fail: seaded.py

Kirjeldus:
Siia faili tuleb kood mängija käitumise kohta mängus.
"""

import pygame

from seaded import *

class Mangija:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, MANGIJA_LAIUS, MANGIJA_KORGUS)
        self.varv = ROHELINE
        self.kiirus = MANGIJA_KIIRUS
        self.elud = 3

    def kasitle_sisendit(self):
        klahvid = pygame.key.get_pressed()

        if klahvid[pygame.K_a] or klahvid[pygame.K_LEFT]:
            self.rect.x -= self.kiirus
        elif klahvid[pygame.K_d] or klahvid[pygame.K_RIGHT]:
            self.rect.x += self.kiirus
        elif klahvid[pygame.K_w] or klahvid[pygame.K_UP]:
            self.rect.y -= self.kiirus
        elif klahvid[pygame.K_s] or klahvid[pygame.K_DOWN]:
            self.rect.y += self.kiirus

    def piira_liikumist(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LAIUS:
            self.rect.right = LAIUS
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > KÕRGUS:
            self.rect.bottom = KÕRGUS

    def uuenda(self):
        self.kasitle_sisendit()
        self.piira_liikumist()

    def joonista(self, ekraan):
        pygame.draw.rect(ekraan, self.varv, self.rect)


    def kaota_elu(self):
        self.elud -= 1

    def lisa_elu(self):
        if self.elud < MAX_ELUD:
            self.elud += 1

    def algseadista(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.elud = 3






