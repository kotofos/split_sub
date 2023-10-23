import re
from itertools import groupby
from typing import NamedTuple, List


class Dialogue(NamedTuple):
    time: str
    character: str
    line: str


def run(text: str) -> str:
    if '[Script Info]' in text:
        res = process_ass(text)
    else:
        res = process_srt(text)

    return format_output(res)


def process_srt(text: str) -> List[Dialogue]:
    """
    Process srt subtitles with special format, when speaker is specified.
    # format:
    # number \n
    # time from --> to\n
    # text lines \n
    """

    dialogues: List[Dialogue] = []

    # "chunk" our input file, delimited by blank lines
    text = text.splitlines()
    res = [list(g) for b, g in groupby(text, lambda x: bool(x.strip())) if b]

    for sub in res:
        if len(sub) >= 3:  # not strictly necessary, but better safe than sorry
            sub = [x.strip() for x in sub]
            number, start_end, *content = sub  # py3 syntax
            time, _ = start_end.split(' --> ')

            time = time[3:8]  # get mm:ss

            content = '\n'.join(content)
            # get characters count
            char_count = len(re.findall(r'(\w+):[\t ]*', content))

            # one character
            if char_count == 1:
                # get character and line
                line_match = re.search(r'^(\w+):[\t ]*([\s\S]*)', content)

                line = line_match.group(2)
                line = ' '.join(line.splitlines())

                character = line_match.group(1)
                dialogues.append(Dialogue(time, character, line))

            # multiple characters at same time at each line
            elif char_count > 1:
                # get characters and lines
                match = re.findall(r'(\w+):[\t ]+(.*)', content)
                for sub_item in match:
                    character = sub_item[0]
                    line = sub_item[1]
                    line = ' '.join(line.splitlines())
                    dialogues.append(Dialogue(time, character, line))
            else:
                # continuation of previous character line
                prev = dialogues.pop()
                time = prev.time
                character = prev.character
                prev_line = prev.line
                line = content.strip()

                line = prev_line + ' ' + line

                dialogues.append(Dialogue(time, character, line))

    return dialogues


def process_ass(text: str) -> List[Dialogue]:
    dialogues = []
    text = iter(text.splitlines())

    while True:
        line = next(text)
        if '[Events]' in line:
            break
    next(text)  # skip header

    for line in text:
        comma_count = 0
        for idx, c in enumerate(line):
            if c == ',':
                comma_count += 1
                if comma_count == 1:
                    time_idx = idx + 1
                if comma_count == 2:
                    time_end_idx = idx

                if comma_count == 3:
                    pony_idx = idx + 1
                if comma_count == 4:
                    pony_end_idx = idx

                if comma_count == 9:
                    txt_idx = idx + 1
                    break

        dialogues.append(
            Dialogue(time=line[time_idx + 2:time_end_idx - 3],
                     character=line[pony_idx:pony_end_idx],
                     line=line[txt_idx:-1])
        )

    return dialogues


def format_output(dialogues: List[Dialogue]) -> str:
    dialogues.sort(key=lambda x: x.character)
    out = []
    for d in dialogues:
        out.append('{} {}: {}'.format(*d))

    out = '\n'.join(out)
    return out