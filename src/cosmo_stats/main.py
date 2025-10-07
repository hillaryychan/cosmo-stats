import typer

from cosmo_stats.commands import objekts

app = typer.Typer(no_args_is_help=True)

app.add_typer(objekts.app, name="objekts")


if __name__ == "__main__":
    app()
