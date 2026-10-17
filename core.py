"""Playlist and subtitle operations; no UI or network dependencies."""
from dataclasses import dataclass
from pathlib import Path
import re
from urllib.parse import urlparse

MEDIA_EXTENSIONS = {'.mp4', '.m4v', '.mkv', '.webm', '.mov', '.avi', '.wmv', '.mpeg', '.mpg', '.ts', '.m2ts', '.ogv', '.3gp', '.flv', '.mp3', '.flac', '.ogg', '.wav', '.m4a', '.aac', '.opus'}

@dataclass(frozen=True)
class Cue:
    start: int
    end: int
    text: str

def timestamp(value):
    parts = value.strip().replace(',', '.').split(':')
    if len(parts) not in (2, 3):
        raise ValueError('Invalid subtitle timestamp')
    numbers = [float(p) for p in parts]
    if any(n < 0 for n in numbers):
        raise ValueError('Negative timestamp')
    return round(sum(n * 60 ** i for i, n in enumerate(reversed(numbers))) * 1000)

def parse_subtitles(text):
    """SRT/WebVTT text, plain captions only; ignore styling/position markup."""
    cues = []
    for block in re.split(r'\n\s*\n', text.replace('\r\n', '\n').lstrip('\ufeff')):
        lines = block.strip().splitlines()
        for i, line in enumerate(lines):
            match = re.match(r'^([\d:.,]+)\s*-->\s*([\d:.,]+)', line)
            if match:
                start, end = map(timestamp, match.groups())
                caption = re.sub(r'<[^>]*>', '', '\n'.join(lines[i+1:])).strip()
                if end > start and caption:
                    cues.append(Cue(start, end, caption))
                break
    return sorted(cues, key=lambda c: c.start)

def caption_at(cues, position, delay=0):
    return '\n'.join(c.text for c in cues if c.start <= position-delay < c.end)

def decode_subtitles(data):
    if data.startswith((b'\xff\xfe', b'\xfe\xff')):
        return data.decode('utf-16')
    try:
        return data.decode('utf-8-sig')
    except UnicodeDecodeError:
        return data.decode('cp1252', errors='replace')

def safe_source(value, base=None):
    value = str(value).strip()
    # Drive letters are paths, not URI schemes.
    if re.match(r'^[A-Za-z]:[\\/]', value):
        return str(Path(value))
    parsed = urlparse(value)
    if parsed.scheme:
        if parsed.scheme.lower() not in ('http', 'https') or not parsed.hostname or parsed.username or parsed.password:
            raise ValueError('Only HTTP(S) URLs without embedded credentials are supported')
        return value
    path = Path(value)
    return str(((Path(base) / path) if base and not path.is_absolute() else path).resolve())

def read_m3u(path):
    path = Path(path)
    return [safe_source(line, path.parent) for line in decode_subtitles(path.read_bytes()).splitlines() if line.strip() and not line.lstrip().startswith('#')]

def write_m3u(sources):
    return '#EXTM3U\n' + '\n'.join(s.replace('\n', '').replace('\r', '') for s in sources) + '\n'

def clock(milliseconds):
    seconds = max(0, int(milliseconds // 1000))
    hours, rest = divmod(seconds, 3600)
    minutes, seconds = divmod(rest, 60)
    return f'{hours}:{minutes:02}:{seconds:02}' if hours else f'{minutes:02}:{seconds:02}'

