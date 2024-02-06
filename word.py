import csv
import logging
import re

from typing import Dict

from pandas.core.frame import DataFrame
from pandas.core.frame import Series

from helpers import Kind
from helpers import ENCODING
from helpers import ResourcePaths
from helpers import get_resource_paths_ru

import sys
sys.path.append("/home/deva/Documents/dpd-db") # https://github.com/digitalpalidictionary/dpd-db

from tools.link_generator import generate_link


_LOGGER = logging.getLogger(__name__)


class DpsRuWord:
    abbreviations_ru = None

    def __init__(self, df: DataFrame, row: int):
        if DpsRuWord.abbreviations_ru is None:
            DpsRuWord.abbreviations_ru = _load_abbrebiations_ru(rsc=get_resource_paths_ru())  # TODO Pass rsc

        self.pali: str = df.loc[row, 'pali_1']
        self.pali_: str = '_' + re.sub(' ', '_', self.pali)
        self.pali_clean: str = re.sub(r' \d*$', '', self.pali)
        # self.fin: str = df.loc[row, 'Fin']
        self.pos: str = df.loc[row, 'pos']
        # Keeps initial value even after translate_abbreviations() call
        self.pos_orig: str = self.pos
        self.grammar: str = df.loc[row, 'grammar']
        self.derived_from: str = df.loc[row, 'derived_from']
        self.neg: str = df.loc[row, 'neg']
        self.verb: str = df.loc[row, 'verb']
        self.trans: str = df.loc[row, 'trans']
        self.plus_case: str = df.loc[row, 'plus_case']
        self.meaning_1: str = df.loc[row, 'meaning_1']
        self.meaning_2: str = df.loc[row, 'meaning_2']
        self.meaning_lit: str = df.loc[row, 'meaning_lit']

        if self.meaning_lit and not self.meaning_1:
            lit_index = self.meaning_2.find("; lit.")
            if lit_index != -1:
                self.meaning_2 = self.meaning_2[:lit_index]
        
        self.ru_meaning: str = df.loc[row, 'ru_meaning']
        self.ru_meaning_lit: str = df.loc[row, 'ru_meaning_lit']
        self.sbs_meaning: str = df.loc[row, 'sbs_meaning']
        self.sanskrit: str = df.loc[row, 'sanskrit']
        self.sanskrit_root: str = df.loc[row, 'sanskrit_root']
        self.sanskrit_root_meaning: str = df.loc[row, 'sanskrit_root_meaning']
        self.sanskrit_root_class: str = df.loc[row, 'sanskrit_root_class']
        self.root: str = df.loc[row, 'root']
        self.root_group: str = df.loc[row, 'root_group']
        self.root_sign: str = df.loc[row, 'root_sign']
        self.root_meaning: str = df.loc[row, 'root_meaning']
        self.root_base: str = df.loc[row, 'root_base']
        self.construction: str = df.loc[row, 'construction']
        self.derivative: str = df.loc[row, 'derivative']
        self.suffix: str = df.loc[row, 'suffix']
        self.phonetic: str = df.loc[row, 'phonetic']
        self.compound_type: str = df.loc[row, 'compound_type']
        self.compound_construction: str = df.loc[row, 'compound_construction']
        self.source_1: str = df.loc[row, 'source_1']
        self.sutta_1: str = df.loc[row, 'sutta_1']
        self.example_1: str = df.loc[row, 'example_1']
        self.source_2: str = df.loc[row, 'source_2']
        self.sutta_2: str = df.loc[row, 'sutta_2']
        self.example_2: str = df.loc[row, 'example_2']

        self.sbs_source_1: str = df.loc[row, 'sbs_source_1']
        self.sbs_sutta_1: str = df.loc[row, 'sbs_sutta_1']
        self.sbs_example_1: str = df.loc[row, 'sbs_example_1']

        self.sbs_chant_pali_1: str = df.loc[row, 'sbs_chant_pali_1']
        self.sbs_chant_eng_1: str = df.loc[row, 'sbs_chant_eng_1']
        self.sbs_chapter_1: str = df.loc[row, 'sbs_chapter_1']

        self.sbs_source_2: str = df.loc[row, 'sbs_source_2']
        self.sbs_sutta_2: str = df.loc[row, 'sbs_sutta_2']
        self.sbs_example_2: str = df.loc[row, 'sbs_example_2']

        self.sbs_chant_pali_2: str = df.loc[row, 'sbs_chant_pali_2']
        self.sbs_chant_eng_2: str = df.loc[row, 'sbs_chant_eng_2']
        self.sbs_chapter_2: str = df.loc[row, 'sbs_chapter_2']
        self.sbs_source_3: str = df.loc[row, 'sbs_source_3']
        self.sbs_sutta_3: str = df.loc[row, 'sbs_sutta_3']
        self.sbs_example_3: str = df.loc[row, 'sbs_example_3']
        self.sbs_chant_pali_3: str = df.loc[row, 'sbs_chant_pali_3']
        self.sbs_chant_eng_3: str = df.loc[row, 'sbs_chant_eng_3']
        self.sbs_chapter_3: str = df.loc[row, 'sbs_chapter_3']
        self.sbs_source_4: str = df.loc[row, 'sbs_source_4']
        self.sbs_sutta_4: str = df.loc[row, 'sbs_sutta_4']
        self.sbs_example_4: str = df.loc[row, 'sbs_example_4']
        self.sbs_chant_pali_4: str = df.loc[row, 'sbs_chant_pali_4']
        self.sbs_chant_eng_4: str = df.loc[row, 'sbs_chant_eng_4']
        self.sbs_chapter_4: str = df.loc[row, 'sbs_chapter_4']
        self.sbs_index: str = df.loc[row, 'sbs_index']

        self.antonym: str = df.loc[row, 'antonym']
        self.synonym: str = df.loc[row, 'synonym']
        
        self.variant: str = df.loc[row, 'variant']
        self.commentary: str = re.sub(r'(.+)\.$', '\\1', df.loc[row, 'commentary'])
        self.notes: str = df.loc[row, 'notes']
        self.sbs_notes: str = df.loc[row, 'sbs_notes']
        self.ru_notes: str = df.loc[row, 'ru_notes']
        self.stem: str = df.loc[row, 'stem']

        self.pattern: str = df.loc[row, 'pattern']
        self.link: str = df.loc[row, 'link']

        self.id: int = df.loc[row, 'id']
        self.sbs_category: str = df.loc[row, 'sbs_category']
        self.sbs_class_anki: int = df.loc[row, 'sbs_class_anki']
        self.sbs_class: int = df.loc[row, 'sbs_class']

        self.sbs_link_1: str = df.loc[row, 'sbs_link_1']
        self.sbs_link_2: str = df.loc[row, 'sbs_link_2']
        self.sbs_link_3: str = df.loc[row, 'sbs_link_3']
        self.sbs_link_4: str = df.loc[row, 'sbs_link_4']

        self.class_link: str = df.loc[row, 'class_link']
        self.sutta_link: str = df.loc[row, 'sutta_link']

        self.source_link_1: str = generate_link(self.source_1) if self.source_1 else ""
        self.source_link_2: str = generate_link(self.source_2) if self.source_2 else ""

        self.sbs_source_link_1: str = generate_link(self.sbs_source_1) if self.sbs_source_1 else ""
        self.sbs_source_link_2: str = generate_link(self.sbs_source_2) if self.sbs_source_2 else ""
        self.sbs_source_link_3: str = generate_link(self.sbs_source_3) if self.sbs_source_3 else ""
        self.sbs_source_link_4: str = generate_link(self.sbs_source_4) if self.sbs_source_4 else ""

    

    def translate_abbreviations(self) -> None:
        # TODO Cache
        # TODO Process by lexems
        targets = [
            'pos',
            'neg',
            'verb',
            'trans',
            'plus_case',
        ]

        for field in targets:
            for abbrev, translation in self.abbreviations_ru.items():
                val = getattr(self, field)
                setattr(self, field, val.replace(abbrev, translation))


