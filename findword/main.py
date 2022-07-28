from typing import Optional, Sequence, Tuple
from dataclasses import dataclass
import termcolor
import requests
import asyncio
import argparse

API_ENDPOINT = "https://api.dictionaryapi.dev/api/v2/entries/en/"


class WordNotFound(Exception):
    pass


@dataclass
class Word:
    word: str
    part_of_speech: str
    meanings: Sequence[str]

    def __str__(self):
        word = termcolor.colored(self.word, "cyan", attrs=["bold"])
        possible_definitions = termcolor.colored(
            "Possible definitions", attrs=["bold", "underline"]
        )
        part_of_speech = termcolor.colored(self.part_of_speech, "green")
        representation = f"{word}, {part_of_speech}\n\n{possible_definitions}:\n"

        if len(self.meanings) < 5:
            for meaning in self.meanings:
                representation += f"   - {meaning}\n"
        else:
            for i in range(5):
                meaning = self.meanings[i]
                representation += f"   - {meaning}\n"

        return representation


class Dictionary:
    def __init__(self, words: Optional[Sequence[str]]) -> None:
        self.words: Optional[Sequence] = words

    async def get_word_raw_data(self, word: str) -> requests.Response:
        return requests.get(API_ENDPOINT + word)

    async def get_word_meanings(self, word: str) -> Word:
        raw_data_request = await self.get_word_raw_data(word)

        match raw_data_request.status_code:
            case 200:
                raw_data = raw_data_request.json()[0]
                part_of_speech = raw_data["meanings"][0]["partOfSpeech"]
                definitions = raw_data["meanings"][0]["definitions"]
                word = Word(
                    word,
                    part_of_speech,
                    [definition["definition"] for definition in definitions],
                )
                return word
            case 404:
                word = termcolor.colored(word, "cyan", attrs=["underline"])
                raise WordNotFound(f"The word {word} was not found in the dictionary.")
            case _:
                raise Exception("An unknown error ocurred during the request.")

    async def display_words(self) -> None:
        try:
            for word in self.words:
                word_meaning = await self.get_word_meanings(word)
                print(word_meaning)

        except (WordNotFound, Exception) as e:
            print(e)
            exit(1)


def build_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="A simple CLI for finding the meaning or translation of a word. "
    )
    parser.add_argument(
        "--words", help="a list of words separated by spaces. Ex.: python incredible"
    )
    return parser


async def main():
    args = build_cli().parse_args()

    if args.words is None:
        print("Error: You should pass at the least one word, get some '--help'")
        exit(1)

    words = args.words.strip().split()

    dictionary = Dictionary(words)
    await dictionary.display_words()
