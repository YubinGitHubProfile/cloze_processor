import csv
from csv import DictReader, DictWriter
from collections import defaultdict

# Load cloze key
clozekey = {}
with open(r'./data/ClozeBrownAnswers_EN.csv', 'r', encoding='utf-8-sig') as f:
    reader = DictReader(f)
    for row in reader:
        # Split the 'key' column by comma and strip whitespace from each answer
        acceptable_answers = [ans.strip() for ans in row['Key'].split(',')]
        clozekey[row['Number']] = acceptable_answers

print("Cloze Key Loaded:", clozekey)

# Load raw cloze task data
with open(r'./data/cloze_20250427.csv', 'r', encoding='utf-8-sig') as f:
    cloze_reader = DictReader(f)
    list_of_cloze = list(cloze_reader)

# Check accuracy
for dic in list_of_cloze:
    # Strip BOM and any whitespace from event_index
    event_index = dic['Event Index'].strip().strip('\ufeff')
    
    # Only process items 2 through 51
    if not (2 <= int(event_index) <= 51):
        dic['Accuracy'] = None
        continue
        
    # Adjust index to match cloze key (subtract 1 to convert from 2-51 to 1-50)
    key_index = str(int(event_index) - 1)
    response = dic['Response'].strip()
    
    if key_index in clozekey:
        if any(response.lower() == answer.lower() for answer in clozekey[key_index]):
            dic['Accuracy'] = 1
        else:
            dic['Accuracy'] = 0
    else:
        print(f"Warning: Key Index {key_index} not found in cloze key")
        dic['Accuracy'] = 0

print("First Three Processed Responses:", list_of_cloze[0:3])

# Export the list to a new CSV file with accuracy
headrow = list(list_of_cloze[0].keys())
with open(r'./data/new_cloze_20250427.csv', 'w', newline='', encoding='utf-8-sig') as output_file:
    dictwriter = DictWriter(output_file, fieldnames=headrow)
    dictwriter.writeheader()
    dictwriter.writerows(list_of_cloze)

print("Accuracy Added and Exported to new_cloze_100participants.csv")

# Summarize accuracy for each participant
participant_accuracy = defaultdict(lambda: {'Total': 0, 'Correct': 0})

for dic in list_of_cloze:
    participant_id = dic['Participant Private ID']
    # Only count items that have a valid accuracy value (not None)
    if dic['Accuracy'] is not None:
        participant_accuracy[participant_id]['Total'] += 1
        participant_accuracy[participant_id]['Correct'] += dic['Accuracy']

# Prepare summary for export
summary_data = []
for participant, stats in participant_accuracy.items():
    accuracy_rate = stats['Correct'] / stats['Total']
    summary_data.append({'Participant ID': participant, 'Total Responses': stats['Total'], 'Correct Responses': stats['Correct'], 'Accuracy Rate': accuracy_rate})

# Export participant accuracy summary
summary_file_path = r'./data/Batch2_accuracy_summary.csv'
with open(summary_file_path, 'w', newline='', encoding='utf-8-sig') as summary_file:
    fieldnames = ['Participant ID', 'Total Responses', 'Correct Responses', 'Accuracy Rate']
    summary_writer = DictWriter(summary_file, fieldnames=fieldnames)
    summary_writer.writeheader()
    summary_writer.writerows(summary_data)

print("Participant Accuracy Summary Exported to 100participants_accuracy_summary.csv")
