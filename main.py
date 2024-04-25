from diff_checker import CSVFileDiffChecker
from file_reader import CSVMemorySafeReader
from file_writer import CSVDictWriterStrategy
from utils import get_args, validate_path


if __name__ == "__main__":
    args = get_args()
    first_file = args.first_file
    second_file = args.second_file
    destination_path = args.diff_path

    validate_path(first_file)
    validate_path(second_file)

    unique_column = "employee_id"   # Fixme: Hardcoding it for now

    diff_checker_obj = CSVFileDiffChecker(
        first_file,
        second_file,
        destination_path,
        CSVMemorySafeReader,
        CSVDictWriterStrategy,
        unique_column
    )
    diff_checker_obj.get_diff()
