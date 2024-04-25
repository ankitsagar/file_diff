from abc import ABC, abstractmethod


class FileReaderInterface(ABC):

    def __init__(self, file_path: str):
        self._file_path = file_path
        self._content = None

    @property
    def content(self):
        return self._content

    @abstractmethod
    def read_file(self) -> None:
        raise NotImplementedError


class CSVFileReaderInterface(FileReaderInterface):

    def __init__(self, file_path: str):
        super().__init__(file_path)
        self._column = None

    @property
    def column(self):
        if not self._column:
            raise Exception("Call read_file first")
        return self._column

    @abstractmethod
    def read_file(self) -> None:
        raise NotImplementedError


class CSVMemorySafeReader(CSVFileReaderInterface):
    """
    Reads the csv file through a generator, so we can read large files
    without exhausting the system's memory.
    """

    def read_file(self):
        # Generator comprehension to read file since it can be very large
        lines = (line for line in open(self._file_path))

        # This yields the value in each line in a list form also removed if any
        # trailing whitespace.
        content = (line.rstrip().split(",") for line in lines)
        try:
            self._column = next(content)
        except StopIteration:
            raise Exception(f"Empty file: {self._file_path}")
        self._content = (dict(zip(self._column, data)) for data in content)

