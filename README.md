# Simple python script to find subfolders to delete

Simple python script to find subfolders in a large file system tree up to a maxdepth (path) and delete them based on a simple regex.
The only python dependency is [click](https://github.com/pallets/click/)

**Windows only right now** - uses robocopy to purge folder contents as apparently long folder names are not supportet in shutil.rmtree, Powershell's Remove-Item or rmdir /s /q. bummer. Should be very easily ported to posix systems.

Please be sure to test before you use this. It's been written quickly to solve a urgent problem. 

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
  --dry-run          Do not actually delete anything.
  --help             Show this message and exit.
````


## Install

Use pipenv to install click and you're good to go.