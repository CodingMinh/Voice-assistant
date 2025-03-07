# credit to gaurav on geeksforgeeks & sayantanl on github
# gaurav: https://www.geeksforgeeks.org/voice-assistant-using-python/
# sayantanl: https://github.com/01-SayantanI/Assistant
# make sure you install all libraries before running
# libraries to install: pip install wolframalpha pyttsx3 speechrecognition wikipedia pyjokes feedparser requests twilio clint ecapture beautifulsoup4 pycountry pywhatkit plyer pillow winshell newsapi-python PyAudio
# if missing any libraries, install them using pip install LIBRARY_NAME_1 LIBRARY_NAME_2
import subprocess
import wolframalpha
import pyttsx3
import tkinter as tk
from tkinter import ttk
from tkinter import LEFT, BOTH, SUNKEN
import json
import random
import operator
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import winshell
import pyjokes
import feedparser
import smtplib
import ctypes
import time
import requests
import shutil
from twilio.rest import Client
from clint.textui import progress
from ecapture import ecapture as ec
from bs4 import BeautifulSoup
import win32com.client as wincl
from urllib.request import urlopen
import newsapi
from newsapi import NewsApiClient
import pycountry
import pywhatkit as kit
from plyer import notification
from PIL import Image, ImageTk
from threading import Thread

# Create an instance of NewsApiClient
newsapi = NewsApiClient(api_key='16536c5d322f4a9facc23ffa6e9b467c')  # Replace 'YOUR_API_KEY' with your actual News API key

# Constants for custom styling
BG_COLOR = "#D2C6E2"

BUTTON_COLOR = "#F9F4F2"

BUTTON_FONT = ("Arial", 14, "bold")

BUTTON_FOREGROUND = "black"

HEADING_FONT = ("white", 24, "bold")

INSTRUCTION_FONT = ("Helvetica", 14)

INSTRUCTION_FONT1 = ("Helvetica", 14)

entry = None
stop_flag = False

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) # [0] if you want male voice, [1] if you want female voice

# change this line to open different browsers like Chrome or Firefox
opera_path = r"C:\\Users\\Hi Windows 11 23\\AppData\\Local\\Programs\\Opera GX\\opera.exe"
webbrowser.register('opera', None, webbrowser.BackgroundBrowser(opera_path))

def speak(audio):
	engine.say(audio)
	engine.runAndWait()

def wishMe():
	hour = int(datetime.datetime.now().hour)
	if hour>= 0 and hour<12:
		speak("Good Morning Sir !")

	elif hour>= 12 and hour<18:
		speak("Good Afternoon Sir !") 

	else:
		speak("Good Evening Sir !") 

	uname =("Jarvis 1 point o")
	speak("I am your Assistant")
	speak(uname)
	speak("How can i Help you, Sir")
	
# Use this if you want to say your name instead of typing it (not recommended)
# You can customize what you want the assistant to call you: Mister, Miss, Madame, etc.
# Press Ctrl+F to find all instances of Mister, Sir, etc. and replace them as needed
def username():
	speak("What should i call you sir")
	user_name = takeCommand()
	speak("Welcome Mister")
	speak(user_name)
	columns = shutil.get_terminal_size().columns
	
	print("#####################".center(columns))
	print("Welcome Mr.", user_name.center(columns))
	print("#####################".center(columns))
	
	speak("How can i Help you, Sir")

def takeCommand():
	
	r = sr.Recognizer()
	
	with sr.Microphone() as source:
		
		print("Listening...")
		r.pause_threshold = 1
		r.adjust_for_ambient_noise(source, duration=0.5)
		audio = r.listen(source)

	try:
		print("Recognizing...") 
		query = r.recognize_google(audio, language ='en-in')
		print(f"User said: {query}\n")

	except Exception as e:
		print(e) 
		print("Unable to Recognize your voice.") 
		return "None"
	
	return query

