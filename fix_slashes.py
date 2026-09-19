import argparse
import re
from pathlib import Path


HTML_PATH_RE = re.compile(r'(?P<attr>src|href)\s*=\s*["\'](?P<value>[^"\']+)["\']', re.IGNORECASE)


def fix_path_value(value: str) -> str:
    """Change backslashes to forward slashes in a path-like string."""
    return value.replace('\\', '/')


def fix_file(path: Path) -> None:
    text = path.read_text(encoding='utf-8')

    def replace(match):
        attr = match.group('attr')
        value = match.group('value')
        new_value = fix_path_value(value)
        return f'{attr}="{new_value}"'

    updated = HTML_PATH_RE.sub(replace, text)

    if updated != text:
        path.write_text(updated, encoding='utf-8')
        print(f'Fixed: {path}')
    else:
        print(f'No changes: {path}')


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Replace backslashes with forward slashes in HTML src/href paths.'
    )
    parser.add_argument('path', help='File or folder to fix.')
    args = parser.parse_args()

    target = Path(args.path)

    if target.is_file():
        fix_file(target)
    elif target.is_dir():
        for file in target.rglob('*'):
            if file.is_file() and file.suffix.lower() in {'.html', '.htm', '.css', '.js'}:
                fix_file(file)
    else:
        print(f'Not found: {target}')


if __name__ == '__main__':
    main()
