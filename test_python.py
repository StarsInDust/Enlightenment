import os
import sys
from pathlib import Path

from fix_slashes import main, normalize_input_path


def test_normalize_input_path_replaces_windows_separators():
    assert normalize_input_path(r'.\Articles\2026\1_Screen_Reader_Compatibility') == Path(
        'Articles/2026/1_Screen_Reader_Compatibility'
    )


def test_main_accepts_windows_relative_path(tmp_path, monkeypatch):
    page = tmp_path / 'page.html'
    page.write_text(
        '<a href="images\\photo.jpg">x</a>\n<style>body{background:url(images\\bg.png)}</style>',
        encoding='utf-8',
    )

    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        monkeypatch.setattr(sys, 'argv', ['fix_slashes.py', r'.\page.html'])
        main()
    finally:
        os.chdir(old_cwd)

    text = page.read_text(encoding='utf-8')
    assert 'images/photo.jpg' in text
    assert 'images/bg.png' in text
