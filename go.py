import os
import cv2
import numpy as np
import json
from pytesseract import pytesseract

# Angiv stien til Tesseract
path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Få alle billeder i mappen og sorter dem
arr = os.listdir("E:\\Python\\ReadImage\\img\\")
arr.sort()  # Sørg for at billederne er i den rigtige rækkefølge

# Opbevar kortene
cards = []

# Læs billederne og udtræk spørgsmål og svar
for i in range(0, len(arr), 2):  # Spring 2 billeder ad gangen (1 spørgsmål, 1 svar)
    # Tjek om billederne følger navngivningsmønstret
    question_image_name = arr[i]
    answer_image_name = arr[i + 1] if i + 1 < len(arr) else None

    # Tjek om det er et spørgsmål og svar billedepar
    if '_a' in question_image_name and '_b' in answer_image_name:
        question_image = cv2.imread("E:\\Python\\ReadImage\\img\\" + question_image_name)
        answer_image = cv2.imread("E:\\Python\\ReadImage\\img\\" + answer_image_name) if answer_image_name else None

        if question_image is None:
            print(f"Kunne ikke læse billede: {question_image_name}")
            continue

        # Behandl spørgsmålet (første billede)
        gray_q = cv2.cvtColor(question_image, cv2.COLOR_BGR2GRAY)
        clahe_q = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8, 8)).apply(gray_q)
        blurred_q = cv2.medianBlur(clahe_q, 3)
        ret, thresh_q = cv2.threshold(blurred_q, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        inverted_q = cv2.bitwise_not(thresh_q)
        sharpen_q = cv2.filter2D(inverted_q, -1, np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]))  # Skarphed
        pytesseract.tesseract_cmd = path_to_tesseract
        question_text = pytesseract.image_to_string(sharpen_q, lang='dan', config='--psm 3')

        # Behandl svaret (andet billede)
        if answer_image is not None:
            gray_a = cv2.cvtColor(answer_image, cv2.COLOR_BGR2GRAY)
            clahe_a = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8, 8)).apply(gray_a)
            blurred_a = cv2.medianBlur(clahe_a, 3)
            ret, thresh_a = cv2.threshold(blurred_a, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
            inverted_a = cv2.bitwise_not(thresh_a)
            sharpen_a = cv2.filter2D(inverted_a, -1, np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]))  # Skarphed
            answer_text = pytesseract.image_to_string(sharpen_a, lang='dan', config='--psm 3')
        else:
            answer_text = ""

        # Rens tekst ved at fjerne uønskede tegn
        question_text = question_text.replace("|", "I").strip()
        answer_text = answer_text.replace("|", "I").strip()

        # Gem data i JSON-format
        card_data = {
            "card_id": (i // 2) + 1,  # Kort ID baseret på billedernes rækkefølge
            "Spørgsmål": question_text,
            "Svar": answer_text
        }
        print(card_data)
        cards.append(card_data)

# Gem dataene i en JSON-fil
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(cards, f, ensure_ascii=False, indent=4)

print("Data er gemt i output.json.")
