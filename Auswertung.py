import csv
from pathlib import Path
import re
#Pfade je nach auszuwertenden Output anpassen
output_folder = Path(r"\Outputs\results_openai")
output_csv = r"\OpenAi-binaer.csv"
#Label-Mapping
standard_labels = [
    "Loaded Language",
    "Name Calling / Labeling",
    "Repetition",
    "Exaggeration / Minimization",
    "Doubt",
    "Appeal to fear-prejudice",
    "Flag-Waving",
    "Causal Oversimplification",
    "Slogans",
    "Appeal to Authority",
    "Black-and-White Fallacy",
    "Thought-terminating Cliches",
    "Bandwagon,Reductio ad Hitlerum",
    "Whataboutism,Straw_Men,Red_Herring"
]

technique_map = {
    "Name calling": "Name Calling / Labeling",
    "Name Calling": "Name Calling / Labeling",
    "Labeling": "Name Calling / Labeling",
    "Repetition": "Repetition",
    "Slogans": "Slogans",
    "Appeal to fear": "Appeal to fear-prejudice",
    "Appeal to fear-prejudice": "Appeal to fear-prejudice",
    "Doubt": "Doubt",
    "Exaggeration/minimization": "Exaggeration / Minimization",
    "Exaggeration/Minimization": "Exaggeration / Minimization",
    "Flag-Waving": "Flag-Waving",
    "Flag-waving": "Flag-Waving",
    "Loaded Language": "Loaded Language",
    "Reduction ad Hitlerum": "Bandwagon,Reductio ad Hitlerum",
    "Bandwagon": "Bandwagon,Reductio ad Hitlerum",
    "Bandwagon,Reductio ad Hitlerum": "Bandwagon,Reductio ad Hitlerum",
    "Causal Oversimplification": "Causal Oversimplification",
    "Obfuscation, intentional vagueness": "Obfuscation, intentional vagueness",
    "Appeal to authority": "Appeal to Authority",
    "Black & white fallacy": "Black-and-White Fallacy",
    "Black-and-White Fallacy": "Black-and-White Fallacy",
    "Thought-terminating clichés": "Thought-terminating Cliches",
    "Thought terminating clichés": "Thought-terminating Cliches",
    "Red herring": "Whataboutism,Straw_Men,Red_Herring",
    "Red Herring": "Whataboutism,Straw_Men,Red_Herring",
    "Straw men": "Whataboutism,Straw_Men,Red_Herring",
    "Straw Men": "Whataboutism,Straw_Men,Red_Herring",
    "Whataboutism": "Whataboutism,Straw_Men,Red_Herring",
    "Whataboutism,Straw_Men,Red_Herring": "Whataboutism,Straw_Men,Red_Herring"
}

line_re = re.compile(r'^\s*\d*\.?\s*(.+?)\s*[-–—]\s*(Yes|No)', re.IGNORECASE)
verdict_re = re.compile(r'Verdict\s*[-–—]\s*(\d+)%', re.IGNORECASE)
#Labels und Verdict auswerten
with open(output_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(["article_id"] + standard_labels + ["Verdict_percent"])
    for file in sorted(output_folder.glob("*_response.txt")):
        article_id = file.stem.replace("_response", "").replace("article", "")
        if "." in article_id:
            article_id = article_id.split(".")[0]
        found = {label: 0 for label in standard_labels}
        verdict_percent = ""
        with open(file, "r", encoding="utf-8") as infile:
            for line in infile:
                m = line_re.match(line.strip())
                if m:
                    raw_name = m.group(1).strip()
                    answer = m.group(2).strip().lower()
                    mapped = technique_map.get(raw_name)
                    if mapped in found and answer == "yes":
                        found[mapped] = 1
                elif "Verdict" in line:
                    vm = verdict_re.search(line)
                    if vm:
                        verdict_percent = vm.group(1)
        row = [article_id] + [found[label] for label in standard_labels] + [verdict_percent]
        writer.writerow(row)

