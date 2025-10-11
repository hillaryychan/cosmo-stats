from enum import StrEnum


class Artist(StrEnum):
    TRIPLES = "tripleS"
    ARTMS = "artms"
    IDNTT = "idntt"


class Season(StrEnum):
    """The base season enum as every artist has different seasons."""


class Edition(StrEnum):
    FIRST = "1"
    SECOND = "2"
    THIRD = "3"

    @staticmethod
    def collection_no_map() -> dict[str, list[str]]:
        return {
            "1": ["101Z", "102Z", "103Z", "104Z", "105Z", "106Z", "107Z", "108Z"],
            "2": ["109Z", "110Z", "111Z", "112Z", "113Z", "114Z", "115Z", "116Z"],
            "3": ["117Z", "118Z", "119Z", "120Z"],
        }

    @property
    def collection_no(self) -> list[str] | None:
        return self.collection_no_map().get(self.value, None)
