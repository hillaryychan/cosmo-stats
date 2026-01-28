from dataclasses import dataclass

from cosmo_stats.enums.cosmo import Member, Season


@dataclass
class Objekt:
    season: Season
    member: Member
    collection_no: str
    total: int = 0

    @property
    def slug(self) -> str:
        return f"{self.season.slug}-{self.member.slug}-{self.collection_no}".lower()
