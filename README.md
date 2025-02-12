# Tafel

A command-line tool for extracting Tafel slopes from MPT files.

This tool is currently in an experimental stage.

## How to install

Requirements: Python 3.11 or above

```
pip install tafel
```

## How to use

```
tafel -f path/to/mpt/file.mpt --reference-potential 0.210 --ph 13 --electrolyte-resistance 0.05
```


## For developers

### Getting started

```
pdm install
```

### Check code quality

```
pdm run check
```
