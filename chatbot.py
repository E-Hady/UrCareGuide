import pandas as pd

data = pd.read_csv('unique_symptoms.csv')

def select_rows(data, base_list):
    mask = data.apply(lambda x: all(symptom in x.values.astype(str) for symptom in base_list), axis=1)
    selected_rows = data[mask]
    return selected_rows

base_list = []
check_list = []
asked_list = []
features = {}

# Welcome message
print("Welcome to the Chatbot. Please enter 'yes' or 'no' for the following questions.")
print("Enter 'Exit' to end the chat.")

while True:
    selected_rows = select_rows(data, base_list)
    symptom_counts = selected_rows.iloc[:, 1:].stack().value_counts()
    
    check_list = [symptom for symptom in symptom_counts.index if symptom not in asked_list and symptom not in base_list]
    
    symptom_found = False
    for symptom in check_list:
        if symptom in base_list:
            continue
        answer = input(f"Do you have {symptom}? (yes/no) ")
        asked_list.append(symptom)
        if answer.lower() == 'yes':
            base_list.append(symptom)
            symptom_found = True
            features[symptom] = 1
            # Update check_list with remaining symptoms not in asked_list and base_list
            check_list = [symptom for symptom in check_list if symptom not in base_list]
            break
        elif answer.lower() == 'exit':
            break
        else:
            features[symptom] = 0
    
    if answer.lower() == 'exit':
        print("Exiting the chatbot.")
        break
    
    data = select_rows(selected_rows, base_list)
    if len(data) == 1:
        break

