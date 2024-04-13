import requests
from playsound import playsound

def clone_voice_jared(text, path, mp3_file, counter):
    """
    Says text in the custom voice of Jared
    Uses Eleven Labs API
    
    Args:
        test: text for Jared to say
        path: location to save the mp3 file output from API call
        mp3_file: partial name of mp3 file
        counter: counter used for partial naming of mp3 file
    """
    
    url = "https://api.elevenlabs.io/v1/text-to-speech/clone_ID_here"
    
    querystring = {"output_format":"mp3_22050_32"}
    
    payload = {
        "text": text,
        "voice_settings": {
            "similarity_boost": 1,
            "stability": 1
            }
        }
    
    headers = {
        "xi-api-key": "api-key-here",
        "Content-Type": "application/json"
        }
    
    response = requests.request("POST", url, json=payload, headers=headers, params=querystring)
    
    with open(path + mp3_file + counter + ".mp3", "wb") as f:
        f.write(response.content)
        
        playsound(path + mp3_file + counter + ".mp3")
        
    
    
if __name__ == "__main__":
    text = "Hi Susan! It's your best friend Jared!"
    path = "/home/aipi/Desktop/leaflink/sounds/"
    mp3_file = "output"
    counter = str(1)
    clone_voice_jared(text, path, mp3_file, counter)
