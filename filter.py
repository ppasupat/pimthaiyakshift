#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import collections
import json
import re

from pythainlp import corpus 
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

BAD_WIKI_TITLES = re.compile(
    r'^[คพร]\.ศ\. ?[๐๑๒๓๔๕๖๗๘๙]*$'    # Years
    r'|^[๐๑๒๓๔๕๖๗๘๙]{1,2} (..?\.[คยพ]\.|.*(คม|ยน|พันธ์))$'     # Dates
    )


def get_word_iter(args):
  if args.words_source == 'pythainlp':
    for word in corpus.thai_words():
      yield word
  elif args.words_source == 'wikititles':
    # Load the Wikipedia titles from a file
    with open(args.infile) as fin:
      for word in fin:
        # Change arabic number to Thai number, or the other way around
        for x, y in NUMBER_MAP.items():
          if args.arabic:
            word = word.replace(y, x)
          else:
            word = word.replace(x, y)
        if BAD_WIKI_TITLES.match(word):
          continue
        yield word.strip()
  elif args.words_source == 'thainames':
    for word in corpus.thai_family_names():
      yield word
    for word in corpus.thai_female_names():
      yield word
    for word in corpus.thai_male_names():
      yield word
  else:
    raise ValueError('Unrecognized source {}'.format(args.words_source))


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-v', '--verbose', action='store_true')
  parser.add_argument('-m', '--min-length', type=int, default=5)
  parser.add_argument('-M', '--max-length', type=int, default=15)
  parser.add_argument('-s', '--min-num-shifts', type=float, default=2.)
  parser.add_argument('-r', '--shift-rate', type=float, default=.3)
  parser.add_argument('-e', '--easy-shift-weight', type=float, default=.5)
  parser.add_argument('-a', '--arabic', action='store_true')
  parser.add_argument('-i', '--infile')
  parser.add_argument('-o', '--outfile')
  parser.add_argument('words_source')
  args = parser.parse_args()

  # The score is 100 * (num_shifts - shift_rate * num_chars).
  # We want the total score to be as close to 0 as possible.
  score_to_words = {}

  # Read the list of words and record the scores.
  for word in get_word_iter(args):
    num_chars = len(word)
    if (num_chars < args.min_length
        or num_chars > args.max_length
        or any(x not in ALL_CHARS for x in word)):
      continue
    num_shifts = (
        sum(x in HARD_SHIFT_CHARS for x in word)
        + args.easy_shift_weight * sum(x in EASY_SHIFT_CHARS for x in word))
    if num_shifts < args.min_num_shifts:
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

