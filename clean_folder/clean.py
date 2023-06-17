import shutil
from pathlib import Path
import sys
import uuid

CATEGORIES = {
    "Audio": [".mp3", ".aiff", ".ogg", ".wav", ".amr"],
    "Documents": [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"],
    "Images": [".jpeg", ".png", ".jpg", ".svg"],
    "Video": [".avi", ".mp4", ".mov", ".mkv"],
    "Archives": [".zip", ".gz", ".tar"],
    "Other": [],
}


def get_categories(path: Path) -> str:
    ext = path.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat

    return "Other"


def move_file(file: Path, root_dir: Path, category: str) -> None:
    target_dir = root_dir.joinpath(category)
    if not target_dir.exists():
        target_dir.mkdir()
    new_name = target_dir.joinpath(f"{normalize(file.stem)}{file.suffix}")
    if new_name.exists():
        new_name = new_name.with_name(
            f"{new_name.stem}-{uuid.uuid4()}{file.suffix}")
    file.rename(new_name)


def sort_folder(path: Path) -> None:
    for item in path.glob("**/*"):
        if item.is_file():
            if item.parent.name not in CATEGORIES.keys():
                cat = get_categories(item)
                move_file(item, path, cat)


def delete_empty_folders(path: Path) -> None:
    for item in path.iterdir():
        if item.is_dir():
            delete_empty_folders(item)
            if not any(item.iterdir()):
                item.rmdir()


def unpack_archive(path: Path) -> None:
    path_arh = path.joinpath("Archives")

    for item in path_arh.iterdir():
        arch_folder = path_arh.joinpath(
            item.stem + "_" + item.suffix.lower()[1:])

        if not arch_folder.exists():
            arch_folder.mkdir()

        unpacked_file = str(path_arh) + "\\" + item.name

        try:
            shutil.unpack_archive(unpacked_file, str(arch_folder))

        except shutil.ReadError:
            print(f"Can't extract {item.name}")


def normalize(in_name):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"

    TRANSLATION = (
        "a",
        "b",
        "v",
        "g",
        "d",
        "e",
        "e",
        "j",
        "z",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "r",
        "s",
        "t",
        "u",
        "f",
        "h",
        "ts",
        "ch",
        "sh",
        "sch",
        "",
        "y",
        "",
        "e",
        "yu",
        "ya",
        "je",
        "i",
        "ji",
        "g",
    )

    TRANS = {}
    for cyr, lat in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(cyr)] = lat
        TRANS[ord(cyr.upper())] = lat.upper()
        in_name = in_name.translate(TRANS)
        out_name = ""

    for i in in_name:
        if (
            i == "."
            or (ord(i) >= 65 and ord(i) <= 90)
            or (ord(i) >= 97 and ord(i) <= 122)
            or (ord(i) >= 48 and ord(i) <= 57)
        ):
            out_name += i
        else:
            out_name += "_"
    return out_name


def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "You must point the Folder's name!"

    if not path.exists():
        return f"The folder {path} doesn't exist !"

    sort_folder(path)

    unpack_archive(path)
    delete_empty_folders(path)

    All_Files = {
        "Audio": [],
        "Documents": [],
        "Images": [],
        "Video": [],
        "Archives": [],
        "Other": [],
    }

    unknown_ext = set()
    known_ext = set()
    for item in path.iterdir():
        for file in item.iterdir():
            if file.is_file():
                All_Files[item.name].append(file.name)
            if item.name == "Other":
                unknown_ext.add(file.suffix)
            else:
                known_ext.add(file.suffix)

    for key, val in All_Files.items():
        print(f'In folder "{key}" there are following files: {val}')

    print(f"There are known extensions in folder : {known_ext}")
    print(f"I don't know such extensions : {unknown_ext}")

    return "I've done everything I could"


if __name__ == "__main__":
    print(main())
