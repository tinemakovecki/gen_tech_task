import click
from pandas import DataFrame
from .data_process import get_gene_expressions, calculate_progeny


def format_hline(length: int, border="") -> str:
    """Format and return horizontal line."""
    return border + ("_" * length) + border


def show_scores(scores: DataFrame) -> None:
    """Format and output scores to terminal."""

    n_cols = len(scores.columns)
    row_length = 11*n_cols - 1
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
def progeny(file: str) -> None:
    """Fetch gene expressions and return progeny scores."""

    gene_expressions = get_gene_expressions(file)
    prog_scores = calculate_progeny(gene_expressions)
    show_scores(prog_scores)


if __name__ == "__main__":
    cli()