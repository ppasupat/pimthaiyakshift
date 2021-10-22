# พิมพ์ไทยยาก Shift

A simple Thai typing game.

## Current word lists

* `words.json`: Generated by

    ```bash
    python3 filter.py pythainlp -o data/words.json -m 5 -M 15 -s 2 -r .3 -e .5
    ```
    
    The command above collects all words with 5-15 characters from the
    [PyThaiNLP](https://pythainlp.github.io/) word list with at least
    2 shift characters.
    Then it greedily removes words with low shift-to-non-shift ratio
    until the ratio of shift characters to all characterss exceeds 0.3. 
    Frequent shift characters count as 0.5 times other shift characters.

* `wikititles.json`: Thai Wikipedia titles

    ```bash
    python3 filter.py wikititles -i <path_to_wiki_titles> -o data/wikititles.json -m 5 -M 15 -s 2 -r .3 -e .5
    ```

    The titles are extracted by running [WikiExtractor](https://github.com/attardi/wikiextractor)
    on the Thai Wikipedia dump (Oct 2021) and then running

    ```bash
    grep -r 'title=".*"' -o -h text/ | sed 's/title="\(.*\)"/\1/' > wiki-titles.txt
    ```

* `names.json`: Thai names from PyThaiNLP

    ```bash
    python3 filter.py thainames -o data/names.json -m 5 -M 15 -s 2 -r .3 -e .5
    ```

* `skoy.json`: Skoy language.
    I want to use authentic Skoy, but the original Facebook page (sowhateiei: ษม่ค่ล์มนิ๋ญฒสก๊อย) has been nuked.
    (Skoy language is pretty old, you know.)
    So I [manually collected parallel sentences](https://docs.google.com/spreadsheets/d/1-tB9bV8ihteGjQ628u2lm8RG0Mrw8w6Xn1yPObY6vyI/edit?usp=sharing)
    from the remnants of the language usage.
