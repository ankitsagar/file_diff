import argparse
import os.path


def get_args():
    """ Parse and validate arguments given by client """
    parser = argparse.ArgumentParser()
    parser.add_argument("first_file", help="Location of first file")
    parser.add_argument("second_file", help="Location of second file")
    parser.add_argument(
        "--diff_path",
        help="Location of destination file where diff will get saved",
        required=False,
        default="t3.csv"
    )
    return parser.parse_args()


def validate_path(path: str):
    """ Validated given path exists """
    if not os.path.isfile(path):
        print(f"Target file: {path} doesn't exist")
        raise SystemExit(1)
