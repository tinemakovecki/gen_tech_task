# Package for Genialis tech task

The package helps a user retrieve gene expression data from Genialis server and use it to calculate metrics (ie. **progeny**), it also includes a CLI for easier use. It was developed for a Genialis technical task. 

## Installation

To install the package, clone the repository and
```
$ pip install .
```

## Quick start

Call a function with a dataset names as an argument, ie.
```
$ progeny windrem-et-al-cell-2017
```
This retireves the dataset from Genialis server and prints out calculated scores into a table.