"""
Projekt: Bakamäng
Autorid: Merilin-Grete Kakko, Karm Korb
Fail: esemed.py

Kirjeldus:
See moodul sisaldab mängus kasutatavate takistuste
ja booster'ite andmeid ning Ese klassi, mis võimaldab
esemeid luua, liigutada ja ekraanile joonistada.

Kasutatud vahendid:
- Python
- Pygame

AI kasutamine:
Ese klassi esialgse ülesehituse loomisel kasutati
ChatGPT abi. Koodi katsetati ja kohandati projekti jaoks.
"""

import pygame
from seaded import KÕRGUS

import pygame
from seaded import KÕRGUS

ESEMED = {
  "kell": {
    "nimi": "Kellakeeramine",
    "punktid": -10,
    "värv": (255, 200, 50)
  },
  "kodutöö": {
      "nimi": "Hilinenud kodutöö",
      "punktid": -25,
      "värv": (255, 130, 50)
  },
  "eksam": {
      "nimi": "Läbikukutud eksam",
      "punktid": -50,
      "värv": (230, 60, 60)
  },
  "kohv": {
      "nimi": "Kohv",
      "punktid": 15,
      "värv": (80, 190, 110)
  },
  "redbull": {
      "nimi": "RedBull",
      "punktid": 15,
      "värv": (60, 150, 240)
  },
  "stipp": {
      "nimi": "Stipendium",
      "punktid": 100,
      "värv": (220, 170, 255)
  }
}

class Ese:
  """Mängus kasutatav takistus või boonusese."""

  def __init__(self, liik, x, y):
    """Loob eseme ning määrab selle omadused ja asukoha."""

    andmed = ESEMED[liik]

    self.liik = liik
    self.nimi = andmed["nimi"]
    self.punktid = andmed["punktid"]
    self.varv = andmed["värv"]

    # Eseme suurus ja asukoht
    # Takistused on suuremad kui booster'id
    if self.punktid < 0:
        suurus = 90
    else:
        suurus = 40

    self.rect = pygame.Rect(x, y, suurus, suurus)
    
    self.y = float(y)

  def liiguta(self, kiirus, dt):
    """Liigutab eset allapoole vastavalt kiirusele ja ajale."""

    self.y += kiirus * dt
    self.rect.y = round(self.y)

  def joonista(self, ekraan):
    """Joonistab eseme mänguaknasse."""

    pygame.draw.rect(
        ekraan,
        self.varv,
        self.rect
    )

  def ekraanilt_valjas(self):
    """Kontrollib, kas ese on mänguaknast väljunud."""

    return self.rect.top > KÕRGUS
