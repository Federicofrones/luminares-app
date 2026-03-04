import os
import sys
import time
import subprocess
import requests
from openai import OpenAI
import re

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TTS_API_URL = "http://localhost:3000/api/generate-tts"
TTS_SERVER_COMMAND = "node \"d:\\Luminares app\\long-tts-app\\server.js\""

ESTRUCTURA = [
    {
        "titulo": "Parte 1: El Origen y la Sombra",
        "instruccion": (
            "Introduce el contexto geográfico e histórico de manera poética pero sombría. "
            "Describe la vida cotidiana de la ciudad antes del horror. Introduce la vida temprana del asesino, "
            "su deterioro psicológico, su resentimiento social y cómo se formó la oscuridad en su mente. "
            "Termina justo un momento antes de que cometa su primer crimen."
        )
    },
    {
        "titulo": "Parte 2: El Primer Golpe",
        "instruccion": (
            "Describe el primer crimen con extremo detalle psicológico. Detalla la falsa confianza, el engaño, "
            "la captura y el horror silencioso y asfixiante. Describe cómo actúa y luego cómo la víctima "
            "desaparece, dejando a las autoridades ciegas y a la comunidad confundida al principio."
        )
    },
    {
        "titulo": "Parte 3: La Escalada y el Terror",
        "instruccion": (
            "Describe la furiosa y fría escalada del asesino. El método se vuelve depurado y asombroso por su crudeza. "
            "Múltiples víctimas. Detalla la paranoia que se apodera de la comunidad: calles vacías, puertas con candados y el miedo palpable. "
            "Detalla la investigación policial que resulta inútil frente a este monstruo invisible."
        )
    },
    {
        "titulo": "Parte 4: El Clímax de Audacia",
        "instruccion": (
            "Es el pico de su carrera letal. El asesino se siente un Dios intocable. Narra un gran ataque "
            "masivo o extremadamente audaz. Deja en claro el orgullo y narcisismo sádico del criminal. "
            "Narra la frustración enorme que esto genera en las autoridades exhaustas de estados o regiones enteras."
        )
    },
    {
        "titulo": "Parte 5: La Falla y la Captura",
        "instruccion": (
            "El muro inexpugnable se fisura. El asesino comete un error clave, o una víctima logra escapar, "
            "o una patrulla rutinaria lo sorprende. Detalla la desesperación y el patetismo del asesino en fuga, "
            "perdiendo todo el control hasta que es arrestado; reducido a un hombre ordinario, asustado y engrillado."
        )
    },
    {
        "titulo": "Parte 6: El Juicio y la Condena",
        "instruccion": (
            "El tribunal. Describe el juicio como un circo pero solemne a la vez. El asesino muestra arrogancia "
            "y falsa intelectualidad frente a los familiares deudos. Describe el momento demoledor en que las pruebas "
            "irrefutables son mostradas. El jurado falla en su contra y un juez con voz aplastante dicta la condena terminal irrevocable."
        )
    },
    {
        "titulo": "Parte 7: El Legado Vacío",
        "instruccion": (
            "La vida encerrado en prisión o la ejecución final. Detalla cómo el sistema lo silencia y los años "
            "borran su mentirosa grandeza hasta volverse un olvido carcelario. Haz una larga y solemne "
            "reflexión para cerrar la historia, exaltando la memoria inquebrantable de las víctimas y no del asesino. "
            "Termina con una afirmación filosófica fuerte e imborrable."
        )
    }
]

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name).replace(" ", "_")

def generate_part(caso, parte_info, client):
    system_prompt = (
        "Eres un guionista especializado en relatos de atmósfera oscura, seria y cinematográfica "
        "para canales de True Crime. Escribes para un motor Text-to-Speech (TTS), por lo que "
        "DEBES EVITAR símbolos extraños, asteriscos, exclamaciones o guiones. Solo usa comas y puntos. "
        "Utiliza el PUNTO Y COMA (;) de manera super constante para forzar pausas dramáticas y pesadas en la voz del TTS. "
        "Tu tarea: Generar UNA SOLA PARTE de un relato de 7 actos."
    )
    
    prompt = (
        f"ESTAMOS ESCRIBIENDO UN CUENTO EXTREMADAMENTE LARGO SOBRE EL CASO DE: {caso}.\n"
        f"Tu tarea es escribir ÚNICAMENTE el ACTO ACTUAL, que corresponde a: {parte_info['titulo']}.\n"
        f"INSTRUCCIONES DE NARRATIVA PARA ESTA PARTE: {parte_info['instruccion']}\n\n"
        "REGLAS OBLIGATORIAS:\n"
        "1. Hazlo larguísimo, inmensamente detallado.\n"
        "2. Usa muchos adjetivos lúgubres.\n"
        "3. Evita diálogos directos.\n"
        "4. Al escribir evita usar formatos de markdown como cursivas (* o _), solo PURO TEXTO para leerse en alto.\n"
        "¡ESCRIBE LA PARTE AHORA!"
    )
    
    print(f"  -> Generando {parte_info['titulo']}...")
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.75,
            max_tokens=2500
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"  [ERROR] Falló la generación de OpenAI: {e}")
        return ""

