"""
Projekt: Bakamäng
Autorid: Merilin-Grete Kakko, Karm Korb
Fail: punktid.py

Kirjeldus:
Moodul sisaldab mängija ja esemete kokkupõrgete kontrollimist
ning kokkupõrgetest saadud või kaotatud punktide arvestust.
Tagastab punktide muutuse ja vastava teate mängijale.
"""

def kontrolli_kokkuporkeid(mangija_rect, esemed):
    """Kontrollib kokkupõrkeid ja tagastab punktid ning teate."""
    punktide_muutus = 0
    teade = None

    for ese in esemed[:]:
        if mangija_rect.colliderect(ese.rect):
            punktide_muutus += ese.punktid

            # Näiteks: "Kohv: +15"
            teade = f"{ese.nimi}: {ese.punktid:+d}"

            esemed.remove(ese)

    return punktide_muutus, teade