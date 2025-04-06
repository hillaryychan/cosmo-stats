from cosmo_stats.enums import Season
from cosmo_stats.objekts.utils import (
    get_objekt_data,
    get_objekt_sales_stats,
    get_objekts,
)


def main() -> None:
    objekts = get_objekts(Season.EVER01, ["117Z", "118Z", "119Z", "120Z"])
    objekt_data = get_objekt_data(objekts)
    stats = get_objekt_sales_stats(objekt_data)
    print(stats)
