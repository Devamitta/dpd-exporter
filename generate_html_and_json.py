import pickle
import re

from typing import List

import pandas as pd
import rich

from helpers import DataFrames
from helpers import ENCODING
from helpers import INDECLINABLES
from helpers import Kind
from helpers import ResourcePaths
from helpers import format_if
from helpers import parse_data_frames
from helpers import string_if
from helpers import timeis, line
from html_components import AbbreviationTemplate
from html_components import HeaderTemplate
from html_components import WordTemplate
from word import AbbreviationEntry
from word import DpsRuWord


# TODO Merge with sbs version (use a dict for lang-specific entries)
def _full_text_dps_ru_entry(word: DpsRuWord) -> str:
    comm_text = re.sub('<br/>', ' ', word.comm)
    comm_text = re.sub('<b>', '', comm_text)
    comm_text = re.sub('</b>', '', comm_text)

    construction_text = re.sub('<br/>', ', ', word.construction)

    result = ''
    result += string_if(not word.russian, f'{word.pali}. {word.pos}. {word.meaning}. [в процессе]')
    result += string_if(word.pos, f'{word.pali}. {word.pos}')

    for i in [word.grammar, word.derived, word.neg, word.verb, word.trans]:
        result += string_if(i, f', {i}')

    result += string_if(word.case, f' ({word.case})')
    result += f'. {word.meaning}'
    result += string_if(word.russian, f'. {word.russian}')
    result += string_if(word.root, f'. корень: {word.root}')
    result += format_if(word.base, '. основа: {}')

    result += format_if(construction_text, '. образование: {}')

    result += format_if(word.var, 'вариант: {}')
    result += format_if(comm_text, '. комментарий: {}')
    result += format_if(word.notes, '. заметки: {}')
    result += format_if(word.sk, '. санскрит: {}')
    result += format_if(word.sk_root, '. санск. корень: {}')
    result += '\n'

    return result


def _full_text_sbs_entry(word: DpsRuWord) -> str:
    comm_text = re.sub('<br/>', ' ', word.comm)
    comm_text = re.sub('<b>', '', comm_text)
    comm_text = re.sub('</b>', '', comm_text)

    construction_text = re.sub('<br/>', ', ', word.construction)

    result = ''
    result += string_if(word.pos, f'{word.pali}. {word.pos}')

    for i in [word.grammar, word.derived, word.neg, word.verb, word.trans]:
        result += string_if(i, f', {i}')

    result += string_if(word.case, f' ({word.case})')
    result += f'. {word.meaning}'
    result += string_if(word.russian, f'. {word.russian}')
    result += string_if(word.root, f'. root: {word.root}')
    result += format_if(word.base, '. base: {}')

    result += format_if(construction_text, '. construction: {}')

    result += format_if(word.var, 'variant: {}')
    result += format_if(comm_text, '. commentary: {}')
    result += format_if(word.notes, '. notes: {}')
    result += format_if(word.sk, '. sanskrit: {}')
    result += format_if(word.sk_root, '. sk. root: {}')
    result += '\n'

    return result


def _full_text_dps_en_entry(word: DpsRuWord) -> str:
    comm_text = re.sub('<br/>', ' ', word.comm)
    comm_text = re.sub('<b>', '', comm_text)
    comm_text = re.sub('</b>', '', comm_text)

    construction_text = re.sub('<br/>', ', ', word.construction)

    result = ''
    result += string_if(word.pos, f'{word.pali}. {word.pos}')

    for i in [word.grammar, word.derived, word.neg, word.verb, word.trans]:
        result += string_if(i, f', {i}')

    result += string_if(word.case, f' ({word.case})')
    result += f'. {word.meaning}'
    result += string_if(word.russian, f'. {word.russian}')
    result += string_if(word.root, f'. root: {word.root}')
    result += format_if(word.base, '. base: {}')

    result += format_if(construction_text, '. construction: {}')

    result += format_if(word.var, 'variant: {}')
    result += format_if(comm_text, '. commentary: {}')
    result += format_if(word.notes, '. notes: {}')
    result += format_if(word.sk, '. sanskrit: {}')
    result += format_if(word.sk_root, '. sk. root: {}')
    result += '\n'

    return result


