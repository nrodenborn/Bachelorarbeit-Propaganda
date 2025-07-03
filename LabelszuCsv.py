import csv
from pathlib import Path
from collections import defaultdict

label_folder = Path(r"\all-labels-task-flc-tc")
output_file = r"\Labels-binär-geordnet.csv"
#Label-Mapping
label_mapping = {
    "Loaded_Language": "Loaded Language",
    "Name_Calling,Labeling": "Name Calling / Labeling",
    "Repetition": "Repetition",
    "Exaggeration,Minimisation": "Exaggeration / Minimization",
    "Doubt": "Doubt",
    "Appeal_to_fear-prejudice": "Appeal to fear-prejudice",
    "Flag-Waving": "Flag-Waving",
    "Causal_Oversimplification": "Causal Oversimplification",
    "Slogans": "Slogans",
    "Appeal_to_Authority": "Appeal to Authority",
    "Black-and-White_Fallacy": "Black-and-White Fallacy",
    "Thought-terminating_Cliches": "Thought-terminating Cliches",
    "Whataboutism,Straw_Men,Red_Herring": "Whataboutism,Straw_Men,Red_Herring",
    "Bandwagon,Reductio_ad_hitlerum": "Bandwagon,Reductio ad Hitlerum",


}

standard_labels = sorted(set(label_mapping.values()))
#CSV-Erzeugen
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(["article_id"] + standard_labels)
    for file in sorted(label_folder.glob("*.labels")):
        # ID bereinigen (Suffix ab erstem Punkt entfernen, Präfix "article" entfernen)
        article_id = file.stem
        if "." in article_id:
            article_id = article_id.split(".")[0]
        article_id = article_id.replace("article", "")
        found_labels = set()
        with open(file, "r", encoding="utf-8") as infile:
            for line in infile:
                parts = line.strip().split()
                if len(parts) == 4:
                    raw_label = parts[1]
                    clean_label = label_mapping.get(raw_label)
                    if clean_label:
                        found_labels.add(clean_label)
        # Egal ob found_labels leer ist, es gibt immer eine Zeile!
        row = [article_id] + [1 if label in found_labels else 0 for label in standard_labels]
        writer.writerow(row)

print(f"✅ Binäre Matrix für alle Artikel (auch ohne Labels = nur Nullen) gespeichert unter: {output_file}")
