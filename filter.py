#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import collections
import json

from pythainlp.util import collate

NORMAL_CHARS = set('ๅภถุคึตจขชๆไำพัะนีรยบลฟหกด้เส่าวงผปแอิมืทใฝ /-')
SHIFT_CHARS = set('๑๒๓๔๕๖๗๘๙๐ฎูฑธํณ๊ฯญฐฤฆฏโฌ็ษ๋ศซฉฮฺฒ์ฬฦ.฿",()?+')
ALL_CHARS = NORMAL_CHARS | SHIFT_CHARS

EASY_SHIFT_CHARS = set('อ์อูอ็โ'.replace('อ', ''))
HARD_SHIFT_CHARS = SHIFT_CHARS - EASY_SHIFT_CHARS

NUMBER_MAP = {chr(ord('0') + x): chr(ord('๐') + x) for x in range(10)}
# print(NUMBER_MAP)

# Uncomment to check the characters. Should only miss non-typable ones
# for x in range(0xe01, 0xe5c):
#     if chr(x) not in ALL_CHARS:
#         print(hex(x))


def get_word_iter(words_source):
    if words_source == 'pythainlp':
        from pythainlp.corpus import thai_words
        for word in thai_words():
            yield word
    else:
        # Assume it's a filename.
        with open(words_source) as fin:
            for line in fin:
                yield line.strip()


def preprocess_word(word):
    # Change number to Thai number
    for x, y in NUMBER_MAP.items():
        word = word.replace(x, y)
    return word.strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-m', '--min-length', type=int, default=5)
    parser.add_argument('-M', '--max-length', type=int, default=15)
    parser.add_argument('-r', '--shift-rate', type=float, default=.3)
    parser.add_argument('-e', '--easy-shift-weight', type=float, default=.5)
    parser.add_argument('-o', '--outfile')
    parser.add_argument('words_source')
    args = parser.parse_args()

    # The score is 100 * (num_shifts - shift_rate * num_chars).
    # We want the total score to be as close to 0 as possible.
    score_to_words = {}

    # Read the list of words and record the scores.
    for word in get_word_iter(args.words_source):
        word = preprocess_word(word)
        num_chars = len(word)
        if (num_chars < args.min_length
                or num_chars > args.max_length
                or any(x not in ALL_CHARS for x in word)):
            continue
        num_shifts = (
                sum(x in HARD_SHIFT_CHARS for x in word)
                + args.easy_shift_weight * sum(x in EASY_SHIFT_CHARS for x in word))
        if num_shifts < 1:
            continue
        score = round(100 * (num_shifts - args.shift_rate * num_chars))
        score_to_words.setdefault(score, set()).add(word)

    # Keep removing words until the average score is 0.
    current_total_score = sum(score * len(words)
            for (score, words) in score_to_words.items())
    print(current_total_score)
    while current_total_score < 0:
        min_score = min(score_to_words)
        current_total_score -= min_score * len(score_to_words[min_score])
        print(f'Removed {min_score} * {len(score_to_words[min_score])} '
                f'--> {current_total_score}')
        del score_to_words[min_score]

    remaining_words = []
    for words in score_to_words.values():
        remaining_words.extend(words)
    remaining_words = collate(remaining_words)
    print(len(remaining_words), 'words left')

    # Dump the scored words to a file.
    if args.outfile:
        with open(args.outfile, 'w') as fout:
            json.dump(remaining_words, fout, indent=0, ensure_ascii=False)



if __name__ == '__main__':
    main()

