import pandas as pd
import numpy as np
from sklearn.metrics import classification_report

# df-pred anpassen je nach Vergleichsdatei
df_gt = pd.read_csv("\Labels-binär-geordnet.csv", delimiter=";")
df_pred = pd.read_csv("\OpenAi-binaer.csv", delimiter=";")

# Setze Index auf article_id
df_gt = df_gt.set_index("article_id")
df_pred = df_pred.set_index("article_id")

# Gleiche Reihenfolge der Zeilen/IDs sicherstellen
df_pred = df_pred.loc[df_gt.index]

# Gleiche Labelspalten
label_columns = [col for col in df_gt.columns if col in df_pred.columns]

# Extrahiere binäre Matrizen
y_true = df_gt[label_columns].values
y_pred = df_pred[label_columns].values

# Multi-label (pro Label) Auswertung
report = classification_report(y_true, y_pred, target_names=label_columns, zero_division=0, output_dict=True)
print(pd.DataFrame(report).T)
results = {}
for idx, label in enumerate(label_columns):
    TP = np.sum((y_true[:, idx] == 1) & (y_pred[:, idx] == 1))
    FP = np.sum((y_true[:, idx] == 0) & (y_pred[:, idx] == 1))
    FN = np.sum((y_true[:, idx] == 1) & (y_pred[:, idx] == 0))
    TN = np.sum((y_true[:, idx] == 0) & (y_pred[:, idx] == 0))
    results[label] = {"TP": TP, "FP": FP, "FN": FN, "TN": TN}


print("Macro F1:", report["macro avg"]["f1-score"])
print("Micro F1:", report["micro avg"]["f1-score"])
df_results = pd.DataFrame(results).T
print(df_results)