def sendEmail(to, content):
	server = smtplib.SMTP('smtp.gmail.com', 587) # we use port number 587 for gmail, other emails might use a different port number
	server.ehlo()
	server.starttls() # start tls for security
	
	# Authentication
	server.login('ng.minh0209@gmail.com', 'cYkwew-soffuz-4fypto')
	# send mail to "to" with the message "content"
	server.sendmail('ng.minh0209@gmail.com', to, content)
	server.close()

# get_country_code, fetch_news, display_headlines, and get_weather don't necessarily have to be functions
# you could put it directly inside the elif, but I found it easier to make them functions
def get_country_code(country_name):
	# Create a dictionary of country names and their codes
	countries = {country.name: country.alpha_2 for country in pycountry.countries}
	return countries.get(country_name.title(), 'Unknown code')

def fetch_news(country_code, category):
	# Fetch top headlines based on country code and category
	top_headlines = newsapi.get_top_headlines(
		category=category.lower(), language='en', country=country_code.lower()
	)
	return top_headlines['articles']

def display_headlines(articles):
	# Display fetched news articles
	if articles:
		for article in articles:
			title = article['title']
			source = article['source']['name']
			print(f"{source}: {title}.")
			speak(f"{source} reports: {title}")
	else:
		speak("Sorry, no articles found. Something went wrong!")

def get_weather(city_name):
	api_key = "c83939c78acceb97819aaccaf70e3d36"  # Replace with your actual OpenWeather API key
	base_url = "http://api.openweathermap.org/data/2.5/weather"
	
	# Construct the complete URL
	complete_url = f"{base_url}?q={city_name}&appid={api_key}&units=metric"  # Use 'metric' for Celsius

	response = requests.get(complete_url)

	if response.status_code == 200:
		data = response.json()
		main = data['main']
		weather_desc = data['weather'][0]['description']
		temperature = main['temp']
		pressure = main['pressure']
		humidity = main['humidity']

		weather_info = (f"The temperature in {city_name} is {temperature}°C with "
						f"{weather_desc}. The atmospheric pressure is {pressure} hPa "
						f"and the humidity is {humidity}%.")
		return weather_info
	else:
		return "Sorry, I couldn't find the weather information for that location."

