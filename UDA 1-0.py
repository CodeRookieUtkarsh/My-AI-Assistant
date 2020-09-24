import wikipedia as wiki
import pyttsx3
from nltk.corpus import wordnet as wn
import wolframalpha as wolf

# Defining a function to say things
def speak(text: str):
	# Setting the properties of the voice that is being heard
	engine = pyttsx3.init()
	engine.setProperty('rate', 120)
	engine.setProperty('volume', 0.9)
	engine.say(text)    # Say whatever you want
	engine.runAndWait()    # Wait for the previously lined up speech command to be completed and then all other commands will be executed

# Defining a function to display the dictionary of a word
def dictionary(word):
	find_sec_word = wn.synsets(word)
	def_sec_word = f'Definition of {word} is: {find_sec_word[1].definition()}'
	syn_sec_word = []
	ant_sec_word = []

	for synset in wn.synsets(word):
		for lemma in synset.lemmas():
			syn_sec_word.append(lemma.name())  # add the synonyms
			if lemma.antonyms():  # When antonyms are available, add them into the list
				ant_sec_word.append(lemma.antonyms()[0].name())

	print(def_sec_word)
	print(f'Synonyms of {word} are: \n')
	for syn in syn_sec_word:
		print(syn)
	print(f'Antonyms of {word} are: \n')
	for ant in ant_sec_word:
		print(ant)


# Defining a function to carry out the process of WolframAlpha
def wolf_process(u_input):
	wolf_client = wolf.Client('5J87J9-VA8G974452')

	wolf_res = wolf_client.query(u_input)

	print(next(wolf_res.results).text)
	speak(next(wolf_res.results).text)


# Defining a function to carry out the process of Wikipedia
def wiki_process(u_input):
	wiki_client = wiki
	wiki_res = wiki_client.summary(u_input, sentences=2)

	req_be_specific = f"""{u_input.capitalize()} has many contexts,
Be specific by putting the context in '()' after writing your query"""
	wiki_interruption = "I am sorry to interrupt but you have to be more specific."
	try:
		print(wiki_res)
		speak(wiki_res)
	except wiki.DisambiguationError as e:
		# This exception occurs when multiple contexts are available for the requested query
		print(wiki_interruption)
		speak(wiki_interruption)
		print(req_be_specific)
		speak(req_be_specific)
		print(e.options)
		speak(e.options)


def uda():
	speak('How may I Help you?')
	user_input = input('How may I Help you? ')

	try:
		if 'define'.casefold() in user_input:
			dictionary(user_input[7:])
		else:
			try:
				dictionary(user_input)
			except IndexError:
				if "wikipedia".casefold() in user_input or 'wiki'.casefold() in user_input:
					wiki_process(user_input)
				else:
					wolf_process(user_input)
			except:
				wiki_process(user_input)
	except:
		print('I am still under development, so I could not process your request at this time. Please forgive me')
		speak('I am still under development, so I could not process your request at this time. Please forgive me')
		print("""We are terribly sorry that your problem could not be solved
Regards,
CodkieUtkarsh""")
		speak("""We are terribly sorry that your problem could not be solved
Regards,
CodkieUtkarsh""")


if __name__ == "__main__":
	print("\t\t\t\t\t\t\t\t\t\t\t**Welcome to UDA (Utkarsh's Digital Assistant)**")
	speak("**Welcome to UDA (Utkarsh's Digital Assistant)**")

	speak(
		"I can only search things in wikipedia, wolfram alpha, and define certain words only when I am specifically told to do so. I do not have speech recognition because I am still under development.")

	uda()

	restart = str(input("Is there something else I can help you with [y/n]? ")).lower()
	speak("Is there something else I can help you with [yes/no]? ")

	if restart.startswith('y') or 'y' in restart:
		uda()
	elif restart.startswith('n') or 'n' in restart:
		print("Thank you for using Utkarsh's Digital Assistant\nRegards,\nCodKieUtkarsh")
		speak("Thank you for using Utkarsh's Digital Assistant\nRegards,\nCodKieUtkarsh")
	else:
		print("I will take that as a no")
		speak("I will take that as a no")

		print("Thank you for using Utkarsh's Digital Assistant\nRegards,\nCodKieUtkarsh")
		speak("Thank you for using Utkarsh's Digital Assistant\nRegards,\nCodKieUtkarsh")
