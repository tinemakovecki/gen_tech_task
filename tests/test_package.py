import decoupler as dc
import numpy as np
import pandas as pd
import resdk
from resdk.tables import RNATables
from gen_tech_task import data_process, cli


def test_hline_formatting():
    assert cli.format_hline(length=3) == "___"
    assert cli.format_hline(length=2, border="|") == "|__|"
    assert cli.format_hline(length=5, border=" ") == " _____ "


def test_progeny():

    progeny = dc.get_progeny(organism='human')
    targets = list(progeny.target.unique())
    n_sources = len(progeny.source.unique())
    n_targets = len(targets)
    n_samples = 30

    dummy_data = np.random.default_rng().random((n_samples, n_targets))
    mat_test = pd.DataFrame(data=dummy_data, columns=targets)
    estimate = data_process.calculate_progeny(mat_test)

    assert estimate.shape == (n_samples, n_sources)


def test_expression_extraction():

    res = resdk.Resolwe(url='https://app.genialis.com')
    resdk.start_logging() # Enable verbose logging to standard output
    collection = res.collection.get(slug='windrem-et-al-cell-2017')

    tables = RNATables(collection)
    exp = tables.exp
    expected_targets = set(tables.readable_columns.values())

    gene_expressions = data_process.exp_from_collection(collection)
    output_targets = set(gene_expressions.columns)

    assert expected_targets == output_targets


if __name__ == "__main__":
    test_expression_extraction()