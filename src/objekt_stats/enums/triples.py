from enum import StrEnum

from objekt_stats.enums.cosmo import Season


class TripleSSeason(Season):
    ATOM01 = "Atom01"
    BINARY01 = "Binary01"
    CREAM01 = "Cream01"
    DIVINE01 = "Divine01"
    EVER01 = "Ever01"
    ATOM02 = "Atom02"


class TripleSObjektClass(StrEnum):
    DOUBLE = "Double"
    FIRST = "First"
    PREMIER = "Premier"
    SPECIAL = "Special"
    WELCOME = "Welcome"
    ZERO = "Zero"
