import os
import json
import wave
import subprocess

SCRIPT_LINES = [
    # [00:00 - 01:00] Intro & Giza Hook
    "क्या आपने कभी सोचा है कि हज़ारों साल पहले, जब आज जैसी मशीनें नहीं थीं, तब इतनी बड़ी-बड़ी पिरामिड्स कैसे बनाई गईं?",
    "मिस्र के पिरामिड्स दुनिया के सबसे रहस्यमयी और शानदार स्ट्रक्चर्स में से एक हैं। ये पिरामिड्स पुराने समय के मिस्र के राजाओं, जिन्हें फ़राओ कहा जाता था, उनकी कब्रों के रूप में बनाए गए थे।",
    "इनमें सबसे मशहूर है ग्रेट पिरामिड ऑफ़ गीज़ा, जिसे लगभग चार हज़ार पाँच सौ साल पहले बनाया गया था।",
    "लेकिन सबसे बड़ा सवाल यही है, इतने भारी पत्थरों को उठाकर, एक के ऊपर एक रखकर, इतनी बड़ी बिल्डिंग आखिर बनाई कैसे गई?",

    # [01:00 - 02:00] Leveling, Quarry, Nile Boat & Wet Sand Sledge
    "सबसे पहले, पिरामिड बनाने के लिए एक सही जगह चुनी जाती थी। ज़मीन को बराबर किया जाता था, ताकि पिरामिड मज़बूत और सीधा बन सके।",
    "इसके बाद हज़ारों बड़े पत्थरों को काटकर तैयार किया जाता था। ये पत्थर आमतौर पर लाइमस्टोन के होते थे।",
    "कुछ पत्थर पास की खदानों से लाए जाते थे, जबकि कुछ को दूर से नावों के ज़रिए पहुँचाया जाता था।",
    "उस समय ट्रक्स या क्रेन्स जैसी मशीनें नहीं थीं। इसलिए पत्थरों को खींचने के लिए स्लेज जैसी लकड़ी की गाड़ियों का इस्तेमाल किया जाता था।",
    "वैज्ञानिकों का मानना है कि रेत को गीला करने से पत्थरों को खींचना आसान हो सकता था।",

    # [02:00 - 03:00] Height Problem & Ramp Theories
    "अब सवाल आता है कि इतने भारी पत्थरों को ऊँचाई तक कैसे पहुँचाया गया?",
    "इसके लिए एक थ्योरी है, रैम्प्स का इस्तेमाल।",
    "रैम्प्स यानी मिट्टी, रेत और पत्थरों से बने ढलान वाले रास्ते।",
    "मज़दूर इन रास्तों पर पत्थरों को धीरे-धीरे ऊपर खींचते थे। फिर उन्हें सही जगह पर सेट किया जाता था।",
    "लेकिन आज भी यह पूरी तरह साफ़ नहीं है कि पिरामिड्स में पत्थरों को ऊपर ले जाने के लिए कौन-सा तरीका इस्तेमाल हुआ था।",
    "हो सकता है कि अलग-अलग हिस्सों में अलग-अलग तरीके अपनाए गए हों।",
    "एक बात ज़रूर है, इस काम के लिए शानदार प्लानिंग, इंजीनियरिंग और टीमवर्क की ज़रूरत थी।",

    # [03:00 - 04:00] Math, Geometry, Base & Workforce vs Slaves Myth
    "पिरामिड बनाना सिर्फ़ पत्थर रखने का काम नहीं था। इसमें मैथ्स और ज्योमेट्री का भी इस्तेमाल होता था।",
    "पिरामिड का बेस बहुत ध्यान से बनाया जाता था, ताकि उसका वज़न सही तरीके से नीचे की ज़मीन पर पड़े।",
    "हर पत्थर को सही जगह पर रखना ज़रूरी था। अगर माप में बड़ी गलती होती, तो पूरी बिल्डिंग कमज़ोर हो सकती थी।",
    "इतने बड़े प्रोजेक्ट को पूरा करने के लिए बहुत सारे वर्कर्स, कारीगरों और सुपरवाइज़र्स की ज़रूरत होती थी।",
    "पहले की कहानियों में अक्सर कहा जाता था कि पिरामिड्स गुलामों ने बनाए थे। लेकिन कई सबूत बताते हैं कि वहाँ बड़ी संख्या में संगठित मज़दूर और कुशल कारीगर काम करते थे।",
    "यह उस समय की इंसानी मेहनत और समझ का एक शानदार उदाहरण है।",

    # [04:00 - 05:00] Conclusion, Science & Final Swarm
    "तो आखिरकार, पिरामिड्स कैसे बने? इसका जवाब है, पत्थरों की कटाई, ट्रांसपोर्टेशन, रैम्प्स जैसे संभावित तरीकों, सही माप और हज़ारों लोगों की मेहनत से।",
    "हालाँकि, पिरामिड्स बनाने की हर डिटेल आज भी पूरी तरह पता नहीं है, लेकिन आर्कियोलॉजी और साइंस हमें इनके बारे में लगातार नई जानकारी देते रहते हैं। सबसे हैरान करने वाली बात यह है कि ये पिरामिड्स हज़ारों साल बाद भी खड़े हैं।",
    "ये हमें बताते हैं कि बिना मॉडर्न टेक्नोलॉजी के भी इंसान कितने बड़े और मुश्किल काम कर सकता था। पिरामिड्स सिर्फ़ पत्थरों से बनी इमारतें नहीं हैं। ये इंसानी दिमाग, मेहनत और इंजीनियरिंग की ताकत का एक शानदार उदाहरण हैं। और शायद यही वजह है कि आज भी दुनिया भर के लोग इन्हें देखकर हैरान रह जाते हैं।"
]

