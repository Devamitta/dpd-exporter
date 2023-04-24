import csv
import logging
import re

from typing import Dict

from pandas.core.frame import DataFrame
from pandas.core.frame import Series

from helpers import Kind
from helpers import ENCODING
from helpers import ResourcePaths
from helpers import get_resource_paths_dps_ru

_LOGGER = logging.getLogger(__name__)

class DpsRuWord:
    abbreviations_ru = None

    def __init__(self, df: DataFrame, row: int):
        if DpsRuWord.abbreviations_ru is None:
            DpsRuWord.abbreviations_ru = _load_abbrebiations_ru(rsc=get_resource_paths_dps_ru())  # TODO Pass rsc

        self.pali: str = df.loc[row, 'pali_1']
        self.pali_: str = '_' + re.sub(' ', '_', self.pali)
        self.pali_clean: str = re.sub(r' \d*$', '', self.pali)
        self.fin: str = df.loc[row, 'Fin']
        self.pos: str = df.loc[row, 'pos']
        # Keeps initial value even after translate_abbreviations() call
        self.pos_orig: str = self.pos
        self.grammar: str = df.loc[row, 'grammar']
        self.derived: str = df.loc[row, 'derived_from']
        self.neg: str = df.loc[row, 'neg']
        self.verb: str = df.loc[row, 'verb']
        self.trans: str = df.loc[row, 'trans']
        self.case: str = df.loc[row, 'plus_case']
        self.meaning: str = df.loc[row, 'meaning_1']
        self.russian: str = df.loc[row, 'ru_meaning']
        self.sbs_meaning: str = df.loc[row, 'sbs_meaning']
        self.sk: str = df.loc[row, 'sanskrit']
        self.sk_root: str = df.loc[row, 'root_sk']
        self.root: str = df.loc[row, 'root_pali']
        self.base: str = df.loc[row, 'root_base']
        self.construction: str = df.loc[row, 'construction']
        self.derivative: str = df.loc[row, 'derivative']
        self.suffix: str = df.loc[row, 'suffix']
        self.pc: str = df.loc[row, 'phonetic']
        self.comp: str = df.loc[row, 'compound_type']
        self.comp_constr: str = df.loc[row, 'compound_construction']
        self.source1: str = df.loc[row, 'source_1']
        self.sutta1: str = df.loc[row, 'sutta_1']
        self.eg1: str = df.loc[row, 'example_1']
        self.sbs_pali_chant1: str = df.loc[row, 'sbs_chant_pali_1']
        self.sbs_eng_chant1: str = df.loc[row, 'sbs_chant_eng_1']
        self.chapter1: str = df.loc[row, 'sbs_chapter_1']
        self.source2: str = df.loc[row, 'source_2']
        self.sutta2: str = df.loc[row, 'sutta_2']
        self.eg2: str = df.loc[row, 'example_2']
        self.sbs_pali_chant2: str = df.loc[row, 'sbs_chant_pali_2']
        self.sbs_eng_chant2: str = df.loc[row, 'sbs_chant_eng_2']
        self.chapter2: str = df.loc[row, 'sbs_chapter_2']
        self.source3: str = df.loc[row, 'sbs_source_3']
        self.sutta3: str = df.loc[row, 'sbs_sutta_3']
        self.eg3: str = df.loc[row, 'sbs_example_3']
        self.sbs_pali_chant3: str = df.loc[row, 'sbs_chant_pali_3']
        self.sbs_eng_chant3: str = df.loc[row, 'sbs_chant_eng_3']
        self.chapter3: str = df.loc[row, 'sbs_chapter_3']
        self.source4: str = df.loc[row, 'sbs_source_4']
        self.sutta4: str = df.loc[row, 'sbs_sutta_4']
        self.eg4: str = df.loc[row, 'sbs_example_4']
        self.sbs_pali_chant4: str = df.loc[row, 'sbs_chant_pali_4']
        self.sbs_eng_chant4: str = df.loc[row, 'sbs_chant_eng_4']
        self.chapter4: str = df.loc[row, 'sbs_chapter_4']
        self.sbs_index: str = df.loc[row, 'sbs_index']
        self.var: str = df.loc[row, 'variant']
        self.comm: str = re.sub(r'(.+)\.$', '\\1', df.loc[row, 'commentary'])
        self.notes: str = df.loc[row, 'notes']
        self.stem: str = df.loc[row, 'stem']
        self.ex: str = df.loc[row, 'sbs_class_anki']
        self.cl: str = df.loc[row, 'sbs_class']
        self.count: str = df.loc[row, 'count']
        self.id: str = df.loc[row, 'id']
        self.dpd_source1: str = df.loc[row, 'DPD_source_1']
        self.dpd_sutta1: str = df.loc[row, 'DPD_sutta_1']
        self.dpd_eg1: str = df.loc[row, 'DPD_example_1']
        self.dpd_source2: str = df.loc[row, 'DPD_source_2']
        self.dpd_sutta2: str = df.loc[row, 'DPD_sutta_2']
        self.dpd_eg2: str = df.loc[row, 'DPD_example_2']
        self.move: str = df.loc[row, 'move']

    def translate_abbreviations(self) -> None:
        # TODO Cache
        # TODO Process by lexems
        targets = [
            'pos',
            'grammar',
            'neg',
            'verb',
            'trans',
            'case',
            'base',
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
        ru_meaning = series.iloc[3]
        self.example = series.iloc[4]
        self.explanation = series.iloc[5]
        ru_abbrev = series.iloc[6]

        if kind == Kind.DPSRU:
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
