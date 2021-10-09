#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import collections
import json


NORMAL_CHARS = set('ๅภถุคึตจขชๆไำพัะนีรยบลฟหกด้เส่าวงผปแอิมืทใฝ')
SHIFT_CHARS = set('๑๒๓๔๕๖๗๘๙๐ฎูฑธํณ๊ฯญฐฤฆฏโฌ็ษ๋ศซฉฮฺฒ์ฬฦ')
ALL_CHARS = NORMAL_CHARS | SHIFT_CHARS

# Uncomment to check the characters. Should only miss non-typable ones
# for x in range(0xe01, 0xe5c):
#   if chr(x) not in ALL_CHARS:
#     print(hex(x))


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-v', '--verbose', action='store_true')
  parser.add_argument('-m', '--min-length', type=int, default=4)
  parser.add_argument('-r', '--shift-rate', type=float, default=.3)
  parser.add_argument('-o', '--outfile')
  parser.add_argument('infile')
  args = parser.parse_args()

  # The score is 100 * (num_shifts - shift_rate * num_chars).
  # We want the total score to be as close to 0 as possible.
  score_to_words = {}

  # Read the list of words and record the scores.
  with open(args.infile) as fin:
    for line in fin:
      word = line.strip()
      num_chars = len(word)
      if (num_chars < args.min_length
          or any(x not in ALL_CHARS for x in word)):
        continue
      num_shifts = sum(x in SHIFT_CHARS for x in word)
      if num_shifts == 0:
        continue
      score = round(100 * (num_shifts - args.shift_rate * num_chars))
      score_to_words.setdefault(score, []).append(word)

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
  print(len(remaining_words), 'words left')

  # Dump the scored words to a file.
  if args.outfile:
    with open(args.outfile, 'w') as fout:
      json.dump(remaining_words, fout, indent=0, ensure_ascii=False)



if __name__ == '__main__':
  main()

