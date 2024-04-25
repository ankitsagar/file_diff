from abc import ABC, abstractmethod
from typing import Any, Dict, List
import csv


class FileWriteStrategy(ABC):

    @abstractmethod
    def write(self, file_path: str, data: Any):
        raise NotImplementedError


class CSVDictWriterStrategy(FileWriteStrategy):

    def write(self, file_path: str, data: [List[str], List[Dict]]):
        """
        Writes the given dictionary into a csv file.

        :param file_path: file name to write the data
        :param data: the first index contains list of columns and second index
                    should be the list of dict to write.

        :return: None
        """
        columns = data[0]
        with open(file_path, 'w', newline="") as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()

            for row in data[1]:
                writer.writerow(row)


class FileWriter:

    def __init__(self, writer_strategy: FileWriteStrategy) -> None:
        self._writer_strategy = writer_strategy

    @property
    def writer(self) -> FileWriteStrategy:
        return self._writer_strategy

    @writer.setter
    def writer(self, writer_strategy: FileWriteStrategy) -> None:
        self._writer_strategy = writer_strategy

    def write_content(self, file_path: str, content: Any) -> None:
        self._writer_strategy.write(file_path, content)
