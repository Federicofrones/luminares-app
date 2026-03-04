import sys
import os
import requests
import argparse

TTS_API_URL = "http://localhost:3000/api/generate-tts"

def main():
    parser = argparse.ArgumentParser(description="Convierte txt a mp3 usando TTS local")
    parser.add_argument("input_file", help="Rútalo")
    parser.add_argument("output_file", help="Rútalo")
    
    args = parser.parse_args()
    
    input_file = args.input_file
    output_file = args.output_file

    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read().strip()
        
    print(f"Enviando {len(text)} caracteres al TTS... Espera, por favor.")
    
    payload = {"text": text}
    
    try:
        response = requests.post(TTS_API_URL, json=payload, timeout=600)
        
        if response.status_code == 200:
            with open(output_file, "wb") as audio_file:
                audio_file.write(response.content)
            print("¡Éxito! Audio generado.")
        else:
            print(f"Error HTTP: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
