#!/usr/bin/env python
import argparse
import json


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-v', '--verbose', action='store_true')
  parser.add_argument('infile')
  args = parser.parse_args()

  data = []
  with open(args.infile) as fin:
    header = fin.readline()
    for line in fin:
      data.append(line.rstrip().split('\t'))
      if len(data[-1]) != len(data[0]):
        print('Mismatched number of columns: {}'.format(line))

  if len(data[0]) == 1:
    data = [x[0] for x in data]
  print('[')
  for x in data[:-1]:
    print(json.dumps(x, ensure_ascii=False) + ',')
  print(json.dumps(data[-1], ensure_ascii=False))
  print(']')


if __name__ == '__main__':
  main()

