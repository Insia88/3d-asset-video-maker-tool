"""Regression checks for public links in copied research checkpoints."""
import tempfile
import unittest
from pathlib import Path
from urllib.parse import quote

from import_research import ExportError, Sanitizer, document_links, rewrite_markdown


class CheckpointDocumentLinks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.source, self.prior, self.other, self.output = [self.base / n for n in ('current', 'prior', 'other', 'public')]
        for directory in (self.source, self.prior, self.other):
            directory.mkdir()
            (directory / '01_뷰티 분석.md').write_text('# Beauty', encoding='utf-8')
        (self.prior / 'private.md').write_text('Private evidence', encoding='utf-8')
        (self.prior / 'proof.png').write_bytes(b'private image')
        self.current_file = self.source / '00_index.md'
        self.current_file.write_text('# Index', encoding='utf-8')
        self.documents = [self.current_file, self.source / '01_뷰티 분석.md']
        self.docs_rel = Path('docs/research/2026-10-05')

    def rewrite(self, text, aliases=()):
        mapping = document_links(self.documents, self.source, self.output, self.docs_rel, aliases)
        return rewrite_markdown(text, self.current_file, self.output / self.docs_rel / self.current_file.name,
                                mapping, self.output / 'data/references/index.json', Sanitizer(),
                                audit_file=self.output / 'data/audit.json', snapshot_file=self.output / 'manifests/snapshot.json')

    def test_prior_absolute_link_requires_explicit_alias(self):
        text = f'[Beauty](<{(self.prior / "01_뷰티 분석.md").as_posix()}>)'
        self.assertNotIn('[Beauty]', self.rewrite(text))
        self.assertIn('[Beauty](<01_%EB%B7%B0%ED%8B%B0%20%EB%B6%84%EC%84%9D.md>)', self.rewrite(text, (self.prior,)))

    def test_percent_encoded_current_link_and_fragment(self):
        text = '[Beauty](<' + quote('01_뷰티 분석.md') + '#growth>)'
        self.assertIn('[Beauty](<01_%EB%B7%B0%ED%8B%B0%20%EB%B6%84%EC%84%9D.md#growth>)', self.rewrite(text))

    def test_percent_encoded_prior_absolute_link(self):
        text = '[Prior](<' + quote((self.prior / '01_뷰티 분석.md').as_posix()) + '#growth>)'
        self.assertIn('[Prior](<01_%EB%B7%B0%ED%8B%B0%20%EB%B6%84%EC%84%9D.md#growth>)', self.rewrite(text, (self.prior,)))

    def test_alias_symlink_cannot_escape_checkpoint(self):
        prior_file = self.prior / '01_뷰티 분석.md'
        prior_file.unlink()
        try:
            prior_file.symlink_to(self.other / '01_뷰티 분석.md')
        except (OSError, NotImplementedError):
            self.skipTest('Temporary symlink creation is unavailable on this host.')
        self.assertNotIn('[Escaped]', self.rewrite(f'[Escaped](<{prior_file.as_posix()}>)', (self.prior,)))

    def test_private_image_and_unexported_markdown_stay_redacted(self):
        text = f'![Proof](<{(self.prior / "proof.png").as_posix()}>) [Private](<{(self.prior / "private.md").as_posix()}>)'
        result = self.rewrite(text, (self.prior,))
        self.assertNotIn('[Proof]', result)
        self.assertNotIn('[Private]', result)
        self.assertNotIn(self.prior.as_posix(), result)

    def test_same_basename_outside_alias_does_not_resolve(self):
        text = f'[Other](<{(self.other / "01_뷰티 분석.md").as_posix()}>)'
        self.assertNotIn('[Other]', self.rewrite(text, (self.prior,)))

    def test_alias_does_not_create_missing_document(self):
        (self.prior / '01_뷰티 분석.md').unlink()
        text = f'[Missing](<{(self.prior / "01_뷰티 분석.md").as_posix()}>)'
        self.assertNotIn('[Missing]', self.rewrite(text, (self.prior,)))

    def test_missing_alias_directory_is_rejected(self):
        with self.assertRaises(ExportError):
            self.rewrite('# Index', (self.base / 'missing',))


if __name__ == '__main__':
    unittest.main()
