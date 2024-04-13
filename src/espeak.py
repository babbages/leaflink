import os

def text_to_speech(text, voice="en", speed=120):
    os.system(f"espeak -v{voice} -s{speed} '{text}'")

if __name__ == "__main__":
    text_to_speech("I hurt. You are killing me. I need water.", voice="en-us", speed=150)

    print("Customized text-to-speech conversion completed.")
