import argparse
import re
from pathlib import Path


HTML_PATH_RE = re.compile(r'(?P<attr>src|href)\s*=\s*["\'](?P<value>[^"\']+)["\']', re.IGNORECASE)
CSS_URL_RE = re.compile(r'url\(\s*["\']?(?P<value>[^)"\']+)["\']?\s*\)', re.IGNORECASE)


def fix_path_value(value: str) -> str:
    """Replace backslashes with forward slashes in a path string."""
    return value.replace('\\', '/')


def fix_file(path: Path) -> None:
    text = path.read_text(encoding='utf-8')

    def replace_html(match):
        value = match.group('value')
        new_value = fix_path_value(value)
        attr = match.group('attr')
        return f'{attr}="{new_value}"'

    def replace_css(match):
        value = match.group('value')
        new_value = fix_path_value(value)
        return f'url({new_value})'

    updated = HTML_PATH_RE.sub(replace_html, text)
    updated = CSS_URL_RE.sub(replace_css, updated)

    if updated != text:
        path.write_text(updated, encoding='utf-8')
        print(f'Fixed: {path}')
    else:
        print(f'No changes: {path}')


def process_target(target: Path) -> None:
    """Fix one file or one folder. Nothing happens unless a target is given."""
    if target.is_file():
        fix_file(target)
    elif target.is_dir():
        for file in target.rglob('*'):
            if file.is_file() and file.suffix.lower() in {'.html', '.htm', '.css', '.js'}:
                fix_file(file)
    else:
        print(f'Not found: {target}')


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Replace backslashes with forward slashes in HTML and CSS paths.'
    )
    parser.add_argument(
        'path',
        nargs='?',
        default=None,
        help='File or folder to fix. If omitted, it will ask for a target.'
    )
    args = parser.parse_args()

    if args.path is None:
        print('Please provide a file or folder path, for example:')
        print('  python fix_slashes.py index.html')
        print('  python fix_slashes.py Articles')
        return

    process_target(Path(args.path))


if __name__ == '__main__':
    main()
