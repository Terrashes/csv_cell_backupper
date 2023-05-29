# CSV_cell_backupper
Backup CSV cells to JSON that exceed the maximum length supported by office programs to prevent them from being cut off.

## Execute script using Python

1. Install Python 3
2. Use command **py main.py** on Windows (or **python3 main.py** on Linux)

## Build binaries from source

1. Install Python 3
2. Install Pyinstaller module
3. Use command **pyinstaller --onefile --icon=icon.ico --noconsole main.py**

## Use

1. Run program before opening CSV file in text editor
2. Select a file
3. Press "Save to JSON"
4. Do anything you need with file
5. Press "Restore from JSON"
