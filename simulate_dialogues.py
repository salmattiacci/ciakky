import pyttsx3
import PyPDF2
import re
import speech_recognition as sr

# Initialize the Text-to-Speech engine
engine = pyttsx3.init()

# Set the voice (optional)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Get user input for playbook path
def get_playbook_path():
    return input("Enter the path to your playbook: ")

# Get user input for page range
def get_page_range():
    start_page = int(input("Enter the starting page number (1-indexed): "))
    end_page = int(input("Enter the ending page number (1-indexed): "))
    return start_page - 1, end_page

# Get user input for character names
def get_characters():
    interlocutor = input("Enter your interlocutor character name: ")
    your_character = input("Enter your character name: ")
    return interlocutor, your_character

# Recognize user speech
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Speak now...')
        audio = r.listen(source)
    try:
        language = "it-IT"  # Set language to Italian
        return r.recognize_google(audio, language=language)
    except sr.UnknownValueError:
        print('Could not understand audio')
    except sr.RequestError as e:
        print(f'Error: {e}')
    return None

# Extract dialogues from playbook
def extract_dialogues(playbook_path, start_page, end_page, interlocutor, your_character):
    with open(playbook_path, 'rb') as playbook_file:
        pdf_reader = PyPDF2.PdfReader(playbook_file)
        text = ""

        for page_num in range(start_page, end_page):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

    pattern = f"(?<={interlocutor} ).+?(?={your_character})"
    regex = re.compile(pattern, re.IGNORECASE)
    dialogues = regex.findall(text)

    return dialogues

# Simulate dialogue
def simulate_dialogue(dialogues):
    for sentence in dialogues:
        engine.say(sentence)
        engine.runAndWait()
        response = recognize_speech()
        while not response:
            response = recognize_speech()
        print(your_character+":", response)

# Get user input
playbook_path = get_playbook_path()
start_page, end_page = get_page_range()
interlocutor, your_character = get_characters()

# Extract dialogues
dialogues = extract_dialogues(playbook_path, start_page, end_page, interlocutor, your_character)

# Simulate dialogue
simulate_dialogue(dialogues)
