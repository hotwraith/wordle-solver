# Wordle Solver

## Index

## How to ?
- Download the last release package, and unzip the file wherever you want it.
- Always keep the following architecture or it'll break:
    - `solver.exe`
    - data
        - words_dictionary.json
- Double click on `solver.exe`

## Using the solver
- Input a first word in the wordle.
- Type the result using the follow syntax:
    - for **correct** words in _right_ positions use **__lowercase____** letters
    - for **correct** words in _wrong_ positions use **__upercase__** letters
    - for **incorrect** words use `-`
- An example, when searching for the word `plant`
    - Input: `trank`
    - The pattern to type would be: `T-an-`

## Misc
- This solver is far from perfect, it will not _always_ solve the thing fast enough or at all, but it works good enough.