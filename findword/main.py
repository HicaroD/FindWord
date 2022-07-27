from typing import Optional, Sequence
import requests
import asyncio

API_ENDPOINT = "https://api.dictionaryapi.dev/api/v2/entries/en/"

class WordNotFound(Exception):
    pass



class Dictionary:
    def __init__(self, words: Optional[Sequence]) -> None:
        self.words: Optional[Sequence] = words

    async def get_word_meanings(self, word: str) -> Sequence[str]:
        request = requests.get(API_ENDPOINT + word)

        match request.status_code:
            case 200: 
                word_definitions = request.json()[0]["meanings"][0]["definitions"]
                parsed_word_definition = [definition["definition"] for definition in word_definitions]
                return parsed_word_definition

            case 404:
                raise WordNotFound(f"{word} was not found in the dictionary.")
            case _:
                raise Exception("An unknown error ocurred during the request.")

    async def display_words(self) -> None:
        if self.words is None:
            # TODO: Report to the user that he should pass at least one word
            return
        
        for word in self.words:
            try:
                meaning = await self.get_word_meanings(word)
                print(meaning)

            except (WordNotFound, Exception) as e:
                print(e)
                exit(1)



async def main():
    # TODO: Split user input
    words = ["rust", "python"]
    dictionary = Dictionary(words)
    await dictionary.display_words()
