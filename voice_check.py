import pyttsx3
import speech_recognition as sr

def speak(text: str):
	engine = pyttsx3.init('sapi5')
	engine.setProperty('rate', 160)
	engine.setProperty('volume', 0.9)

	voice = engine.getProperty('voices')
	engine.setProperty('voices', voice[1].id)

	engine.say(text)
	engine.runAndWait()


def speech_recognition():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print("Listening...")
		r.pause_threshold = 1
		audio = r.listen(source)

		try:
			print("Recognizing...")
			query = r.recognize_google(audio, language="en-IN")
			print(query)
		except Exception as e:
			print(e)
			speak("I did not get that.")

			return "None"

	return query

speak('Start!')
command = speech_recognition()
speak('Stop!')