with open("script.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(SCRIPT_LINES))

durations = []
segment_files = []
PAUSE_SEC = 0.45

print("Generating sentence-by-sentence audio with Piper TTS...")

for i, line in enumerate(SCRIPT_LINES):
    seg_file = f"seg_{i}.wav"
    cmd = ["piper", "-m", "hi.onnx", "--length_scale", "1.12", "-f", seg_file]
    subprocess.run(cmd, input=line.encode("utf-8"), check=True)
    segment_files.append(seg_file)

with wave.open(segment_files[0], "rb") as first_wav:
    params = first_wav.getparams()
    framerate = first_wav.getframerate()
    sampwidth = first_wav.getsampwidth()
    nchannels = first_wav.getnchannels()

# Calculate whole frames FIRST so byte length is always a multiple of (sampwidth * nchannels)
pause_frames = int(framerate * PAUSE_SEC)
frame_size = sampwidth * nchannels
silence_frames = b"\x00" * (pause_frames * frame_size)

with wave.open("raw_voiceover.wav", "wb") as out_wav:
    out_wav.setparams(params)
    for seg_file in segment_files:
        with wave.open(seg_file, "rb") as in_wav:
            nframes = in_wav.getnframes()
            data = in_wav.readframes(nframes)
            # Ensure data is strictly aligned to frame_size
            valid_len = (len(data) // frame_size) * frame_size
            out_wav.writeframes(data[:valid_len])
            out_wav.writeframes(silence_frames)

            seg_duration = (nframes / float(framerate)) + (pause_frames / float(framerate))
            durations.append(round(seg_duration, 3))
        os.remove(seg_file)

# Convert to standard 44.1kHz 16-bit stereo PCM for Manim's pydub mixer
subprocess.run([
    "ffmpeg", "-y", "-i", "raw_voiceover.wav",
    "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le", "voiceover.wav"
], check=True)

with open("durations.json", "w") as f:
    json.dump(durations, f)

print(f"Success! Generated {len(durations)} synced segments. Total duration: {sum(durations):.2f}s")
