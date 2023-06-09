import os
import pwd
import grp
import argparse
from datetime import datetime

def format_file_size(size):
    """Formatuje rozmiar pliku na czytelną postać."""
    units = ["B", "KB", "MB", "GB", "TB"]
    index = 0
    while size >= 1024 and index < len(units) - 1:
        size /= 1024
        index += 1
    return f"{size:.2f} {units[index]}"

def get_owner_name(uid):
    """Zwraca nazwę użytkownika na podstawie UID."""
    try:
        return pwd.getpwuid(uid).pw_name
    except KeyError:
        return str(uid)

def get_group_name(gid):
    """Zwraca nazwę grupy na podstawie GID."""
    try:
        return grp.getgrgid(gid).gr_name
    except KeyError:
        return str(gid)

def ls(directory, options):
    """Wyświetla listę plików w katalogu."""
    files = os.listdir(directory)
    files.sort()

    if not options.all:
        files = [f for f in files if not f.startswith(".")]

    # Sortowanie plików
    if options.sort_by_time:
        files.sort(key=lambda f: os.path.getmtime(os.path.join(args.directory, f)), reverse=args.reverse)
    elif options.sort_by_size:
        files.sort(key=lambda f: os.path.getsize(os.path.join(args.directory, f)), reverse=args.reverse)
    else:
        files.sort(reverse=args.reverse)

    # Filtracja plików
    if options.user:
        uid = pwd.getpwnam(args.user).pw_uid
        files = [f for f in files if os.stat(os.path.join(args.directory, f)).st_uid == uid]

    if options.group:
        gid = grp.getgrnam(args.group).gr_gid
        files = [f for f in files if os.stat(os.path.join(args.directory, f)).st_gid == gid]


    if options.long_format:
        print("Permissions   Links   Owner    Group    Size       Last Modified  Name")
        print("--------------------------------------------------------------------")

        for file in files:
            file_path = os.path.join(directory, file)
            file_stats = os.stat(file_path)
            permissions = oct(file_stats.st_mode)[-3:]
            links = file_stats.st_nlink
            owner = get_owner_name(file_stats.st_uid)
            group = get_group_name(file_stats.st_gid)
            size = format_file_size(file_stats.st_size)
            modified = datetime.fromtimestamp(file_stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            print(f"{permissions}          {links}      {owner}      {group}      {size}  {modified}  {file}")
    elif options.one_per_line:
        print("\n".join(files))
    else:
        num_columns = options.columns
        num_files = len(files)
        num_rows = (num_files + num_columns - 1) // num_columns
        column_width = max(len(file) for file in files) + 2

        for i in range(num_rows):
            row_files = files[i::num_rows]
            row_entries = [file.ljust(column_width) for file in row_files]
            print("".join(row_entries))

# Przykład użycia
parser = argparse.ArgumentParser(description="Polecenie ls w Pythonie.")
parser.add_argument("directory", nargs="?", default=".", help="Ścieżka do katalogu.")
parser.add_argument("-a", "--all", action="store_true", help="Wyświetla wszystkie pliki.")
parser.add_argument("-l", "--long-format", action="store_true", help="Wyświetla szczegółowe informacje o plikach.")
parser.add_argument("-1", "--one-per-line", action="store_true", help="Wyświetla każdy plik w osobnej linii.")
parser.add_argument("-C", "--columns", type=int, default=80, help="Liczba kolumn dla wyświetlania plików.")
parser.add_argument("-r", "--reverse", action="store_true", help="Odwraca kolejność wyświetlania plików.")
parser.add_argument("-t", "--sort-by-time", action="store_true", help="Sortuje pliki według czasu modyfikacji.")
parser.add_argument("-S", "--sort-by-size", action="store_true", help="Sortuje pliki według rozmiaru.")
parser.add_argument("-u", "--user", help="Filtruje pliki dla podanego użytkownika.")
parser.add_argument("-g", "--group", help="Filtruje pliki dla podanej grupy.")

args = parser.parse_args()


ls(args.directory, args)
