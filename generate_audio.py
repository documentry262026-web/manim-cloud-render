import os
import subprocess
import wave
import contextlib
import google.generativeai as genai

# 1. Setup Gemini
genai.configure(api_key=os.environ["GOOGLE_API"])
try:
    model = genai.GenerativeModel('gemini-3.6-flash')
except:
    model = genai.GenerativeModel('gemini-1.5-flash')

# 2. 5-Minute Documentary Prompt (Hindi + Devanagari English)
prompt = """
Write a 5-minute YouTube documentary script about 'The Mystery of the Pyramids'. 
Structure it clearly:
1. Heavy Hook (Grab attention immediately)
2. Chapter 1: The Impossible Scale (Tons of blocks)
3. Chapter 2: The Orion Alignment (Stars and aliens theory)
4. Chapter 3: The Secret Chambers (Internal layout)
5. Conclusion & Call to Action (Ask them to subscribe and like)

Language Rules: Use simple conversational Hindi. Write common English technical or modern words in Devanagari script (e.g., 'स्ट्रक्चर', 'इंजीनियरिंग', 'एलियंस', 'थ्योरी', 'सब्सक्राइब'). Do NOT use highly difficult pure Hindi words.
Target word count: ~600 to 700 words. 
Output ONLY the spoken text. No brackets, no formatting, no visual instructions.
"""

print("Generating 5-minute script with Gemini...")
try:
    response = model.generate_content(prompt)
    script_text = response.text.replace('\n', ' ')
except Exception as e:
    print(f"Gemini failed: {e}")
    script_text = "पिरामिड का रहस्य। सब्सक्राइब करें।"

with open("script.txt", "w", encoding="utf-8") as f:
    f.write(script_text)

# 3. Generate Audio using Piper TTS
print("Generating audio with Piper TTS...")
piper_cmd = f'echo "{script_text}" | piper -m hi.onnx -f voiceover.wav'
subprocess.run(piper_cmd, shell=True)

# 4. Measure Audio Duration for Manim Sync!
audio_duration = 300.0 # Default 5 mins fallback
if os.path.exists("voiceover.wav"):
    with contextlib.closing(wave.open("voiceover.wav", 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        audio_duration = frames / float(rate)

print(f"Audio generated successfully! Total Duration: {audio_duration} seconds.")

# Save duration for Manim to read
with open("duration.txt", "w") as f:
    f.write(str(audio_duration))
