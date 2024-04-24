from typing import Generator, Dict, Any, List
import csv


CHANGE_TYPE_KEY = "change_type"
UNIQUE_COLUMN = "employee_id"
ADDED_VAL = "Added"
CHANGED_VAL = "Changed"
DELETED_VAL = "Deleted"


def read_csv_file(file_name: str) -> [Generator[Dict[str, str], Any, None], List[str]]:  # noqa
    """
    Reads the csv file through a generator, so we can read large files without
    exhausting the system's memory.

    :param file_name: location of file
    :returns: Generator objects that yields dict which contains column name as
              key, and it's value.
    """

    # Generator comprehension to read file since it can be very large
    lines = (line for line in open(file_name))

    # This yields the value in each line in a list form also removed if any
    # trailing whitespace.
    line_list = (line.rstrip().split(",") for line in lines)
    columns = next(line_list)

    return (dict(zip(columns, data)) for data in line_list), columns


def create_merge_dict(
    file_content: Generator[Dict[str, str], Any, None],
    data_table: Dict,
    default_change_type: str,
) -> None:
    """
    Runs on the existing data if any row is found again then It'll update the
    change status otherwise it keeps as default given.

    :param file_content: Generator object of the file
    :param data_table: Dict which holds the value of unique column as key and
                         entire row data as value
    :param default_change_type: If the record does not found in the existing
                                record then it'll use this value for column
                                change_type.
    :return: None
    """

    for data in file_content:
        unique_value = data.get(UNIQUE_COLUMN)
        # it's a mandatory column if not found that means row is corrupted
        if not unique_value:
            continue
        previous_value = data_table.get(unique_value, {})
        previous_value.pop(CHANGE_TYPE_KEY, None)
        if not previous_value:
            change_type = default_change_type
        elif previous_value == data:
            change_type = None
        else:
            change_type = CHANGED_VAL

        # If the data is same across both files so no need to add in diff
        # TODO: Need to discuss this logic with interviewer
        if not change_type:
            del data_table[unique_value]
            continue

        data[CHANGE_TYPE_KEY] = change_type
        data_table[unique_value] = data


def dict_to_csv(data: Dict, columns: List[str], file_name: str) -> None:
    """
    Writes the given dictionary into a csv file.

    :param data: Data to write into the file
    :param columns: Header for the csv
    :param file_name: file name to write the data

    :return: None
    """
    with open(file_name, 'w', newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()

        for key, value in data.items():
            writer.writerow(value)


if __name__ == "__main__":

    print("Reading files.....")
    file_t1, columns_t1 = read_csv_file("t1.csv")
    file_t2, columns_t2 = read_csv_file("t2.csv")

    print("Merging records.....")
    data_dict = {}
    create_merge_dict(file_t1, data_dict, DELETED_VAL)
    create_merge_dict(file_t2, data_dict, ADDED_VAL)

    print("Writing to the new file......")
    # Just in case if any file has extra columns
    merged_columns = list(set(columns_t1 + columns_t2))
    merged_columns.append(CHANGE_TYPE_KEY)
    dict_to_csv(data_dict, merged_columns, "t3.csv")
