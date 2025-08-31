from pathlib import Path


def count_ext(path: Path) -> dict[str, int]:
    """Count the number of files for each file extension in the given directory and its subdirectories.

    Args:
        path (Path): Path to search.

    Returns:
        dict[str, int]: A dictionary with file extensions as keys and their counts as values.
    """
    SKIP_EXTS = {".tmp", ".log", ".ini", ".zip", ".lrv", ".insv"}
    ext_count = {}

    for file in path.rglob("*"):
        if file.is_file():
            ext = file.suffix.lower()
            if ext in ext_count and ext not in SKIP_EXTS:
                ext_count[ext] += 1
            elif ext not in ext_count and ext not in SKIP_EXTS:
                ext_count[ext] = 1
            else:
                continue

    return ext_count


def compare_files(path1: Path, path2: Path) -> list[Path]:
    """Compare files in two directories and find files with the same name and returns name of files not exists in both directory.

    Args:
        path1 (Path): The first directory to compare.
        path2 (Path): The second directory to compare.

    Returns:
        list[Path]: A list of files that are unique to either directory."""
    SKIP_EXTS = {".tmp", ".log", ".ini", ".zip", ".lrv", ".insv"}
    files1 = {
        file.relative_to(path1)
        for file in path1.rglob("*")
        if file.is_file() and file.suffix not in SKIP_EXTS
    }
    files2 = {
        file.relative_to(path2)
        for file in path2.rglob("*")
        if file.is_file() and file.suffix not in SKIP_EXTS
    }

    unique = files1.symmetric_difference(files2)

    unique_files = []

    for rel_path in unique:
        if rel_path in files1:
            unique_files.append(path1 / rel_path)
        elif rel_path in files2:
            unique_files.append(path2 / rel_path)

    return unique_files


if __name__ == "__main__":
    first_path = Path(r"input().strip("\u202a")")
    second_path = Path(r"input().strip("\u202a")")
    print("First path:", count_ext(first_path))
    print("Second path:", count_ext(second_path))

    with open("unique_files.txt", "a+") as f:
        for file in compare_files(first_path, second_path):
            f.write(str(file) + "\n")
