import pandas
from pandas.io import json

csv_dataframe = pandas.read_csv(open("data.csv"))
diseases = [(name, i) for i, name in enumerate(csv_dataframe['disease'])]

data = []

for disease, i in diseases:
    symptoms = []
    for symptom in csv_dataframe.keys()[1:]:
        if (csv_dataframe[symptom][i] == 1):
            symptoms.append(symptom)

    data.append({
        "name": disease,
        "description": "",
        "treatment": "",
        "symptoms": ", ".join(symptoms),
        "id": i + 1
    })

with open("dump.json", "w") as file:
    file.write((json.dumps(data, indent=2)))