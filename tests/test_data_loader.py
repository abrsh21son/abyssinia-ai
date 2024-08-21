import os
import tempfile
from code.rag_assistant.data_loader import list_text_files


def test_returns_txt_only():
    with tempfile.TemporaryDirectory() as tmpdir:
        open(os.path.join(tmpdir, 'a.txt'), 'w').close()
        open(os.path.join(tmpdir, 'b.md'), 'w').close()
        open(os.path.join(tmpdir, 'c.csv'), 'w').close()
        files = list_text_files(tmpdir)
        assert len(files) == 1
        assert all(f.endswith('.txt') for f in files)


def test_returns_sorted():
    with tempfile.TemporaryDirectory() as tmpdir:
        for name in ['z.txt', 'a.txt', 'm.txt']:
            open(os.path.join(tmpdir, name), 'w').close()
        files = list_text_files(tmpdir)
        assert files == sorted(files)


def test_empty_dir_returns_empty_list():
    with tempfile.TemporaryDirectory() as tmpdir:
        assert list_text_files(tmpdir) == []