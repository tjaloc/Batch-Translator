"""Batch translate words/ phrases from a csv file
"""
import pandas
from googletrans import Translator
import os
from time import sleep

# settings
FILE_PATH = 'example.csv'
OUTPUT_DIR = 'ouput'
SEP = ';'
ENCODINGS = ['utf8', 'iso-8859-1']  # Save in different encodings if necessary. Note, encoding must match language e.g. 'iso-8859-1' wouldn't work for Chinese or Russian


# read csv input
df = pandas.read_csv(
    FILE_PATH,
    sep=SEP,
    skip_blank_lines=True,
    encoding='utf8'
)

languages = df.columns
first_language = languages[0]

# init google-translate
translator = Translator()

# create another df for translations / destination_df
translated_df = pandas.DataFrame(columns=languages)

def translate_word(word, src_lang, dest_lang, retries=3):
    for attempt in range(retries):
        try:
            translation = translator.translate(word, src=src_lang, dest=dest_lang)
            return translation.text
        except AttributeError:
            print(f"Error trying to fetch translation of {word}.")
            sleep(1)
    return None

# 1st column is copy of source column
translated_df[first_language] = df[first_language]

# other columns are translations
for other_language in languages[1:]:
    translated_df[other_language] = df[first_language].apply(lambda word: translate_word(word, first_language, other_language))

name, ext = os.path.splitext(os.path.basename(FILE_PATH))
for enc in ENCODINGS:
    filename = f"{name}_{'-'.join(languages)}_{enc}.{ext}"
    dest_file = os.path.join(OUTPUT_DIR, filename)
    translated_df.to_csv(dest_file, sep=SEP, index=False, encoding=enc)
