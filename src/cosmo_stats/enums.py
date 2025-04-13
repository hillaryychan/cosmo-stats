from enum import StrEnum


class Artist(StrEnum):
    TRIPLES = "tripleS"
    ARTMS = "artms"


class Season(StrEnum):
    ATOM01 = "Atom01"
    BINARY01 = "Binary01"
    CREAM01 = "Cream01"
    DIVINE01 = "Divine01"
    EVER01 = "Ever01"


class ObjektClass(StrEnum):
    FIRST = "First"
    SPECIAL = "Special"
    DOUBLE = "Double"
    PREMIER = "Premier"
    WELCOME = "Welcome"
    ZERO = "Zero"


class TripleSMember(StrEnum):
    SEOYEON = "SeoYeon"
    HYERIN = "HyeRin"
    JIWOO = "JiWoo"
    CHAEYEON = "ChaeYeon"
    YOOYEON = "YooYeon"
    SOOMIN = "SooMin"
    NAKYOUNG = "NaKyoung"
    YUBIN = "YuBin"
    KAEDE = "Kaede"
    DAHYUN = "DaHyun"
    KOTONE = "Kotone"
    YEONJI = "YeonJi"
    NIEN = "Nien"
    SOHYUN = "SoHyun"
    XINYU = "Xinyu"
    MAYU = "Mayu"
    LYNN = "Lynn"
    JOOBIN = "JooBin"
    HAYEON = "HaYeon"
    SHION = "ShiOn"
    CHAEWON = "ChaeWon"
    SULLIN = "Sullin"
    SEOAH = "SeoAh"
    JIYEON = "JiYeon"


class ArtmsMember(StrEnum):
    HEEJIN = "HeeJin"
    HASEUL = "HaSeul"
    KIMLIP = "KimLip"
    JINSOUL = "JinSoul"
    CHOERRY = "Choerry"


class StatsOutput(StrEnum):
    TERM = "term"
    CSV = "csv"
    HTML = "html"
    JSON = "json"
