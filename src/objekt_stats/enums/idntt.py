from enum import StrEnum

from objekt_stats.enums.cosmo import Season


class IdnttSeason(Season):
    SPRING25 = "Spring25"
    SUMMER25 = "Summer25"


class IdnttObjektClass(StrEnum):
    EVENT = "Event"
    WELCOME = "Welcome"
