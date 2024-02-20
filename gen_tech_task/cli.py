import click
from pandas import DataFrame
from .data_process import get_gene_expressions, calculate_progeny


def format_hline(length: int, border="") -> str:
    """Format and return horizontal line."""
    return border + ("_" * length) + border


def lookup_err_msg(used_login: bool) -> None:
    """Show neat lookup error message to user."""

    click.echo("Lookup Error: No collection with given name was found.")
    if not used_login:
        click.echo("You used guest access. More collections are avaliable with credentials.")
        click.echo("Use '--login True' flag to login to server.")


def show_scores(scores: DataFrame) -> None:
    """Format and output scores to terminal."""

    n_cols = len(scores.columns)
    row_length = 11 * n_cols - 1
    horizontal_line = format_hline(row_length, border=" ")

    click.echo(horizontal_line)

    # headers
    for col_name in scores.columns:
        click.echo("|" + f"{col_name:<10}", nl=False)
    click.echo("|")

    horizontal_line = format_hline(row_length, border="|")
    click.echo(horizontal_line)

    # score table
    for index, row in scores.iterrows():
        for val in row:
            short_val = f"{val:.6f}"
            click.echo("|" + f"{short_val:<10}", nl=False)
        click.echo("|")

    click.echo(horizontal_line)


@click.group()
def cli():
    pass


@cli.command()
@click.argument("file")
@click.option("-l", "--login", type=click.BOOL, default=False)
def progeny(file: str, login: bool) -> None:
    """Fetch gene expressions, calculate and show progeny scores."""

    try:
        gene_expressions = get_gene_expressions(file, use_login=login)
        prog_scores = calculate_progeny(gene_expressions)
        show_scores(prog_scores)

    except LookupError as err:
        lookup_err_msg(used_login=login)


if __name__ == "__main__":
    cli()
