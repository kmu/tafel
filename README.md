
[![Python application](https://github.com/kmu/tafel/actions/workflows/test.yaml/badge.svg)](https://github.com/kmu/tafel/actions/workflows/test.yaml)

# Tafel


A command-line tool for extracting Tafel slopes from MPT files.

This tool is currently in an experimental stage.

## Supported files

- csv files: see `dataset` for the supported format.
- mpt files: assumes LSV experiments conducted using BioLogic EC-Lab.

## Installation

Requirements: Python 3.11 or above

```bash
pip install tafel
```

## How to use

```bash
tafel -f dataset/HER.csv
```

## For Developers

### Getting Started

To set up the development environment, run:

```bash
pdm install
```

### Code Quality Check

To check the code quality, run:

```bash
pdm run check
```

To test CLI, run

```
pdm run python src/tafel/app/cli.py -f dataset/HER.csv
```

### Release a New PyPI Package

To release a new version, update the `pyproject.toml` file with the new version number and publish a new release from [here](https://github.com/kmu/tafel/releases/new).
