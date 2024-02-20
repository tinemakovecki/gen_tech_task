import decoupler as dc
import resdk
from pandas import DataFrame
from resdk.resources import Collection
from resdk.tables import RNATables


def exp_from_collection(collection: Collection) -> RNATables:
    """Create and inspect RNA table from collection."""

    tables = RNATables(collection)

    # Rename column names (gene ID's) to gene symbols
    exp = tables.exp
    assert exp.attrs["exp_type"] == "TPM"
    exp.columns = list(map(str, exp.columns))
    exp = tables.exp.rename(columns=tables.readable_columns)

    return exp


def get_gene_expressions(dataset_name: str, use_login=False) -> DataFrame:
    """Get collection from Genialis server and extract gene expressions data."""

    res = resdk.Resolwe(url="https://app.genialis.com")
    resdk.start_logging()  # Enable verbose logging to standard output

    if use_login:
        res.login()

    collection = res.collection.get(slug=dataset_name)
    gene_expressions = exp_from_collection(collection)

    return gene_expressions


def calculate_progeny(gene_data: DataFrame) -> DataFrame:
    """Calculate progeny scores for gene expressions data."""

    # retrieve progeny model to use as net
    progeny = dc.get_progeny(organism="human")

    # fit model to infer pathway enrichment scores
    estimate, pvals = dc.run_mlm(
        mat=gene_data, net=progeny, source="source", target="target", weight="weight", verbose=True
    )

    return estimate


if __name__ == "__main__":

    gene_expressions = get_gene_expressions("windrem-et-al-cell-2017")
    prog_scores = calculate_progeny(gene_expressions)

    print(prog_scores)
