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
    ATOM02 = "Atom02"


class Edition(StrEnum):
    FIRST = "1"
    SECOND = "2"
    THIRD = "3"

    @staticmethod
    def collection_no_map() -> dict[str, str]:
        return {
            "1": "101Z,102Z,103Z,104Z,105Z,106Z,107Z,108Z",
            "2": "109Z,110Z,111Z,112Z,113Z,114Z,115Z,116Z",
            "3": "117Z,118Z,119Z,120Z",
        }

    @property
    def collection_no(self) -> str | None:
        return self.collection_no_map().get(self.value, None)


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
