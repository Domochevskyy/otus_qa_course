import csv
import json
from dataclasses import asdict, dataclass, field
from json import JSONDecodeError
from typing import Iterable, List, Tuple


@dataclass
class Book:
    title: str
    author: str
    pages: int
    genre: str


@dataclass
class Person:
    name: str
    gender: str
    address: str
    age: str
    books: List[dict] = field(default_factory=list)


class Parser:
    def __init__(self):
        self.json_parser = JsonParser()
        self.csv_parser = CsvParser()
        self.books: List[Book] = []
        self.persons: List[Person] = []

    def parse_persons(self, path_to_file):
        raw_data = self.json_parser.deserialize(path_to_file)
        for _dict_user_info in raw_data:
            name = _dict_user_info.get("name")
            gender = _dict_user_info.get("gender")
            address = _dict_user_info.get("address")
            age = _dict_user_info.get("age")
            self.persons.append(
                Person(
                    name,
                    gender,
                    address,
                    age,
                )
            )

    def parse_books(self, path_to_file):
        raw_data = self.csv_parser.deserialize(path_to_file)
        for _list_user_info in raw_data[1]:
            title = _list_user_info[0]
            author = _list_user_info[1]
            pages = _list_user_info[2]
            genre = _list_user_info[3]
            self.books.append(
                Book(
                    title,
                    author,
                    pages,
                    genre,
                )
            )

    def from_dataclass_to_dict(self):
        for i in range(len(self.persons)):
            self.persons[i] = asdict(self.persons[i])


class JsonParser:
    @staticmethod
    def deserialize(path_to_file) -> List[dict]:
        with open(path_to_file, "r") as file:
            try:
                content = json.load(file)
            except JSONDecodeError as error:
                print(error.msg)
        return content

    @staticmethod
    def serialize(path_to_file: str, data: Iterable[Person]):
        with open(path_to_file, "w") as file:
            json.dump(obj=data, fp=file, indent=4)


class CsvParser:
    @staticmethod
    def deserialize(path_to_file) -> Tuple[list, list]:
        with open(path_to_file, "r") as file:
            reader = csv.reader(file)
            headers = next(reader)
            return headers, list(reader)


class PersonIterator:
    def __init__(self, collection: List[Person], stop: int):
        self._collection = collection
        self._cursor = -1
        self._stop = stop
        self._stop_counter = -1

    def __next__(self):
        if self._stop == self._stop_counter:
            raise StopIteration()
        self._stop_counter += 1

        if self._cursor + 1 >= len(self._collection):
            self._cursor = -1
        self._cursor += 1

        return self._collection[self._cursor]

    def __iter__(self):
        return self


class BookHelper:
    @staticmethod
    def give_books(whom, book_collection):
        person_iter = iter(whom)
        for book in book_collection:
            try:
                current_person = next(person_iter)
                current_person.books.append(asdict(book))
            except StopIteration:
                return


if __name__ == "__main__":
    parser = Parser()
    parser.parse_books("books.csv")
    parser.parse_persons("users.json")
    book_helper = BookHelper()
    person_iterator = PersonIterator(parser.persons, len(parser.books))
    book_helper.give_books(person_iterator, parser.books)
    parser.from_dataclass_to_dict()
    parser.json_parser.serialize("result.json", parser.persons)
