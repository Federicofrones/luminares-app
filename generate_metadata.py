import csv
import os

# Definir la ruta de las imágenes y del CSV
IMAGENES_DIR = r"d:\Luminares app\IMAGENES MICROSTOCK"
CSV_PATH = r"d:\Luminares app\metadata_adobe_stock.csv"

# Preparamos los datos SEO (Palabras clave y Títulos para "Interiores de Auto Premium")
seo_data = [
    {
        "filename": "sports_car_interior_1.png",
        "title": "Modern ultra-luxury German sports car interior with glossy carbon fiber and red ambient lighting",
        "keywords": "car interior, luxury car, sports car, carbon fiber, leather steering wheel, dashboard, ambient lighting, neon red, premium, modern, german car, automotive, transportation, drive, high-end, exclusive, wealth, fast, vehicle interior, luxury lifestyle, speed, cockpit, digital dashboard, driver seat, expensive, sleek, dark mood, cinematic, auto, passenger"
    },
    {
        "filename": "sports_car_interior_2.png",
        "title": "Futuristic luxury electric vehicle interior with large touchscreen and icy blue ambient light",
        "keywords": "electric vehicle, ev, futuristic car, luxury interior, touchscreen display, dashboard display, vegan leather, blue ambient lighting, minimalist, modern transport, zero emission, technology, smart car, innovation, elegant, clean energy, high tech, premium materials, automotive design, eco-friendly, luxury lifestyle, auto interior, futuristic design, drive, transportation, luxury car, cabin, sleek, premium, expensive"
    },
    {
        "filename": "sports_car_interior_3.png",
        "title": "Macro close-up of luxury car center console with rich dark brown leather and brushed aluminum",
        "keywords": "car console, luxury details, macro photography, brown leather, pristine stitching, brushed aluminum, car interior, premium materials, automotive details, craftsmanship, expensive auto, luxury lifestyle, high-end, dashboard dials, exclusive, sophisticated, design, texture, close up, auto parts, luxury trim, rich texture, dark mood, automotive photography, motor, vehicle details, elegant, luxury vehicle, gear shift, transportation"
    },
    {
        "filename": "sports_car_interior_4.png",
        "title": "Premium ultra-luxury SUV interior at night with starry panoramic sunroof and quilted leather",
        "keywords": "suv interior, luxury suv, starry roof, panoramic sunroof, quilted leather, cream leather, wood grain, ambient purple lighting, night drive, premium cabin, luxury lifestyle, elegant transport, first class, spacious interior, automotive luxury, high-end vehicle, expensive car, luxury lifestyle, dark interior, comfort, passenger experience, auto, wealthy, dashboard, cinematic, night scene, modern, exclusive, car cabin, transportation"
    },
    {
        "filename": "sports_car_interior_5.png",
        "title": "Bright minimalist modern luxury car interior with white leather seats and panoramic glass roof",
        "keywords": "car interior, bright interior, white leather, black piping, minimalist design, panoramic roof, luxury car, modern vehicle, daylight, clean aesthetic, high-end transport, premium cabin, sunny, elegant, sophisticated, automotive, expensive, luxury lifestyle, auto, daylight drive, interior design, comfortable, pristine, flawless, modern auto, bright light, car cabin, luxury seating, transportation, exclusive"
    },
    {
        "filename": "sports_car_interior_6.png",
        "title": "Modernized vintage classic supercar interior with tan leather seats and carbon fiber tub",
        "keywords": "vintage supercar, classic car interior, modernized classic, restomod, tan leather, carbon fiber, analog dials, racing seats, retro modern, automotive history, luxury classic, sports car, exotic car, warm lighting, cinematic, car cabin, retro aesthetic, premium, expensive, collector car, high performance, auto, motor, steering wheel, classic luxury, transportation, vintage style, iconic, driver focus, manual"
    },
    {
        "filename": "sports_car_interior_7.png",
        "title": "Extremely luxurious VIP van passenger cabin with diamond quilted leather and starry roof headliner",
        "keywords": "vip van, luxury van, passenger cabin, quilted leather, captain chairs, starry roof, rolls royce style, luxury transport, executive travel, first class, premium interior, comfortable ride, chauffeur, wealthy lifestyle, high-end van, interior design, elegant, expensive, business travel, luxury lifestyle, custom van, thick carpets, transportation, auto, spacious, opulent, exclusive, passenger, motor, luxury"
    },
    {
        "filename": "sports_car_interior_8.png",
        "title": "High-performance track car stripped interior with carbon fiber monocoque and alcantara steering wheel",
        "keywords": "track car, race car interior, high performance, motorsport, carbon fiber tub, alcantara steering wheel, sequential shifter, roll cage, stripped interior, racing, speed, fast, extreme, functional design, automotive, sports car, supercar, hypercar, aggressive, cockpit, driver focused, circuit racing, motor, auto, expensive, lightweight, performance vehicle, competition, intense, transportation"
    },
    {
        "filename": "sports_car_interior_9.png",
        "title": "Luxury convertible car interior at golden hour sunset with tan leather and rose gold accents",
        "keywords": "convertible car, luxury interior, sunset drive, golden hour, tan leather, rose gold, lifestyle, road trip, summer drive, premium car, warm lighting, romantic, elegant transport, open top, beautiful lighting, cinematic, wealthy lifestyle, high-end vehicle, expensive, vacation, travel, automotive photography, motor, auto, luxury lifestyle, scenic drive, classy, dashboard, relaxing, transportation"
    },
    {
        "filename": "sports_car_interior_10.png",
        "title": "Close-up of high-end car door panel with diamond stitched alcantara and red ambient lighting",
        "keywords": "car door panel, luxury details, stitched alcantara, diamond pattern, interior trim, ambient lighting, red light, brushed steel, premium materials, automotive design, texture, close up, craftsmanship, expensive auto, luxury lifestyle, high-end, exclusive, sophisticated, design, auto parts, luxury trim, dark mood, automotive photography, motor, vehicle details, elegant, luxury vehicle, sport trim, transportation, rich texture"
    },
    {
        "filename": "sports_car_interior_11.png",
        "title": "Aggressive cybernetic supercar interior with bare carbon fiber and neon green ambient lighting",
        "keywords": "supercar interior, cybernetic, futuristic, aggressive design, carbon fiber, titanium, neon green, ambient lighting, racing steering wheel, high tech, dark cinematic, hypercar, extreme performance, sports car, fast, speed, advanced technology, automotive, modern design, sleek, angular, expensive, premium, exclusive, motor, auto, driver focus, cockpit, luxury lifestyle, transportation"
    },
    {
        "filename": "sports_car_interior_12.png",
        "title": "Passenger view of a modern hypercar interior with black alcantara cockpit and red stitching",
        "keywords": "hypercar interior, passenger view, black alcantara, red stitching, driver focused cockpit, center console, tactile buttons, dramatic lighting, premium aesthetic, high end, sports car, exotic car, luxury vehicle, fast, performance, expensive, exclusive, automotive, motor, auto, interior design, cinematic, dark mood, wealthy lifestyle, luxury, transportation, modern auto, sleek design, quality, auto cabin"
    },
    {
        "filename": "sports_car_interior_13.png",
        "title": "Luxury grand tourer car interior with saddle brown leather, deep mahogany wood trims and analog clock",
        "keywords": "grand tourer, luxury car, saddle brown leather, mahogany wood, analog clock, classic elegance, timeless design, warm lighting, premium interior, sophisticated, high class, wealthy, expensive car, luxury lifestyle, automotive, motor, auto, elegant transport, comfortable, relaxed drive, traditional luxury, classy, interior design, dashboard, premium materials, exclusive, passenger, driver, transportation, luxury cabin"
    },
    {
        "filename": "sports_car_interior_14.png",
        "title": "Aggressive supercar interior at night with glowing red digital cluster and exposed carbon fiber",
        "keywords": "supercar interior, night drive, city lights, exposed carbon fiber, glowing red, digital cluster, street racing, aggressive mood, high contrast, cinematic, fast, speed, sports car, hypercar, performance vehicle, dark aesthetic, automotive, motor, auto, cockpit, driver seat, luxury lifestyle, expensive, exclusive, urban drive, neon lights, modern transport, sleek, advanced, transportation"
    },
    {
        "filename": "sports_car_interior_15.png",
        "title": "Minimalist futuristic luxury SUV interior with pure white leather and glowing cyan frosted glass console",
        "keywords": "futuristic suv, luxury interior, white leather, minimalist, frosted glass, cyan lighting, ambient light, high key, clean design, modern aesthetic, premium suv, elegant, sophisticated, bright interior, concept car, advanced technology, luxury lifestyle, expensive vehicle, automotive design, pristine, pure, exclusive, auto, motor, dashboard, car cabin, transportation, high tech, innovative, luxury"
    }
]

# Escribir el archivo CSV
def write_adobe_stock_csv():
    headers = ["Filename", "Title", "Keywords", "Category", "Releases"]
    
    with open(CSV_PATH, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        
        for item in seo_data:
            # Imprimimos la fila según el formato estándar que pide Adobe Stock
            # Categoría 20 es "Transporte" (Transportation)
            writer.writerow([item["filename"], item["title"], item["keywords"], "20", ""])
            
    print(f"✅ Se ha escrito el archivo {CSV_PATH} con los metadatos de las 15 imágenes generadas.")

if __name__ == "__main__":
    write_adobe_stock_csv()
