import tempfile
from pathlib import Path
import unittest
from core import parse_subtitles,caption_at,decode_subtitles,safe_source,read_m3u,write_m3u,clock

class CoreTests(unittest.TestCase):
    def test_real_srt_with_overlap_and_markup(self):
        cues=parse_subtitles('1\n00:00:01,200 --> 00:00:03,000\n<b>¡Hola!</b>\n\n2\n00:00:02,000 --> 00:00:04,000\nBonjour\nEncore\n')
        self.assertEqual(caption_at(cues,2200),'¡Hola!\nBonjour\nEncore')
        self.assertEqual(caption_at(cues,3200,1000),'¡Hola!\nBonjour\nEncore')
        self.assertEqual(caption_at(cues,4000),'')
    def test_webvtt_cue_settings_utf16_and_cp1252(self):
        text='WEBVTT\n\n00:01.500 --> 00:03.000 align:start\nFrançais\n'
        cues=parse_subtitles(decode_subtitles(text.encode('utf-16')))
        self.assertEqual(caption_at(cues,1500),'Français')
        self.assertEqual(decode_subtitles('Español'.encode('cp1252')),'Español')
        self.assertEqual(parse_subtitles('00:02.000 --> 00:01.000\ninvalid'),[])
    def test_playlist_relative_paths_and_urls(self):
        target=Path(__file__).resolve().parents[1]/'test-output'; target.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=target) as folder:
            file=Path(folder)/'list.m3u8';file.write_text('#EXTM3U\nclip.mp4\nhttps://example.com/test.webm\n',encoding='utf-8')
            values=read_m3u(file); self.assertEqual(values[0],str((Path(folder)/'clip.mp4').resolve()))
            self.assertIn('https://example.com/test.webm',write_m3u(values))
    def test_reject_unintended_protocols_and_credentials(self):
        for value in ['javascript:alert(1)','file:///secret','ftp://example.com/file','https://user:pass@example.com/test']:
            with self.assertRaises(ValueError):safe_source(value)
        self.assertEqual(safe_source('https://example.com/test'),'https://example.com/test')
    def test_clock(self):
        self.assertEqual(clock(3661000),'1:01:01');self.assertEqual(clock(-20),'00:00')

if __name__=='__main__':unittest.main()
