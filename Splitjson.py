import json
import re
import sys

# Læs data fra filen output.json
with open('output.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Funktion til at opdele spørgsmål korrekt
def split_questions(text):
    # Erstat \n med mellemrum for at sikre korrekt opdeling
    text = text.replace("\n", " ")
    # Del spørgsmålene ved spørgsmålstegnet og sikre, at hvert spørgsmål slutter med ?
    questions = [q.strip() for q in re.split(r'(?<=\?)\s+', text) if 'bullshit?' in q]
    return questions

# Funktion til at opdele svar korrekt
def split_answers(text):
    # Erstat \n med mellemrum for at sikre korrekt opdeling
    text = text.replace("\n", " ")
    
    # Del svarene baseret på dobbelt linjeskift (\n\n) eller gennemgående mønstre
    answers = re.split(r'\s{2,}', text)
    
    # Opdel svarene yderligere, hvis der er flere "Sandt" eller "Bullshit" i samme svar
    split_answers = []
    for answer in answers:
        # Find alle svar, der starter med "Sandt" eller "Bullshit"
        parts = re.split(r'(?=Bullshit|Sandt)', answer)
        # Fjern tomme strenge og sikre, at svarene indeholder relevante informationer
        for part in parts:
            part = part.strip()
            if part and ("Bullshit" in part or "Sandt" in part):
                split_answers.append(part)
    
    return split_answers

# Behandl hver post i dataen
output_data = []
card_counter = 1  # Start kortnummerering fra 1

for entry in data:
    questions = split_questions(entry['Spørgsmål'])
    answers = split_answers(entry['Svar'])
    print("Questions:", questions)
    print("Answers:", answers)

    # Hvis spørgsmål og svar ikke matcher, log en advarsel, men fortsæt behandlingen
    if len(questions) != len(answers):
        print(f"Warn: Mismatch mellem spørgsmål og svar for card_id {entry['card_id']}")
        print(f"Spørgsmål: {len(questions)}")
        print(f"Svar: {len(answers)}")
        # Hvis der er et mismatch, stop og afslut programmet
        exit()

    # For hvert spørgsmål og svar, tilføj som card_id.x
    for idx, (question, answer) in enumerate(zip(questions, answers), 1):
        card_output = {
            "card_id": f"{card_counter}.{idx}",
            "questions": question,
            "answers": answer
        }

        # Tilføj kortet til output_data
        output_data.append(card_output)

    # Øg card_counter for næste kort
    card_counter += 1

# Skriv det opdelte resultat til en ny JSON-fil
with open('q_And_A.json', 'w', encoding='utf-8') as outfile:
    json.dump(output_data, outfile, ensure_ascii=False, indent=4)

# Udskriv resultatet
print(json.dumps(output_data, ensure_ascii=False, indent=4))