def perform_task():
	# This Function will clean any
	# command before execution of this python file
	global stop_flag
	global entry
	clear()
	wishMe()
	dassname = entry.get() # this will be the name you entered in the GUI
	while not stop_flag:
		
		query = takeCommand().lower()
		
		# All the commands said by user will be 
		# stored here in 'query' and will be
		# converted to lower case for easily 
		# recognition of command
		if 'wikipedia' in query:
			speak('Searching Wikipedia...')
			query = query.replace("wikipedia", "")
			results = wikipedia.summary(query, sentences = 3)
			speak("According to Wikipedia")
			print(results)
			speak(results)

		elif 'open youtube' in query:
			speak("Here you go to Youtube\n")
			webbrowser.get('opera').open("youtube.com")

		elif 'open google' in query:
			speak("Here you go to Google\n")
			webbrowser.get('opera').open("google.com")

		elif 'open stack overflow' in query:
			speak("Here you go to Stack Over flow.Happy coding")
			webbrowser.get('opera').open("stackoverflow.com") 

		elif 'play music' in query or "play song" in query:
			speak("Here you go with music")
			music_dir = "D:\Songs"
			songs = os.listdir(music_dir)
			print(songs) 
			random = os.startfile(os.path.join(music_dir, songs[1]))

		elif 'the time' in query:
			strTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
			speak(f"Sir, the time is {strTime}")

		elif 'open opera' in query:
			codePath = r"C:\\Users\\Hi Windows 11 23\\AppData\\Local\\Programs\\Opera GX\\opera.exe"
			os.startfile(codePath)

		# to allow the voice assistant to send emails, you need to either enable less secure apps or app passwords
		# use at your own risk

		#elif 'email to me' in query:
		#	try:
		#		speak("What should I say?")
		#		content = takeCommand()
		#		to = "ng.minh0209@gmail.com" # put your email here
		#		sendEmail(to, content)
		#		speak("Email has been sent !")
		#	except Exception as e:
		#		print(e)
		#		speak("I am not able to send this email")

		#elif 'send a mail' in query:
		#	try:
		#		speak("What should I say?")
		#		content = takeCommand()
		#		speak("Whom should i send?")
		#		to = input() # type your receiver email here
		#		sendEmail(to, content)
		#		speak("Email has been sent !")
		#	except Exception as e:
		#		print(e)
		#		speak("I am not able to send this email")

		elif 'how are you' in query:
			speak("I am fine, Thank you")
			speak("How are you, Sir")

		elif 'fine' in query or "well" in query:
			speak("It's good to know that your fine")

		elif "change my name to" in query:
			query = query.replace("change my name to", "")
			dassname = query
			speak("Understood, hello mister " + dassname)

		elif "what is my name" in query or "what's my name" in query:
			speak("hello mister ")
			speak(dassname)

		#elif 'exit' in query:
		#	speak("Thanks for giving me your time")
		#	stop_voice_assistant()

		elif "who made you" in query or "who created you" in query: 
			speak("I have been created by you.")
			
		elif 'joke' in query:
			speak(pyjokes.get_joke())
			
		elif "calculate" in query: 
			
			app_id = "KV3H4H-V9P3KK6896"
			client = wolframalpha.Client(app_id)
			indx = query.lower().split().index('calculate') 
			query = query.split()[indx + 1:] 
			res = client.query(' '.join(query)) 
			answer = next(res.results).text
			print("The answer is " + answer) 
			speak("The answer is " + answer) 

		elif 'search' in query:
			speak("Here's what I found")
			query = query.replace("search", "") 
			# Create the Google search URL based on the query
			search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
			webbrowser.get('opera').open(search_url)
		
		elif 'play' in query:
			speak("Here you go")
			song_name = query.replace("play", "")
			# Create the YouTube search URL based on the song name
			search_url = f"https://www.youtube.com/results?search_query={song_name.replace(' ', '+')}"
			webbrowser.get('opera').open(search_url)

		elif "who i am" in query:
			speak("If you talk then definitely your human.")

		elif "why you came to world" in query:
			speak("Thanks to you! further It's a secret")

		#elif 'power point presentation' in query:
			#speak("opening Power Point presentation")
			#power = r"C:\\Users\\"
			#os.startfile(power)

		elif 'is love' in query:
			speak("It is 7th sense that destroy all other senses")

		elif "who are you" in query:
			speak("I am your virtual assistant created by you")

		elif 'reason for you' in query:
			speak("I was created as a personal project by Mister Minh")

		elif 'change background' in query:
			ctypes.windll.user32.SystemParametersInfoW(20, 
													0, 
													"E:\god-of-war-ragnarok-ps4-ps5-wallpapers-01.jpg", # input wallpaper location as path here
													0)
			speak("Background changed successfully")

		#elif 'open bluestack' in query:
			#appli = r"C:\\ProgramData\\BlueStacks\\Client\\Bluestacks.exe"
			#os.startfile(appli)
		
		elif 'top news' in query or 'news' in query:
			speak("Which country are you interested in?")
			country_name = takeCommand()

			# Get the country code from the provided country name
			country_code = get_country_code(country_name)
			if country_code == 'Unknown code':
				speak("Sorry, I couldn't find the country code for that. Please try again.")
				continue

			speak("What topic are you interested in? You can say business, entertainment, general, health, science, or technology.")
			topic = takeCommand().lower()
			
			# Define a mapping for the topics to categories
			category_map = {
				'business': 'business',
				'entertainment': 'entertainment',
				'general': 'general',
				'health': 'health',
				'science': 'science',
				'technology': 'technology'
			}
			
			category = category_map.get(topic)
			
			if category:
				articles = fetch_news(country_code, category)
				display_headlines(articles)
			else:
				speak("I didn't understand the topic. Please try again.")


		elif 'lock window' in query:
				speak("locking the device")
				ctypes.windll.user32.LockWorkStation()

		elif 'shutdown system' in query:
				speak("Hold On a Sec ! Your system is on its way to shut down")
				subprocess.call('shutdown / p /f')
				
		elif 'empty recycle bin' in query:
			winshell.recycle_bin().empty(confirm = False, show_progress = False, sound = True)
			speak("Recycle Bin Recycled")

		elif "don't listen" in query or "stop listening" in query:
			speak("for how much time you want to stop jarvis from listening commands")
			a = int(takeCommand())
			time.sleep(a)
			print(a)

		elif "where is" in query:
			query = query.replace("where is", "")
			location = query
			speak("User asked to Locate")
			speak(location)
			webbrowser.get('opera').open("https://www.google.com/maps/place/" + location.replace(" ", "+"))

		elif "camera" in query or "take a photo" in query:
			ec.capture(0, "Jarvis Camera ", "img.jpg")

		elif "restart" in query:
			subprocess.call(["shutdown", "/r"])
			
		elif "hibernate" in query or "sleep" in query:
			speak("Hibernating")
			subprocess.call("shutdown / h")

		elif "log off" in query or "sign out" in query:
			speak("Make sure all the application are closed before sign-out")
			time.sleep(5)
			subprocess.call(["shutdown", "/l"])

		elif "write a note" in query:
			speak("What should i write, sir")
			note = takeCommand()
			file = open('jarvis.txt', 'w')
			speak("Sir, Should i include date and time")
			snfm = takeCommand()
			if 'yes' in snfm or 'sure' in snfm:
				strTime = datetime.datetime.now().strftime("% H:% M:% S")
				file.write(strTime)
				file.write(" :- ")
				file.write(note)
			else:
				file.write(note)
		
		elif "show note" in query:
			speak("Showing Notes")
			file = open("jarvis.txt", "r") 
			print(file.read())
			speak(file.read(6))

		elif "update assistant" in query:
			speak("After downloading file please replace this file with the downloaded one")
			url = '# url after uploading file'
			r = requests.get(url, stream = True)
			
			with open("Voice.py", "wb") as Pypdf:
				
				total_length = int(r.headers.get('content-length'))
				
				for ch in progress.bar(r.iter_content(chunk_size = 2391975),
									expected_size =(total_length / 1024) + 1):
					if ch:
						Pypdf.write(ch)
					
		# NPPR9-FWDCX-D2C8J-H872K-2YT43
		elif "jarvis" in query:
			
			wishMe()
			speak("Jarvis 1 point o in your service Mister")
			speak(dassname)

		elif "weather" in query:
			speak("Which city do you want the weather for?")
			print("City name: ")
			city_name = takeCommand()
			weather_info = get_weather(city_name)
			speak(weather_info)
			print(weather_info)
			
		#elif "send message " in query:
		#		# You need to create an account on Twilio to use this service
		#		account_sid = 'Account Sid key'
		#		auth_token = 'Auth token'
		#		client = Client(account_sid, auth_token)
		#
		#		message = client.messages \
		#						.create(
		#							body = takeCommand(),
		#							from_='Sender No',
		#							to ='Receiver No'
		#						)
		#
		#		print(message.sid)

		elif "go to the wiki" in query:
			webbrowser.get('opera').open("https://www.wikipedia.org")

		elif "good morning" in query:
			speak("A warm" + query)
			speak("How are you Mister")
			speak(dassname)

		# most asked question from google Assistant
		elif "will you be my gf" in query or "will you be my bf" in query: 
			speak("I'm not sure about, may be you should give me some time")

		elif "how are you" in query:
			speak("I'm fine, glad you asked me that")

		elif "i love you" in query:
			speak("It's hard to understand")

		elif "what is" in query and "your name" not in query:
			
			# Use the same API key of WolframAlpha
			# that we have generated earlier
			app_id = "KV3H4H-V9P3KK6896"
			client = wolframalpha.Client(app_id)
			res = client.query(''.join(query)) 
			
			try:
				print (next(res.results).text)
				speak (next(res.results).text)
			except StopIteration:
				print ("No results")
			
		elif "who is" in query:
			speak("I don't know, but here's what I found")
			query = query.replace("who is", "") 
			# Create the Google search URL based on the query
			search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
			webbrowser.get('opera').open(search_url)
		
		elif "what is your name" in query or "what's your name" in query:
			speak("My name is Jarvis, your personal voice assistant")

		# elif "" in query:
			# Command go here
			# For adding more commands

