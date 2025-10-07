from enum import StrEnum

from cosmo_stats.enums.cosmo import Season


class ArtmsSeason(Season):
    ATOM01 = "Atom01"
    BINARY01 = "Binary01"
    CREAM01 = "Cream01"
    DIVINE01 = "Divine01"


class ArtmsObjektClass(StrEnum):
    DOUBLE = "Double"
    FIRST = "First"
    PREMIER = "Premier"
    SPECIAL = "Special"
    WELCOME = "Welcome"
