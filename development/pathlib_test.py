from pathlib import Path
if len(list(Path("./").glob('reac*'))) != 0:
    print(len(list(Path("./").glob('reac*'))))
