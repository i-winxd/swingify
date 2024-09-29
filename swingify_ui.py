from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from swingify import swing_ify
from ui import DataclassUI


@dataclass
class Ipt(DataclassUI):
    bpm: float
    input: Path = field(metadata={
        'filetypes': [('MUSIC', '.wav .mp3 .ogg .flac')]
    })
    output: Path = field(metadata={
        'filetypes': [('MUSIC', '.wav .mp3 .ogg .flac')],
        'save': True,
        'defaultextension': '.wav'
    })


def sf_validate(ipt: Ipt) -> Optional[str]:
    if ipt.bpm < 1:
        return "Nonsensical would be a negative BPM"
    if ipt.input.__str__() == ".":
        return "Please select an input"
    if ipt.output.__str__() == ".":
        return "Please select an output"
    else:
        return None


if __name__ == '__main__':
    ps = Ipt.get_instance_from_ui(title="TO SWING CONVERTER", desc="Converts any audio file to swing tempo",
                                  custom_check=sf_validate
                                  )
    ts = swing_ify(ps.input, ps.bpm)
    ts.export(ps.output, format=ps.output.suffix.removeprefix("."))
