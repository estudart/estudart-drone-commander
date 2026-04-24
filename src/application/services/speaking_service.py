import pyttsx3

class SpeakingService:
    """Small wrapper around text-to-speech (pyttsx3)."""

    def __init__(self) -> None:
        self.engine = pyttsx3.init()
        self._start_config()
    
    def _start_config(self) -> None:
        # Tune defaults once at startup.
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)

    def text_to_voice(self, text: str) -> None:
        self.engine.say(text)
        self.engine.runAndWait()
