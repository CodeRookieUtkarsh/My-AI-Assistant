import pyttsx3
import wikipedia as wiki
import wolframalpha as wolf
import requests
import time


def speak(text: str):
	engine = pyttsx3.init()
	engine.setProperty('rate', 120)
	engine.setProperty('volume', 0.9)

	engine.say(text)
	engine.runAndWait()


def wolf_process_1(command: str):
	api_key = '5J87J9-VA8G974452'  # You can create your own API key in wolframalpha.com
	wolf_client = wolf.Client(api_key)

	wolf_res = wolf_client.query(command)

	print(f"The answer is {next(wolf_res.results).text}")
	speak(f"The answer is {next(wolf_res.results).text}")


def wolf_process_2(command: str):
	api_key = '5J87J9-VA8G974452'  # You can create your own API key in wolframalpha.com
	wolf_client = wolf.Client(api_key)

	index = command.lower().split().index('calculate')
	query = command.split()[index + 1:]

	wolf_res = wolf_client.query(' '.join(query))

	print(f"The answer is {next(wolf_res.results).text}")
	speak(f"The answer is {next(wolf_res.results).text}")


def wiki_process(command: str):
	wiki_client = wiki
	wiki_res = wiki_client.summary(command, sentences=4)
	try:
		print(wiki_res)
		speak(wiki_res)
	except wiki.DisambiguationError as e:
		# This exception occurs when multiple contexts are available for the requested query
		speak("I am sorry to interrupt but you have to be more specific.")
		print("I am sorry to interrupt but you have to be more specific.")
		speak(f"""{command.capitalize()} has many contexts,
		Pls also mention the context of your query after telling me about that""")
		print(f"""{command.capitalize()} has many contexts,
Pls also mention the context of your query after telling me about that""")
		speak(e.options)
		print(e.options)


def definition(word: str):
	api_key = 'your api key'  # You can create an  API Key in dictionaryapi.com. It is an API Key provider of Merriam Webster Dictionary
 	url = f'https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={api_key}'

	r = requests.get(url)

	result = r.json()
	dictionary_definition = result[0]['shortdef']
	sorted_def = list(zip(range(1, 300), dictionary_definition))

	print(f"Definitions of {word.capitalize()}:")
	speak(f"Definitions of {word.capitalize()}:")
	for dictionary_definition in sorted_def:
		print(f"\t{dictionary_definition[0]}: {dictionary_definition[1]}")
		speak(f"\t{dictionary_definition[0]}: {dictionary_definition[1]}")
	print()
	print("*" * 150)


def thesaurus(word: str):
	try:
		api_key = 'your api key'  # You can create an  API Key in dictionaryapi.com. It is an API Key provider of Merriam Webster Dictionary
		url = f'https://dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={api_key}'

		r = requests.get(url)

		result = r.json()
		synonyms = result[0]['meta']['syns']
		antonyms = result[0]['meta']['ants']

		print(result)

		print(f"\nSynonyms of {word}:")
		speak(f"\nSynonyms of {word}:")
		for s in synonyms:
			for syn in s:
				print(f"{syn.capitalize()},", end=' ')
		print('\n' + ('*' * 125))
		time.sleep(5)

		print(f"\nAntonyms of {word}:")
		speak(f"\nAntonyms of {word}:")
		for a in antonyms:
			for ant in a:
				print(f"{ant.capitalize()},", end=' ')
		print('\n' + ('*' * 125))
		time.sleep(5)
	except:
		print(
			'ERROR fetched:\nUnfortunately, I cannot provide you with the details for the desired word because of some error')


month_string = {
	1: 'January',
	2: 'February',
	3: 'March',
	4: 'April',
	5: 'May',
	6: 'June',
	7: 'July',
	8: 'August',
	9: 'September',
	10: 'October',
	11: 'November',
	12: 'December'
}
