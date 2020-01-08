# Word Morph (Letter change variant)

Cool coding excercise.

## What is?

A word game. For a given two words of the same length, move from the first to the second by changing one character each step. i.e. 
`morph(foo, bar) ===> foo -> for -> far -> bar`. Each word in the chain should be a valid English word.

## Why?

why not?

## How to use

1. Simplest use case is morphing two words

    ```sh
    >> python morph.py dic.txt fake news
    Morphing [fake <-> news] using [dic.txt].
    Solution: fake <-> fate <-> fats <-> fets <-> nets <-> news
    ```

    `dic.txt` is the dictionary to use. Each line should containt only one word.


2. Morphing two words while excluding some words from the dictionary.

    In the example above, say we don't like the word `fets` and we would like to find a solution without it, we could exclude it from search using `-e fets` i.e.

    ```sh
    >> python morph.py dic.txt fake news -e fets
    Morphing [fake <-> news] using [dic.txt] excluding [fets].
    Solution: fake <-> bake <-> babe <-> nabe <-> nabs <-> nebs <-> news
    ```

    of course one can exclude several words.

## Algorithim

The program uses the Breadth-first search (BFS) algorithim. It will always find the shortest path but there might be other paths of the same length.

## Contributing

Anything is welcome.

I am a python newbie and this is my very first script. Feel free to modify anything and submit PR.
