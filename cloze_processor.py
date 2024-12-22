import csv
from csv import DictReader, DictWriter
from collections import defaultdict

# Load cloze key
clozekey_reader = csv.reader(open(r'path/cloze_key.csv', 'r', encoding='utf-8-sig'))
clozekey = dict(clozekey_reader)
print("Cloze Key Loaded:", clozekey)

# Load raw cloze task data
with open("path/cloze_100participants", 'r', encoding='utf-8-sig') as f:
    cloze_reader = DictReader(f)
    list_of_cloze = list(cloze_reader)

print("First Response Loaded:", list_of_cloze[0])

# Check accuracy
for dic in list_of_cloze:
    for item in clozekey:
        if dic['Event Index'] == item:
            if dic['Response'] in clozekey[item]:
                dic.update({'Accuracy': 1})
            else:
                dic.update({'Accuracy': 0})

print("First Three Processed Responses:", list_of_cloze[0:3])

# Export the list to a new CSV file with accuracy
headrow = list(list_of_cloze[0].keys())
with open('path/new_cloze_100participants.csv', 'w', newline='', encoding='utf-8-sig') as output_file:
    dictwriter = DictWriter(output_file, fieldnames=headrow)
    dictwriter.writeheader()
    dictwriter.writerows(list_of_cloze)

print("Accuracy Added and Exported to new_cloze_116.csv")

# Summarize accuracy for each participant
participant_accuracy = defaultdict(lambda: {'Total': 0, 'Correct': 0})

for dic in list_of_cloze:
    participant_id = dic['Participant ID']
    participant_accuracy[participant_id]['Total'] += 1
    participant_accuracy[participant_id]['Correct'] += dic['Accuracy']

# Prepare summary for export
summary_data = []
for participant, stats in participant_accuracy.items():
    accuracy_rate = stats['Correct'] / stats['Total']
    summary_data.append({'Participant ID': participant, 'Total Responses': stats['Total'], 'Correct Responses': stats['Correct'], 'Accuracy Rate': accuracy_rate})

# Export participant accuracy summary
summary_file_path = 'path/participant_accuracy_summary.csv'
with open(summary_file_path, 'w', newline='', encoding='utf-8-sig') as summary_file:
    fieldnames = ['Participant ID', 'Total Responses', 'Correct Responses', 'Accuracy Rate']
    summary_writer = DictWriter(summary_file, fieldnames=fieldnames)
    summary_writer.writeheader()
    summary_writer.writerows(summary_data)

print("Participant Accuracy Summary Exported to participant_accuracy_summary.csv")
