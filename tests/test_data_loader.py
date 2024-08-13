import os
import tempfile
from code.rag_assistant.data_loader import list_text_files


def test_returns_txt_only():
    with tempfile.TemporaryDirectory() as tmpdir:
        open(os.path.join(tmpdir, 'a.txt'), 'w').close()
        open(os.path.join(tmpdir, 'b.md'), 'w').close()
        files = list_text_files(tmpdir)
        assert len(files) == 1
        assert files[0].endswith('.txt')


def test_returns_sorted():
    with tempfile.TemporaryDirectory() as tmpdir:
        open(os.path.join(tmpdir, 'z.txt'), 'w').close()
        open(os.path.join(tmpdir, 'a.txt'), 'w').close()
        files = list_text_files(tmpdir)
        assert files == sorted(files)