import sounddevice as sd
import numpy as np
import time
import requests
from twilio.rest import Client

SAMPLE_RATE = 44100
DURATION = 0.5

BUZZER_FREQ_MIN = 2000
BUZZER_FREQ_MAX = 4500
ENERGY_THRESHOLD = 1.0

buzz_duration = 0
alert_sent = False

TWILIO_ACCOUNT_SID = "ACf632e12a65c09e3204cf3d277449cc22"
TWILIO_AUTH_TOKEN = "0154877b40535a404fb5e668d6405a45"
TWILIO_NUMBER = "+1 405 809 3353" 

MY_PHONE_NUMBER = "+77054918335" 

def send_emergency_call():
    """Айфонға 0 секундта бірден НАҚТЫ ҰЯЛЫ ТЕЛЕФОН ҚОҢЫРАУЫН соғу"""
    print(f"[ҚОҢЫРАУ] Twilio арқылы {MY_PHONE_NUMBER} нөміріне шұғыл қоңырау шалынуда...")
    
    try:
        client = Client("ACf632e12a65c09e3204cf3d277449cc22", "0154877b40535a404fb5e668d6405a45")
        
        call = client.calls.create(
            twiml='<Response><Say language="en-US" voice="alice">Sultan! Emergency! Water leak detected in your smart home. Check it now!</Say></Response>',
            to="+77054918335",
            from_="+1 405 809 3353"
        )
        print(f"[СӘТТІ] Телефоныңыз дәл қазір шырылдайды! Қоңырау ID: {call.sid}")
    except Exception as e:
        print(f"[ҚАТЕ] Нақты қоңырау соғу сәтсіз аяқталды: {e}")


def audio_callback(indata, frames, time_info, status):
    global buzz_duration, alert_sent
    if status:
        print(status)
        
    signal = indata[:, 0]
    fft_data = np.abs(np.fft.rfft(signal))
    frequencies = np.fft.rfftfreq(len(signal), d=1.0/SAMPLE_RATE)
    
    buzzer_mask = (frequencies >= BUZZER_FREQ_MIN) & (frequencies <= BUZZER_FREQ_MAX)
    buzzer_energy = np.mean(fft_data[buzzer_mask]) if np.any(buzzer_mask) else 0

    if buzzer_energy > ENERGY_THRESHOLD:
        buzz_duration += DURATION
        print(f"[ТАБЫЛДЫ] Макет шиқылы естіліп тұр! Таймер: {int(buzz_duration)} сек. (Қуаты: {buzzer_energy:.2f})")
        
        if buzz_duration >= 10.0 and not alert_sent:
            print("\n🚨🚨🚨 ҚАУІП! СУ БАСУ 10 СЕКУНДТАН АСТЫ! 🚨🚨🚨")
            send_emergency_call()
            alert_sent = True
    else:
        if buzz_duration > 0:
            print("[ТОҚТАДЫ] Дыбыс үзілді. Таймер нөлге түсірілді.\n")
        buzz_duration = 0
        alert_sent = False

print("[AI СҮЗГІ] Микрофон іске қосылды. Макет дыбысын бақылау басталды...")
try:
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=audio_callback, blocksize=int(SAMPLE_RATE * DURATION)):
        while True:
            time.sleep(0.1)
except KeyboardInterrupt:
    print("\n[AI СҮЗГІ] Жүйе тоқтатылды.")