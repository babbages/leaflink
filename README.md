# Leaflink
Interact with an AI aliasing as a plant (false indigo). This project is a proof of concept to show how a plant can sustain itself using AI, as well as interact with users.

The tool is programmed to pump water when the moisture level is low, turn on LED lights in low light, and fertilize the plant at regular intervals.

The AI is programmed to interact with the user, allowing the user to speak directly with the plant. The AI is programmed to assist with EDA, model building, RAG pdf search (false indigo specific files), and web search. The AI makes use of Google's Text to Speech and Eleven Lab's voice cloning ability.

## Hardware
Built using a Raspberry Pi 4b, with an ADS1115 analog to digital converter for the moisture sensor.

### Input Sensors
- Moisture (Analog)
- Temperature and Humidity
- Light (Digital)
- Microphone (With Sound Card)
- Button 

### Outputs
- Water Pump
- Fertiliziling Box Using Servo Motor
- LED Lights
- Speaker (AV Jack)

## Software
### Overview
- Micropython libraries for controlling sensors and motors with Pi, and writing sensor details to a csv
- Langchain agents
- GPT-4
- Google speech to text
- ElevenLabs.ai voice cloning, text to speech

### AI Details
The AI was built with multiple levels. 

1. Using Google Text to Speech, user input to the microphone is transcribed into text. This text is then sent to AI #2 by way of an API call (hosted on HuggingFace).
2. On HuggingFace, there is a master AI instructed to control subordinate langchain AI agents. The master AI classifies the user input to decide which langchain agent to send directions to. Then various langchain agents are capable of:
    - Controling the output motors
    - EDA of the csv sensor data file
    - Building models using the csv sensor data file
    - RAG operation to search false indigo specific pdf files
    - Web search if the other operations do not appear appropriate
3. Once the langchain agent of choice returns a chain of thought response, the master AI then converts the response and any motor instructions to a json format for delivery.
4. The response is translated, passed to the motors, converted to audio using a voice clone, and played back to the user through the speaker.