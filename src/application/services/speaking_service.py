import pyttsx3

class SpeakingService:
    def __init__(self):
        self.engine = pyttsx3.init()
    
    def _start_config(self):
        # Set properties (optional)
        self.engine.setProperty('rate', 150)    # Speed percent (can go higher or lower)
        self.engine.setProperty('volume', 0.9)  # Volume 0-1

    def text_to_voice(self, text: str):
        self.engine.say(text)
        self.engine.runAndWait()
