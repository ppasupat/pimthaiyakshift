#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse


NORMAL_CHARS = set('ๅ/-ภถุคึตจขชๆไำพัะนีรยบลฃฟหกด้เส่าวงผปแอิมืทใฝ')
SHIFT_CHARS = set('+๑๒๓๔๕๖๗๘๙๐"ฎูฑธํณ๊ฯญฐ,ฅฤฆฏโฌ็ษ๋ศซ.()ฉฮฺฒ์?ฬฦ')
ALL_CHARS = NORMAL_CHARS | SHIFT_CHARS
MIN_LENGTH = 3
MAX_LEN_FOR_NUM_SHIFT = {0: 0, 1: 4, 2: 9, 3: 14, 4: 100}

# Uncomment to check the characters. Should only miss non-typable ones
# for x in range(0xe01, 0xe5c):
#   if chr(x) not in ALL_CHARS:
#     print(hex(x))


def check(word):
  if len(word) < MIN_LENGTH or any(x not in ALL_CHARS for x in word):
    return False
  num_shifts = min(4, sum(x in SHIFT_CHARS for x in word))
  return len(word) <= MAX_LEN_FOR_NUM_SHIFT[num_shifts]


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-v', '--verbose', action='store_true')
  parser.add_argument('infile')
  args = parser.parse_args()

  with open(args.infile) as fin:
    for line in fin:
      line = line.strip()
      if check(line):
        print(line)


if __name__ == '__main__':
  main()

