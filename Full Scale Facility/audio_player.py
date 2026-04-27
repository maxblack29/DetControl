import pyttsx3

def vacuum_audio_indicator():
    engine = pyttsx3.init()
    rate = engine.setProperty('rate', 150)

    engine.say("Vacuum pressure of 0.5 Pascals reached")
    engine.runAndWait()


'Main function used for testing audip player. Click run while in this file to test.'
def main(): 
    engine = pyttsx3.init()
    rate = engine.setProperty('rate', 150)

    engine.say("Vacuum pressure of 0.5 Pascals reached")
    engine.runAndWait()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")