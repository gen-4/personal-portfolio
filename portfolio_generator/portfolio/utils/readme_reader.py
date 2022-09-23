#!/usr/bin/env python3

from os.path import getsize
from os import walk, stat
import re
from typing import Tuple
import fnmatch


class Markdown:
    
    def __init__(self, path: str):
        self.file = open(path, 'r')
        self.size = getsize(path)
        self.bytes_read = self.file.tell()

    def __del__(self):
        print("Closing file...")
        self.file.close()
        print("File closed...")


    def _print_remaining(self):
        percentage = self.bytes_read / self.size * 100
        icon = '#'
        print('[', end='')
        for i in range(10):
            character = icon
            if abs(percentage - (i * 10)) < 5: # This will probably fail if result = 5
                icon = '-'
                character = f'{percentage:2.0f}'

            print(f"{character}{'' if len(character) == 1 else '%'}", end='')

        print(f'] ({self.bytes_read} out of {self.size} bytes)')

    def _parse_title(self, line: str) -> Tuple[str, str, str]:
        hash_simbols, title = line.split(' ', 1)

        return title, 'title', str(len(hash_simbols))

    def _parse_code(self, line: str) -> Tuple[str, str, str]:
        language = line.split('```')[1].split('\n')[0]
        line = ''
        text = ''
        while not line.__contains__('```'):
            line = self.file.readline()
            if line.__contains__('```'):
                text += line.split('```')[0]

            else: text += line

        self.bytes_read = self.file.tell()

        return text, 'code', language

    def _transform_reference(self, line: str) -> str:
        found = re.search('\[.+\]\(.+\)', line)
        if found:
            name, reference = line.split('](', 1)
            name = name.split('[')[1]
            reference = reference.split(')')[0]

            line = line[:found.start()] + f"<a href={reference}>{name}</a>" + line[found.end():]

        return line

    def read_line(self) -> Tuple[str, str, str]:
        if self.size <= self.bytes_read: return None, 'end', None
        line = self.file.readline()
        self.bytes_read = self.file.tell()
        line = self._transform_reference(line)

        result_tuple = None
        if line.startswith('#'):
            result_tuple = self._parse_title(line)

        elif line.startswith('```'):
            result_tuple = self._parse_code(line)

        else: 
            result_tuple = line, 'text', ''

        self._print_remaining()

        return result_tuple


if __name__ == '__main__':    

    for _, dirs, _ in walk("python/"):
        for dir in dirs:
            print('\n')
            print(dir.upper())
            print('\n')
            if not dir.startswith('.'):
                reader = Markdown(f"python/{dir}/README.md")
                text = ''
                while text is not None:
                    text, typ, arg = reader.read_line()
                    if text is not None:
                        text = text.rstrip('\n')
                        print(f"{typ.upper()}: {text} ({arg})")