def generate_html_and_json(rsc, generate_roots: bool = True):
    data = parse_data_frames(rsc)
    kind = rsc['kind']
    assert kind in list(Kind), 'Invalid kind get from resources'

    rich.print(f'{timeis()} [yellow]generate html and json')
    rich.print(f'{timeis()} {line()}')
    rich.print(f'{timeis()} [green]generating dps html')

    error_log = ''

    html_data_list = []
    text_data_full = ''
    text_data_concise = ''

    inflection_table_error_string = ''
    synonyms_error_string = ''

    df = data['words_df']
    df_length = data['words_df'].shape[0]

    with open(rsc['dict_words_css_path'], 'r', encoding=ENCODING) as f:
        words_css = f.read()

    with open(rsc['buttons_js_path'], 'r', encoding=ENCODING) as f:
        buttons_js = f.read()

    header_template = HeaderTemplate()
    word_template = WordTemplate(rsc['word_template_path'])

    for row in range(df_length):
        word = DpsRuWord(df, row)

        if rsc['kind'] is Kind.DPSRU:
            word.translate_abbreviations()

        if row % 5000 == 0 or row % df_length == 0:
            rich.print(f'{timeis()} {row}/{df_length}\t{word.pali}')

        html_string = ''
        if kind is Kind.DPSRU:
            text_full = _full_text_dps_ru_entry(word=word)
        elif kind is Kind.SBS:
            text_full = _full_text_sbs_entry(word=word)
        elif kind is Kind.DPSEN:
            text_full = _full_text_dps_en_entry(word=word)

        text_concise = ''

        # html head & style
        html_string += header_template.render(css=words_css, js=buttons_js)

        # summary
        if kind is Kind.DPSRU:
            if word.russian == '':
                text_concise += f'{word.pali}. {word.pos}. {word.meaning}.'
            else:
                if word.pos != '':
                    text_concise += f"{word.pali}. {word.pos}."
                text_concise += f' {word.russian}'

        elif kind is Kind.SBS:
            text_concise = f'{word.pali}.'

            if word.pos != '':
                text_concise += f"{word.pos}."

            if word.sbs_meaning != '':
                text_concise += f" {word.sbs_meaning}"

            if word.sbs_meaning == '':
                text_concise += f" {word.meaning}"

        elif kind is Kind.DPSEN:
            text_concise = f'{word.pali}.'

            if word.pos != '':
                text_concise += f"{word.pos}. {word.meaning}"


        # inflection table
        if word.pos not in INDECLINABLES:
            table_path = rsc['inflections_dir'].joinpath("output/html tables/").joinpath(word.pali + ".html")

            table_data_read = ''
            try:
                with open(table_path, encoding=ENCODING) as f:
                    table_data_read = f.read()
            except FileNotFoundError:
                inflection_table_error_string += word.pali + ", "
                error_log += f'error reading inflection table: {word.pali}.html\n'

        html_string += word_template.render(word, table_data_read=table_data_read)
        html_string += '</html>'

        inflections_path = rsc['inflections_dir'].joinpath("output/inflections translit/").joinpath(word.pali)

        if inflections_path.exists():
            with open(inflections_path, "rb") as syn_file:
                synonyms = pickle.load(syn_file)
        else:
            synonyms_error_string += word.pali + ', '
            error_log += f'error reading synonyms - {word.pali}\n'
            synonyms = ''

        # data compiling
        html_data_list += [[word.pali, html_string, '', synonyms]]
        text_data_full += text_full
        text_data_concise += f"{text_concise}\n"

        if row % 100 == 0:
            p = rsc['output_html_dir'].joinpath(f"{word.pali} (sample).html")
            with open(p, 'w', encoding=ENCODING) as f:
                f.write(html_string)

    error_log_path = rsc['error_log_dir'].joinpath("exporter errorlog.txt")
    with open(error_log_path, 'w', encoding=ENCODING) as error_log_file:
        error_log_file.write(error_log)

    if inflection_table_error_string != '':
        rich.print(f'{timeis()} [red]inflection table errors: {inflection_table_error_string}')

    if synonyms_error_string != '':
        rich.print(f'{timeis()} [red]synonym errors: {synonyms_error_string}')

    # convert ṃ to ṁ
    text_data_full = re.sub('ṃ', 'ṁ', text_data_full)
    text_data_concise = re.sub('ṃ', 'ṁ', text_data_concise)

    # write text versions
    p = rsc['output_share_dir'].joinpath('dps_ru_full.txt')
    with open(p, 'w', encoding=ENCODING) as f:
        f.write(text_data_full)

    p = rsc['output_share_dir'].joinpath('dps_ru_concise.txt')
    with open(p, 'w', encoding=ENCODING) as f:
        f.write(text_data_concise)

    if generate_roots:
        generate_roots_html_and_json(data, rsc, html_data_list)


