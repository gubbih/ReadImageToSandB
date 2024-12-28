import os

arr = os.listdir("E:\\Python\\ReadImage\\Rename\\")

# Indstillinger
input_folder = "Rename/"  # Mappe med originale billeder
output_folder = "savedimg/"  # Mappe til omdøbte billeder
os.makedirs(output_folder, exist_ok=True)  # Opret output-mappe, hvis den ikke eksisterer

# Hent og sorter billeder
image_files = sorted(os.listdir(input_folder))  # Sørg for, at billederne er i korrekt rækkefølge
counter = 1

for image in image_files:
    if 'front' in image.lower():  # Tjek om filen indeholder "front"
        new_name = f"card_{counter:02d}_a.png"
        os.rename(os.path.join(input_folder, image), os.path.join(output_folder, new_name))
        counter += 1
    elif 'back' in image.lower():  # Tjek om filen indeholder "back"
        new_name = f"card_{counter:02d}_b.png"
        os.rename(os.path.join(input_folder, image), os.path.join(output_folder, new_name))
        counter += 1

print("Billeder er omdøbt til formatet card_XX_a/b!")
