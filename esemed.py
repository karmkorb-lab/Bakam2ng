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
  def __init__(self, liik, x, y):
    andmed = ESEMED[liik]

    self.liik = liik
    self.nimi = andmed["nimi"]
    self.punktid = andmed["punktid"]
    self.varv = andmed["värv"]

    # Eseme suurus ja asukoht
    self.rect = pygame.Rect(x, y, 50, 50)
    self.y = float(y)

  def liiguta(self, kiirus, dt):
    # Liigutame eset allapoole
    self.y += kiirus * dt
    self.rect.y = round(self.y)

  def joonista(self, ekraan):
    # Joonistame eseme ekraanile
    pygame.draw.rect(
        ekraan,
        self.varv,
        self.rect
    )

  def ekraanilt_valjas(self):
      return self.rect.top > KÕRGUS