def generate_roots_html_and_json(data: DataFrames, rsc: ResourcePaths, html_data_list):
    # html list > dataframe
    pali_data_df = pd.DataFrame(html_data_list)
    pali_data_df.columns = ["word", "definition_html", "definition_plain", "synonyms"]

    rsc['output_help_html_dir'].mkdir(parents=True, exist_ok=True)

    abbrev_data_list = _generate_abbreviations_html(data, rsc)
    help_data_list = _generate_help_html(data, rsc)
    definition_data_list = _generate_definition_html(data, rsc)

    # roots > dataframe > json
    rich.print(f'{timeis()} [green]generating json')

    abbrev_data_df = pd.DataFrame(abbrev_data_list)
    abbrev_data_df.columns = ["word", "definition_html", "definition_plain", "synonyms"]

    help_data_df = pd.DataFrame(help_data_list)
    help_data_df.columns = ["word", "definition_html", "definition_plain", "synonyms"]

    definition_data_df = pd.DataFrame(definition_data_list)
    definition_data_df.columns = ["word", "definition_html", "definition_plain", "synonyms"]
    pali_data_df = pd.concat([pali_data_df, abbrev_data_df, help_data_df, definition_data_df])

    rich.print(f'{timeis()} [green]saving html to json')

    pali_data_df.to_json(rsc['gd_json_path'], force_ascii=False, orient="records", indent=6)

    rich.print(f'{timeis()} {line()}')


def _generate_abbreviations_html(data: DataFrames, rsc: ResourcePaths) -> List[List[str]]:
    rich.print(f'{timeis()} [green]generating abbreviations html')

    abbrev_data_list = []

    with open(rsc['dict_help_css_path'], 'r', encoding=ENCODING) as f:
        abbrev_css = f.read()

    abbrev_df = data['abbrev_df']
    abbrev_df_length = len(abbrev_df)

    header_template = HeaderTemplate()
    abbreviation_template = AbbreviationTemplate(rsc['abbreviation_template_path'])

    for row in range(abbrev_df_length):
        abbrev_series = abbrev_df.iloc[row]
        abbrev_entry = AbbreviationEntry(rsc['kind'], abbrev_series)

        html_string = header_template.render(css=abbrev_css)
        html_string += abbreviation_template.render(abbrev_entry)
        html_string += '</html>'

        part_file = rsc['output_help_html_dir'].joinpath(f'{abbrev_entry}.html')

        with open(part_file, 'w', encoding=ENCODING) as file:
            file.write(html_string)

        # compile root data into list
        synonyms = [abbrev_entry.abbrev, abbrev_entry.meaning]

        abbrev_data_list += [[abbrev_entry.abbrev, html_string, '', synonyms]]

    return abbrev_data_list


