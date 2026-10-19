import os
import subprocess
import google.generativeai as genai

# 1. Setup Gemini 3.6 Flash (Falling back gracefully if version is adjusting)
genai.configure(api_key=os.environ["GOOGLE_API"])
try:
    model = genai.GenerativeModel('gemini-3.6-flash')
except:
    model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Prompt for simple Hindi + English words in Devanagari
prompt = """
Write a 90-second documentary video script about 'The Mystery of the Pyramids'.
Language: Use simple Hindi, but write common English terms in Devanagari (e.g., 'पिरामिड', 'ब्लॉक्स', 'टन', 'इंजीनियरिंग'). 
Do NOT use highly difficult pure Hindi words. Keep it very conversational and mysterious.
Output ONLY the spoken text. No brackets, no formatting, no visual instructions. Just the script.
"""

print("Generating script with Gemini...")
try:
    response = model.generate_content(prompt)
    script_text = response.text.replace('\n', ' ')
except Exception as e:
    print(f"Gemini failed: {e}")
    script_text = "प्राचीन मिस्र के पिरामिड आज भी एक बहुत बड़ा रहस्य हैं। क्या आप जानते हैं कि इन्हें कैसे बनाया गया था? लाखों भारी ब्लॉक्स को बिना किसी मॉडर्न मशीन के रेगिस्तान में ट्रांसपोर्ट किया गया।"

# Save script for Discord
with open("script.txt", "w", encoding="utf-8") as f:
    f.write(script_text)

# 3. Generate Audio using Piper TTS
print("Generating audio with Piper TTS...")
piper_cmd = f'echo "{script_text}" | piper -m hi.onnx -f voiceover.wav'
result = subprocess.run(piper_cmd, shell=True)

if result.returncode != 0 or not os.path.exists("voiceover.wav"):
    print("Piper TTS failed. Fallback: Outputting text script only to Discord.")
else:
    print("Voiceover generated successfully!")
