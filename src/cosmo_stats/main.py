import typer

from cosmo_stats.objekts.commands import app as objekts_app

app = typer.Typer(no_args_is_help=True)

app.add_typer(objekts_app, name="objekts")


if __name__ == "__main__":
    app()
