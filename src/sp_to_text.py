import speech_recognition as sr

speech = sr.Recognizer()

def voice_to_text():
    """
    Converts audio from microphone into text
    Uses Google's speech recognition platform
    
    Args:
        None
    Return:
        string to text
    """
    
    text = ""
    
    with sr.Microphone() as source:
        speech.adjust_for_ambient_noise(source)
        print("Say something...")
        
        try:
            audio = speech.listen(source, timeout=5)
            text = speech.recognize_google(audio)
            print("You said:", text)
            print("Done listening")
            return text
        except:
            return "Sorry, I could not recognize your voice"
        
if __name__ == "__main__":
    print(voice_to_text())