def stop_voice_assistant():
	global stop_flag
	speak("Stopping the Voice Assistant.")
	stop_flag = True

def start_voice_assistant():
	global stop_flag
	perform_task()
	stop_flag = False  # Reset the flag to False when starting the voice assistant

def main():
	# Create the main GUI window
	root = tk.Tk()
	root.title("Voice Assistant")
	root.geometry("2700x1745")
	root.configure(bg=BG_COLOR)

	def on_button_click():
		global stop_flag
		if not stop_flag:
			stop_flag = False  # Reset the flag to False when starting the voice assistant
			Thread(target=start_voice_assistant).start()
		else:
			stop_voice_assistant()
	def on_button_click_2():
		stop_voice_assistant()
		root.destroy()

	# Load and set the background image
	background_image = Image.open("C:\\Users\\Hi Windows 11 23\\Desktop\Python\\Voice assistant\\background.jpg")  
	# Replace this with the actual image file path on your computer
	background_photo = ImageTk.PhotoImage(background_image)
	background_label = ttk.Label(root, image=background_photo)
	background_label.place(x=0, y=0, relwidth=1, relheight=1)

	f1 = ttk.Frame(root)
	f1.pack(pady=100)  # Add some padding to the frame to center it vertically

	image2 = Image.open("C:\\Users\\Hi Windows 11 23\\Desktop\\Python\Voice assistant\\mic icon.jpg")  
	# Replace this with the actual path to your image on your computer
	resized_image = image2.resize((240, 240))
	p2 = ImageTk.PhotoImage(resized_image)
	l2 = ttk.Label(f1, image=p2, relief=SUNKEN)
	l2.pack(side="top", fill="both")

	# Heading
	heading_label = ttk.Label(root, text="Voice Assistant", font=HEADING_FONT, background=BG_COLOR)
	heading_label.pack(pady=20)

	global entry
	f1 = ttk.Frame(root)
	f1.pack()
	l1 = ttk.Label(f1, text="Enter Your Name", font=INSTRUCTION_FONT, background=BG_COLOR)
	l1.pack(side=LEFT, fill=BOTH)
	entry = ttk.Entry(f1, width=30)
	entry.pack(pady=10)

	# Instruction
	instruction_label = ttk.Label(root, text="Click the button below to start the Voice Assistant",
								  font=INSTRUCTION_FONT, background=BG_COLOR)
	instruction_label.pack(pady=20)

	# Style the button
	style = ttk.Style(root)
	style.configure("VoiceAssistant.TButton", font=BUTTON_FONT, background=BUTTON_COLOR, foreground=BUTTON_FOREGROUND)

	# Create and place a button on the GUI
	button = ttk.Button(root, text="Start Voice Assistant", command=on_button_click, style="VoiceAssistant.TButton")
	button.pack(pady=20)

	# Button to stop the voice assistant
	button2 = ttk.Button(root, text="Stop Voice Assistant", command=on_button_click_2, style="VoiceAssistant.TButton")
	button2.pack(pady=20) 

	# Run the GUI main loop
	root.mainloop()

if __name__ == '__main__':
	clear = lambda: os.system('cls')

	main()
