import csv
import os

# Definir la ruta del CSV existente
CSV_PATH = r"d:\Luminares app\metadata_adobe_stock.csv"

# Datos para las 2 imágenes generadas antes de llegar a la restricción
seo_data = [
    {
        "filename": "reptile_eye_macro_1.png",
        "title": "Extreme macro photography of a mystical reptilian eye with iridescent green and gold scales",
        "keywords": "reptile eye, macro photography, animal texture, biological texture, iridescent scales, green scales, gold scales, dragon eye, vertical pupil, mystical, fantasy, nature, wildlife, extreme details, cinematic, dark background, animal portrait, eye close up, snake eye, lizard eye, predator, wild, exotic, scaly skin, textured background, science, zoology, biology, premium, photorealistic"
    },
    {
        "filename": "reptile_eye_macro_2.png",
        "title": "Ultra close-up macro of a terrifying bioluminescent dragon eye with crimson glowing scales",
        "keywords": "dragon eye, macro texture, bioluminescent, glowing scales, red scales, neon purple, monster eye, fantasy texture, scary, cinematic, dark mood, extreme close-up, sharp focus, reptilian, beast, mythological, creature, sci-fi, horror, aggressive, fierce, alien texture, scaly skin, eye iris, glowing eye, detailed texture, visual effects, cg texture, premium, scary animal"
    }
]

def append_to_csv():
    # Escribiremos 'a' (append) para no borrar los 15 autos anteriores
    with open(CSV_PATH, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        for item in seo_data:
            # 22 = "Animals/Wildlife" (categoría de Adobe Stock) o "Graphic Resources"
            writer.writerow([item["filename"], item["title"], item["keywords"], "22", ""])
            
    print(f"Se agregaron los 2 metadatos macro al archivo {CSV_PATH}.")

if __name__ == "__main__":
    append_to_csv()
