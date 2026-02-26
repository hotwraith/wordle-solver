# Wordle Solver

## Index

- [How to ?](#how-to-)
- [Using the solver](#using-the-solver)
    - [For the first time](#for-the-first-time)
    - [The rest of the steps](#the-rest-of-the-steps)
- [Misc](#misc)

## How to ?
- Download the [latest release](https://github.com/hotwraith/wordle-solver/releases/latest) package, and unzip the file wherever you want it.
- Always keep the following architecture or it'll break:
    - `.env` (this file is created on first startup)
    - `solver.exe`
    - data
        - words_dictionary.json
- Double click on `solver.exe`

## Using the solver

### For the first time

- The script will prompt you with a choice tu use one of the two available .json file, on a decent enough PC the difference between both is minimal, however the already filtered five letter word list will always be faster.
- If you want to reset your choice just delete the `.env` file in the folder.

### The rest of the steps

- Input a first word in the wordle.
- Type the result using the follow syntax:
    - for **correct** letters in _right_ positions use **__lowercase____** letters
    - for **correct** letters in _wrong_ positions use **__upercase__** letters
    - for **incorrect** letters use `-`
- An example, when searching for the word `plant`
    - Input: `trank`
    - The pattern to type would be: `T-an-`
- After proposing a word the script will ask you to choose between:
    - `y`: yes
    - `n`: no
    - `ne`: non-existent (some words might not be in the wordle's database, use this to get rid of them)
    - Typing anything else will just prompt a new word without discarding the old one so please don't :)

## Misc
- This solver is far from perfect, it will not _always_ solve the thing fast enough or at all, but it works good enough.
