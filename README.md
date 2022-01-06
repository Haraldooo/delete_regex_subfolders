# Simple python script to find subfolders to delete

Simple python script to find subfolders in a large file system tree to delete based on a simple regex.
The only dependency is [click](https://github.com/pallets/click/)
Please be sure to test before you use this. It's been written fast to solve a specific problem. 

## Usage

First configure the regex match you need in the source code and then run the script.
Also be sure to set the "older than check" in the source.
The first run should be ````python main.py -c ```` to scan your folder structure for the folders to delete. It will create a sqlite-db to keep track of the progress. To see the folders found just check the folder-list.db (e.g. with sqlite cli client or the excellent [sqlitestudio](https://github.com/pawelsalawa/sqlitestudio))


````
Usage: main.py [OPTIONS]

Options:
  --top-dir TEXT     Defines the top of the tree..   [required]
  -c, --create-list  Create folder list file.
  -d, --delete
  --help             Show this message and exit.
````


## Install

Use pipenv to install click and you're good to go.