def _generate_help_html(data: DataFrames, rsc: ResourcePaths) -> List[List[str]]:
    rich.print(f'{timeis()} [green]generating help html')

    help_data_list = []

    try:
        with open(rsc['dict_help_css_path'], 'r', encoding=ENCODING) as f:
            help_css = f.read()
    except FileNotFoundError:
        help_css = ''

    help_df = data['help_df']
    help_df_length = len(help_df)
    header_template = HeaderTemplate()

    for row in range(help_df_length):
        html_string = ''

        help_title = help_df.iloc[row, 0]
        meaning = help_df.iloc[row, 1]

        html_string += header_template.render(css=help_css)

        html_string += "<body>"

        # summary
        if rsc['kind'] is Kind.DPSRU:
            html_string += f'<div class="help"><p>помощь. <b>{help_title}</b>. {meaning}</p></div>'
        else:
            html_string += f'<div class="help"><p>help. <b>{help_title}</b>. {meaning}</p></div>'

        p = rsc['output_help_html_dir'].joinpath(f"{help_title}.html")

        with open(p, 'w', encoding=ENCODING) as f:
            f.write(html_string)

        # compile root data into list
        synonyms = [help_title]
        help_data_list += [[help_title, html_string, '', synonyms]]

    return help_data_list


def _generate_definition_html(data: DataFrames, rsc: ResourcePaths) -> List[List[str]]:
    kind = rsc['kind']
    rich.print(f'{timeis()} [green]generating definition HTML')

    df = data['words_df']
    df_length = data['words_df'].shape[0]
    pos_exclude_list = ["abbrev", "cs", "letter", "root", "suffix", "ve"]

    definition = {}

    for row in range(df_length):
        word = DpsRuWord(df, row)

        if rsc['kind'] is Kind.DPSRU:
            word.translate_abbreviations()

        meanings_list = []
        meaning_data = word.russian if kind is Kind.DPSRU else word.meaning
        meaning_data = re.sub(r'\?\?', '', meaning_data)

        if row % 10000 == 0:
            rich.print(f'{timeis()} {row}/{df_length}\t{word.pali}')

        if meaning_data != '' and word.pos_orig not in pos_exclude_list:

            meanings_clean = re.sub(r' \(.+?\)', '', meaning_data)              # remove all space brackets
            meanings_clean = re.sub(r'\(.+?\) ', '', meanings_clean)            # remove all brackets space
            meanings_clean = re.sub(r'(^ | $)', '', meanings_clean)             # remove space at start and fin
            meanings_clean = re.sub(r'  ', ' ', meanings_clean)                 # remove double spaces
            meanings_clean = re.sub(r' ;|; ', ';', meanings_clean)              # remove space around semicolons
            meanings_clean = re.sub(r'\((комм|comm)\).+$', '', meanings_clean)  # remove commentary meanings
            meanings_clean = re.sub(r'(досл|lit).+$', '', meanings_clean)       # remove lit meanings
            meanings_list = meanings_clean.split(';')

            for meaning in meanings_list:
                if meaning in definition and word.case == '':
                    definition[meaning] = f'{definition[meaning]}<br><b>{word.pali_clean}</b> {word.pos}. {meaning_data}'
                elif meaning in definition and word.case != '':
                    definition[meaning] = (
                        f'{definition[meaning]}<br>'
                        f'<b>{word.pali_clean}</b> {word.pos}. {meaning_data} ({word.case})')
                elif meaning not in definition and word.case == '':
                    definition.update({meaning: f'<b>{word.pali_clean}</b> {word.pos}. {meaning_data}'})
                elif meaning not in definition and word.case != '':
                    definition.update({meaning: f'<b>{word.pali_clean}</b> {word.pos}. {meaning_data} ({word.case})'})

    with open(rsc['definition_css_path'], 'r', encoding=ENCODING) as f:
        definition_css = f.read()

    definition_data_list = []

    div_class = 'rpd' if kind is Kind.DPSRU else 'epd_sbs'
    for key, value in definition.items():
        html_string = ''
        html_string = definition_css
        html_string += f"<body><div class='{div_class}'><p>{value}</p></div></body></html>"
        definition_data_list += [[key, html_string, '', '']]

    return definition_data_list