def check_tts():
    try:
        r = requests.get("http://localhost:3000", timeout=2)
        return True
    except:
        return False

def main():
    print("==========================================================")
    print(" GENERADOR DEFINITIVO DE AUDIOCUENTOS MASIVOS TRUE CRIME")
    print("==========================================================")
    print("Presiona Ctrl+C en cualquier momento para cancelar.\n")
    
    try:
        caso = input("=> INGRESA EL NOMBRE DEL CASO O ASESINO (Ej: John Wayne Gacy): ")
    except KeyboardInterrupt:
        print("\nCancelado por el usuario.")
        sys.exit(0)
        
    if not caso.strip():
        print("El caso no puede estar vacío.")
        sys.exit(1)
        
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    # 1. GENERAR TEXTO POR PARTES
    print(f"\n[PASO 1] Iniciando proceso de escritura estructurada (7 Partes) para: {caso}")
    historia_completa = ""
    
    for parte in ESTRUCTURA:
        texto_parte = generate_part(caso, parte, client)
        if texto_parte:
            historia_completa += f"\n\n{texto_parte}\n\n"
            time.sleep(2)
        else:
            print("Abortando debido a un error de OpenAI.")
            sys.exit(1)
            
    # Guardar respaldo
    nombre_archivo_base = sanitize_filename(caso)
    archivo_txt = f"d:\\Luminares app\\{nombre_archivo_base}.txt"
    with open(archivo_txt, "w", encoding="utf-8") as f:
        f.write(historia_completa)
    print(f"\n>> Historia GIGANTE generada y guardada como texto en: {archivo_txt}")
    
    # 2. TTS
    print(f"\n[PASO 2] Comenzando generación de audio TTS...")
    tts_process = None
    if not check_tts():
        print(" -> El servidor TTS no interactúa. Intentando levantarlo localmente...")
        try:
            tts_process = subprocess.Popen(
                TTS_SERVER_COMMAND,
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            time.sleep(8)
            if not check_tts():
                print(" [ERROR] No se pudo levantar el servidor TTS. Inícialo node server.js manualmente.")
                sys.exit(1)
        except Exception as e:
            print(f" [ERROR] Excepción al lanzar servidor: {e}")
            sys.exit(1)
    else:
        print(" -> Servidor TTS detectado funcionando y listo.")

    # 3. ENVIAR A TTS
    print(f" -> Grabando audio... Enviando más de {len(historia_completa)} caracteres al TTS.")
    print(" -> ESTE PROCESO TARDARÁ VARIOS MINUTOS (Por favor, no cierres la ventana)...")
    archivo_mp3 = f"d:\\Luminares app\\{nombre_archivo_base}.mp3"
    
    try:
        response = requests.post(TTS_API_URL, json={"text": historia_completa}, timeout=600)
        
        if response.status_code == 200:
            with open(archivo_mp3, "wb") as f:
                f.write(response.content)
            print("----------------------------------------------------------")
            print(f"\n[ÉXITO TOTAL] ¡Audiocuento MP3 de '{caso}' creado exitosamente!")
            print(f"Audio disponible en: {archivo_mp3}")
        else:
            print(f"\n[ERROR] Servidor devolvió error HTTP {response.status_code}")
            print(response.text)
    except requests.exceptions.Timeout:
        print("\n[ERROR] Timeout esperando al TTS. El audio es inmenso y tomará más tiempo procesarse, revisa la consola del TTS.")
    except Exception as e:
        print(f"\n[ERROR] Error inesperado en el TTS: {e}")
        
    finally:
        if tts_process:
            tts_process.terminate()

if __name__ == "__main__":
    main()
