#!/usr/bin/env python3
# coding: utf-8

import io
import json
import logging

import rich
import rich.logging
import typer

from generate_html_and_json import generate_html_and_json
from helpers import ENCODING
from helpers import ResourcePaths
from helpers import copy_goldendict
from helpers import get_resource_paths_ru
from helpers import get_resource_paths_sbs
from helpers import get_resource_paths_dps
from helpers import timeis, line  # TODO Use logging with the rich.logging.RichHandler for messages



app = typer.Typer()

RSC = get_resource_paths_ru()


@app.command()
def run_generate_html_and_json(generate_roots: bool = True):
    rsc = get_resource_paths_ru()
    generate_html_and_json(
        rsc=rsc,
        generate_roots=generate_roots)


@app.command()
def run_generate_html_and_json_dps(generate_roots: bool = True):
    rsc = get_resource_paths_dps()
    generate_html_and_json(
        rsc=rsc,
        generate_roots=generate_roots)


@app.command()
def run_generate_html_and_json_sbs(generate_roots: bool = True):
    rsc = get_resource_paths_sbs()
    generate_html_and_json(
        rsc=rsc,
        generate_roots=generate_roots)


def _run_generate_goldendict(rsc: ResourcePaths, ifo: 'StarDictIfo', move_to_dest: bool = True):
    """Generate a Stardict-format .zip for GoldenDict."""

    # importing Simsapa here so other commands don't have to load it and its numerous dependencies
    from stardict_nu import export_words_as_stardict_zip, DictEntry

    rich.print(f"{timeis()} [yellow]generate goldendict")
    rich.print(f"{timeis()} {line()}")

    rich.print(f"{timeis()} [green]reading json")

    with open(rsc['gd_json_path'], "r", encoding=ENCODING) as f:
        gd_data_read = json.load(f)

    rich.print(f"{timeis()} [green]parsing json")

    def item_to_word(x):
        return DictEntry(
            word=x["word"],
            definition_html=x["definition_html"],
            definition_plain=x["definition_plain"],
            synonyms=x["synonyms"],
        )

    words = list(map(item_to_word, gd_data_read))

    rich.print(f"{timeis()} [green]writing goldendict")
    export_words_as_stardict_zip(words, ifo, rsc['output_stardict_zip_path'], rsc['icon_path'])
    print(f"saved into {rsc['output_stardict_zip_path']}")

    if move_to_dest:
        copy_goldendict(rsc['output_stardict_zip_path'], rsc['output_share_dir'])
        print(f"moved into {rsc['output_share_dir']}")


    rich.print(f"{timeis()} {line()}")


@app.command()
def run_generate_goldendict(move_to_dest: bool = True):
    from stardict_nu import ifo_from_opts, StarDictIfo

    rsc = get_resource_paths_ru()

    ifo = ifo_from_opts({
            "bookname": "Пали Словарь",
            "author": "Бхиккху Дэвамитта",
            "description": "Пали Словарь",
            "website": "devamitta.github.io/pali/",
    })

    return _run_generate_goldendict(rsc, ifo, move_to_dest)


@app.command()
def run_generate_goldendict_dps(move_to_dest: bool = True):
    from stardict_nu import ifo_from_opts, StarDictIfo

    rsc = get_resource_paths_dps()

    ifo = ifo_from_opts({
            "bookname": "DPS",
            "author": "Devamitta",
            "description": "work in progress",
            "website": "",
    })

    return _run_generate_goldendict(rsc, ifo, move_to_dest)


@app.command()
def run_generate_goldendict_sbs(move_to_dest: bool = True):
    from stardict_nu import ifo_from_opts, StarDictIfo

    rsc = get_resource_paths_sbs()

    ifo = ifo_from_opts({
        "bookname": "SBS Pāḷi Dictionary",
        "author": "Devamitta Bhikkhu",
        "description": "words from the SBS Pāḷi-English Recitation an other Pāḷi study tools",
        "email": "sasanarakkha.org",
    })

    return _run_generate_goldendict(rsc, ifo, move_to_dest)


def _exit_callback(profile: 'cProfile.Profile') -> None:
    """ Print profiling statistics on exit """
    profile.disable()
    stat_stream = io.StringIO()
    stats = pstats.Stats(profile, stream=stat_stream).sort_stats('tottime').reverse_order()
    stats.print_stats()
    print(stat_stream.getvalue())


@app.callback()
def main(log_level: str = 'info', profiling: bool = False):
    """ The main() callback uses to define additional CLI options """
    handler = rich.logging.RichHandler()
    formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)s %(message)s',
        style='%',
        datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(log_level.upper())
    logger.addHandler(handler)

    if profiling:
        profile = cProfile.Profile()
        profile.enable()
        atexit.register(_exit_callback, profile)


if __name__ == "__main__":
    import atexit
    import cProfile
    import pstats

    app()
