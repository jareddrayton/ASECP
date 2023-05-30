import argparse
import glob
import json
import shutil
from pathlib import Path

from bs4 import BeautifulSoup

audio_control = """<td> <audio controls>
          <source src="{}" type="audio/wav">
          Your browser does not support the audio element.
        </audio> </td>"""

parser = argparse.ArgumentParser()
parser.add_argument("glob")
parser.add_argument("experiment_class")
parser.add_argument("experiment_name")
parser.add_argument("sound_option")
args = parser.parse_args()


glob_string = Path("C:\\Users\\Jazz\\VSCODE\\Repo\\ASECP\\thesis_data\\") / args.glob
experiment_class = args.experiment_class
experiment_name = args.experiment_name

sound_options = {"sounds_1": ['Primary1.wav', 'Primary4.wav', 'Primary8.wav'],
                 "sounds_2": [f'Primary{i}.wav' for i in range(1, 9)]}

sounds = sound_options[args.sound_option]
runs = 15

paths = glob.glob(str(glob_string))

output_path = Path.cwd() / 'docs' / experiment_class / experiment_name
output_index = output_path / "index.html"

if not output_path.exists():
    output_path.mkdir(parents=True)

html_output = ""

def get_best(path, run_id, vowel):
    with open(Path(path) / 'Best.txt', 'r') as f:
        individual = f.readlines()[-1].strip()

    with open(path + '\\arguments.json', 'r') as f:
        arguments = json.loads(f.read())
        final_generation = arguments["generation_size"]

    sound_file = Path(path) / f"Generation{final_generation}" / f"Individual{individual}.wav"

    filename = f"{vowel}Run{run_id}Individual{individual}.wav"
    return sound_file, filename


headers = "<tr>" + "<th>Run</th>" + "\n".join(["<th>{}</th>".format(sound.strip(".wav")) for sound in sounds]) + "</tr>"

def add_target_vowels():
    target_html = ""

    for vowel in sounds:
        filename = f"..\\..\\target_sounds\\{vowel}"
        target_html += audio_control.format(filename)

    return "<table>" + headers + "<tr><td></td>" + target_html + "</tr> </table>"


for run in range(1, runs + 1):
    sub_paths = sorted([path for path in paths if path.endswith("id" + str(run))])
    html_output += "<tr>"
    html_output += f"<td> {run} </td>\n"
    for sub_path, vowel in zip(sub_paths, sounds):
        html_output += ""

        if vowel not in sub_path:
            raise BaseException

        src_path, filename = get_best(sub_path, run, vowel)
        dst_path = output_path / filename

        shutil.copyfile(src_path, dst_path)
        html_output += audio_control.format(filename)
    html_output += "</tr>"

title = f"<h2>{experiment_class} {experiment_name}</h2>"

html_output = title + add_target_vowels() + "<table>" + headers + html_output + "</table>"


html_output = BeautifulSoup(html_output, 'html.parser').prettify()

with open(output_index, 'w') as fh:
    fh.write(html_output)
