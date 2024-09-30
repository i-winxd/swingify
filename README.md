# Swingify

**Puts any audio file into swing tempo.** Accepted formats: `mp3, wav, flac, ogg` because who would use anything else.

- Your audio must immediately start (no silence), just like how FNF songs are put into mods.
- **The tempo/BPM is one of the parameters for this program, so you need to know what the tempo of your song is.**
- No BPM changes. Too bad.
- No 7/8 time signatures or whatever that is. You know why.

## Download and installation

**you must have ffmpeg installed**

This is bundled in a single executable, which you can find in the releases tab (look out for the green `latest`, **literally** the first image when you search up `github releases` on Google tells you where it is).

Run the executable to launch up the GUI.

## Programmatic usage

```python
from swingify import swing_ify
from pathlib import Path

ts = swing_ify(Path("path/to/file.mp3"), 120)
ts.export(Path("path/to/output/mp3"), format="mp3")
```

## Quality

Slightly worse than if you did it in FL Studio. At least it's "faster"