class AbbreviationEntry:
    def __init__(self, kind: Kind, series: Series):
        self.abbrev = series.iloc[0]
        self.en_abbrev = series.iloc[0]
        self.meaning = series.iloc[1]
        self.en_meaning = series.iloc[1]
        self.pali_meaning = series.iloc[2]
        self.ru_meaning = series.iloc[3]
        ru_meaning = series.iloc[3]
        self.example = series.iloc[4]
        self.explanation = series.iloc[5]
        self.ru_abbrev = series.iloc[6]
        ru_abbrev = series.iloc[6]

        if kind == Kind.RU or kind == Kind.DPS:
            if ru_abbrev:
                self.abbrev = ru_abbrev

            if ru_meaning:
                self.meaning = ru_meaning

    def __str__(self) -> str:
        return self.abbrev


def _load_abbrebiations_ru(rsc: ResourcePaths) -> Dict[str, str]:
    result = {}
    sorted_result = {}

    with open('./assets/abbreviations.csv', 'r', encoding=ENCODING) as abbrev_csv:
        reader = csv.reader(abbrev_csv, delimiter='\t')
        header = next(reader)  # Skip header
        _LOGGER.debug('Skipping abbreviations header %s', header)
        for row in reader:
            assert len(row) == 7, f'Expected 7 items in a row {row}'
            if row[6]:
                result[row[0]] = row[6]

    # Sort resulting dict from longer to shorter keys to match then long lexems first
    for key in sorted(result, key=len, reverse=True):
        sorted_result[key] = result[key]

    _LOGGER.debug('Got En-Ru abbreviations dict: %s', sorted_result)
    return sorted_result
