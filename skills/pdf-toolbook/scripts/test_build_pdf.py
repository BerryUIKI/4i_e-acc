"""Regression checks for manuscript-to-PDF content preservation."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('builder', Path(__file__).with_name('build_pdf.py'))
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class ContentPreservation(unittest.TestCase):
    def test_nested_pdf_keeps_sources_in_build_directory(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            work = base / 'build/book'
            work.mkdir(parents=True)
            merged = work / 'merged.md'
            merged.write_text('# Chapter', encoding='utf-8')
            target = base / 'pdf/book.pdf'

            def fake_tex(template, source, target_tex, *args):
                target_tex.write_text('source', encoding='utf-8')

            def fake_compile(tex, directory, passes):
                self.assertEqual(passes, 3)
                (directory / 'book.pdf').write_bytes(b'%PDF-test')
                return True

            with patch.object(builder, 'generate_tex', side_effect=fake_tex), \
                 patch.object(builder, 'should_split', return_value=False), \
                 patch.object(builder, 'run_xelatex', side_effect=fake_compile):
                self.assertTrue(builder.compile_pdf('template', merged, target))
            self.assertEqual(target.read_bytes(), b'%PDF-test')
            self.assertTrue((work / 'book.tex').exists())
            self.assertTrue(merged.exists())
            self.assertEqual([p.name for p in target.parent.iterdir()], ['book.pdf'])

    def test_image_attributes_survive_preprocessing_and_resolution(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            (base / 'art.png').touch()
            source = '之前![概念](art.png){width=115mm}之后'
            actual = builder.preprocess_markdown(builder.resolve_image_paths(source, base))
            self.assertIn(f'![概念]({(base / "art.png").as_posix()}){{width=115mm}}', actual)
            self.assertNotIn(')\n\n{width', actual)

    def test_chinese_quotes_preserve_code_and_urls(self):
        source = '称作"长期目标"，英文 "cash"。\n`{"用途":"中文"}`\n```json\n{"用途":"中文"}\n```\n[原文](https://example.org/)'
        actual = builder.normalize_chinese_quotes(source)
        self.assertIn('称作“长期目标”', actual)
        self.assertIn('英文 "cash"', actual)
        self.assertIn('`{"用途":"中文"}`', actual)
        self.assertIn('```json\n{"用途":"中文"}\n```', actual)
        self.assertIn('https://example.org/', actual)

    def test_epilogue_starts_unnumbered_backmatter(self):
        entries = builder.parse_index((builder.WORKSPACE_ROOT / 'book-task.md').read_text(encoding='utf-8'))
        with tempfile.TemporaryDirectory() as folder:
            path, _ = builder.merge_markdown(entries, Path(folder) / 'merged.md')
            merged = path.read_text(encoding='utf-8')
        self.assertLess(merged.index('\\backmatter'), merged.index('# 终章'))
        self.assertEqual(merged.count('\\backmatter'), 1)
        self.assertNotIn('# 目录 · Table', merged)
        self.assertIn('review-opening-v1.png){width=115mm}', merged)


if __name__ == '__main__':
    unittest.main()
