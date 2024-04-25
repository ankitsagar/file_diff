# CSV File Diff Checker

Takes two CSV files as argument and checks if the first file entry is changed or not in the second file if changed.
It adds a new column change type in the output CSV if the entry is changed then value will be changed if row is not present in the second file then it's deleted if it's only present in second file then it's added.

## Installation and setup

Just python needs to be installed on you system no need of any addition package or tool
This was tested on python 3.11.

### How to run?
This will save the diff in t3.csv in current path.
```
$ python main.py test_files/t1.csv test_files/t2.csv
```
if you need custom diff file path then run
```
$ python main.py test_files/t1.csv test_files/t2.csv --diff_path diff.csv
```