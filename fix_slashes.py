import argparse
import re
from pathlib import Path


HTML_ATTR_RE = re.compile(
    r'(?P<prefix>(?:href|src|action|poster|data|content)\s*=\s*["\'])(?P<value>[^"\']*?)(?P<suffix>["\'])',
    re.IGNORECASE,
)

CSS_URL_RE = re.compile(
    r'url\(\s*(?P<quote>["\']?)(?P<value>[^)"\']+?)(?P=quote)\s*\)',
    re.IGNORECASE,
)


def normalize_path_value(value: str) -> str:
    """Convert Windows-style separators only in path-like text."""
    return value.replace('\\', '/')


def convert_backslashes_to_forward(path: Path) -> int:
    """Normalize path-like backslashes in common web file references.

    This is safer than replacing every backslash in the file, because it only
    touches values in HTML attributes such as src/href and CSS url(...).
    """
    text = path.read_text(encoding='utf-8')

    def replace_html_attr(match: re.Match[str]) -> str:
        value = match.group('value')
        new_value = normalize_path_value(value)
        return f"{match.group('prefix')}{new_value}{match.group('suffix')}"

    def replace_css_url(match: re.Match[str]) -> str:
        value = match.group('value')
        new_value = normalize_path_value(value)
        return f"url({match.group('quote')}{new_value}{match.group('quote')})"

    updated = HTML_ATTR_RE.sub(replace_html_attr, text)
    updated = CSS_URL_RE.sub(replace_css_url, updated)

    if updated != text:
        path.write_text(updated, encoding='utf-8')
        print(f'Updated: {path}')
        return 1

    print(f'No changes: {path}')
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Convert Windows backslashes to forward slashes in text files.'
    )
    parser.add_argument(
        'paths',
        nargs='+',
        help='One or more files or folders to process.'
    )
    parser.add_argument(
        '--ext',
        nargs='*',
        default=['.html', '.htm', '.css', '.js', '.txt'],
        help='File extensions to include when a folder is given.'
    )

    args = parser.parse_args()
    changed_files = 0

    for input_path in args.paths:
        p = Path(input_path)

        if p.is_file():
            if p.suffix.lower() in args.ext:
                changed_files += convert_backslashes_to_forward(p)
            else:
                print(f'Skipped: {p} (extension not selected)')
        elif p.is_dir():
            for file in p.rglob('*'):
                if file.is_file() and file.suffix.lower() in args.ext:
                    changed_files += convert_backslashes_to_forward(file)
        else:
            print(f'Not found: {p}')

    print(f'\nFinished. Updated {changed_files} file(s).')


if __name__ == '__main__':
    main()
