def kontrolli_kokkuporkeid(mangija_rect, esemed):
    """Kontrollib mängija kokkupõrkeid esemetega.

    Tagastab kokkupõrgetest saadud või kaotatud punktid.
    """
    punktide_muutus = 0

    for ese in esemed[:]:
        if mangija_rect.colliderect(ese.rect):
            punktide_muutus += ese.punktid
            esemed.remove(ese)

    return punktide_muutus
