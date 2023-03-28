from io import BufferedReader
import os
from zipfile import ZipFile
from lzw import lzw_decompress

def read_file(filename: str) -> bytes:
    filename = filename.upper()

    if os.path.exists(f"data/{filename}"):
        print(f"loading {filename} ...")
        with open(f"data/{filename}", "rb") as file:
            return file.read()

    if filename[-4:] != ".EGA" and os.path.exists("data/u4upgrad.zip"):
        with ZipFile("data/u4upgrad.zip") as zipfile:
            for name in zipfile.namelist():
                if name.upper() == filename or name.upper()[-4:] == ".OLD" and name.upper()[0:-4] == filename[0:-4]:
                    print(f"loading u4upgrad.zip/{name} as {filename} ...")
                    return zipfile.read(name)
    if os.path.exists("data/ultima4.zip"):
        with ZipFile("data/ultima4.zip") as zipfile:
            for name in zipfile.namelist():
                if name.upper() == filename:
                    print(f"loading ultima4.zip/{name} as {filename} ...")
                    return zipfile.read(name)

    raise Exception(f"could not find file {filename}")

class DosFile:
    _bytes: bytes
    _pos = 0
    _len = 0

    def __init__(self, path):
        self._bytes = read_file(path)
        self._len = len(self._bytes)

    def seek(self, offset) -> None:
        self._pos = min(self._len, max(offset, 0))

    def read(self, offset: int = -1) -> int:
        if offset != -1:
            self.seek(offset)
        if self._pos >= self._len: return -1
        try:
            return self._bytes[self._pos]
        finally:
            self._pos += 1

    def read_byte(self, offset: int = -1) -> int:
        return self.read(offset)

    def read_word(self, offset: int = -1) -> int:
        if offset != -1:
            self.seek(offset)
        lo = self.read()
        hi = self.read()
        return 256 * hi + lo

    def read_asciiz(self, offset: int = -1) -> str:
        if offset != -1:
            self.seek(offset)
        string = ""
        while True:
            c = self.read()
            if c <= 0: return string
            string += chr(c)

    def read_n_asciiz(self, count: int, offset: int = -1) -> list:
        if offset != -1:
            self.seek(offset)
        return [ self.read_asciiz() for _ in range(count) ]

    def read_n_bytes(self, count: int, offset: int = -1) -> list:
        if offset != -1:
            self.seek(offset)
        return [ self.read_byte() for _ in range(count) ]

    def read_n_words(self, count: int, offset: int = -1) -> list:
        if offset != -1:
            self.seek(offset)
        return [ self.read_word() for _ in range(count) ]

class LzwDosFile(DosFile):
    def __init__(self, path):
        self._bytes = lzw_decompress(read_file(path))
        self._len = len(self._bytes)
