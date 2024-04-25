from file_reader import FileReaderInterface
from file_writer import FileWriteStrategy, FileWriter
from typing import Iterable, Dict, List
from abc import ABC


class FileDiffCheckerInterface(ABC):

    def __init__(
            self,
            first_file_path: str,
            second_file_path: str,
            destination_path: str,
            reader: FileReaderInterface,
            writer_strategy: FileWriteStrategy,
            unique_column: str = None):
        self._first_file_path = first_file_path
        self._second_file_path = second_file_path
        self._destination_path = destination_path
        self._reader = reader
        self._writer = FileWriter(writer_strategy())
        self._unique_column = unique_column

    def read_files(self) -> None:
        self.reader_1 = self._reader(self._first_file_path)
        self.reader_2 = self._reader(self._second_file_path)
        self.reader_1.read_file()
        self.reader_2.read_file()

    def check_diff(self) -> Iterable:
        raise NotImplementedError

    def write_diff(self) -> None:
        raise NotImplementedError

    def get_diff(self):
        print("Reading files.....")
        self.read_files()

        print("Checking difference.....")
        self.diff = self.check_diff()

        print("Writing to the new file......")
        self.write_diff()
        print(f"Your difference is written in file: {self._destination_path}")


class CSVFileDiffChecker(FileDiffCheckerInterface):
    CHANGE_TYPE_KEY = "change_type"
    ADDED_VAL = "Added"
    CHANGED_VAL = "Changed"
    DELETED_VAL = "Deleted"

    def __create_merge_dict(
            self,
            file_content: Iterable,
            data_table: Dict,
            default_change_type: str,
    ) -> None:
        """
        Runs on the existing data if any row is found changed then It'll update
        the change status otherwise it keeps as default given.

        :param file_content: Iterable content of the file
        :param data_table: Dict which holds the value of unique column as key
                           and entire row data as value
        :param default_change_type: If the record does not found in the existing
                                    record then it'll use this value for column
                                    change_type.
        :return: None
        """

        for data in file_content:
            unique_value = data.get(self._unique_column)
            # it's a mandatory column if not found that means row is corrupted
            if not unique_value:
                continue
            previous_value = data_table.get(unique_value, {})
            previous_value.pop(self.CHANGE_TYPE_KEY, None)
            if not previous_value:
                change_type = default_change_type
            elif previous_value == data:
                change_type = None
            else:
                change_type = self.CHANGED_VAL

            # If the data is same across both files so no need to add in diff
            # TODO: Need to discuss this logic with interviewer
            if not change_type:
                del data_table[unique_value]
                continue

            data[self.CHANGE_TYPE_KEY] = change_type
            data_table[unique_value] = data

    def check_diff(self) -> List[Dict]:
        data_table = {}
        self.__create_merge_dict(
            self.reader_1.content, data_table, self.DELETED_VAL)
        self.__create_merge_dict(
            self.reader_2.content, data_table, self.ADDED_VAL)

        return [value for _, value in data_table.items()]

    def write_diff(self) -> None:
        # Just in case if any file has extra columns
        merged_columns = list(set(self.reader_1.column + self.reader_2.column))
        merged_columns.append(self.CHANGE_TYPE_KEY)
        self._writer.write_content(
            self._destination_path, [merged_columns, self.diff])
