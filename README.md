# Objekt Stats

Objekt Stats is a command line tool that retrieves the total no. of Objekt minted
for members of a MODHAUS group.

## Installation

Installation via [pipx](https://pipx.pypa.io/stable/) is recommended.

Via Git repository:

```sh
pipx install git+https://github.com/hillaryychan/objekt-stats.git@main
```

Check that Objekt Stats is available by running the `objekt-stats` command:

```sh
objekt-stats --help
```

## Usage

The basic usage of `objekt-stats` requires the artist, season and collection numbers of the objekts:

```sh
objekt-stats tripleS atom02 --collection-no 101z,102z,103z,104z,105z,106z,107z,108z
```

Each season has three editions. The collection numbers remain constant for each edition, so there is
an alias argument that can be used when retrieving data for Objekts from editions:

```sh
objekt-stats tripleS atom02 --edition 1
```

If you do not provide a collection number or edition, `objekt-stats` will retrieve data for **all**
Objekts for the season. This is not recommended as you may get rate limited.
