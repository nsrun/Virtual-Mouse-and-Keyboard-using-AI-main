import pyttsx3
import speech_recognition as sr
from datetime import date
import time
import webbrowser
import datetime
from pynput.keyboard import Key, Controller
import pyautogui
import sys
import os
from os import listdir
from os.path import isfile, join
import smtplib
import wikipedia
import app
from threading import Thread

# -------------Object Initialization---------------
today = date.today()
r = sr.Recognizer()
keyboard = Controller()
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# ----------------Variables------------------------
file_exp_status = False
files = []
path = ''
is_awake = True  # Bot status


# ------------------Functions----------------------
def reply(audio):
    try:
        app.ChatBot.addAppMsg(audio)
    except:
        pass
    print(f"🤖 Proton: {audio}")
    engine.say(audio)
    engine.runAndWait()


def wish():
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour < 12:
        reply("Good Morning!")
    elif hour >= 12 and hour < 18:
        reply("Good Afternoon!")
    else:
        reply("Good Evening!")

    reply("I am Proton, how may I help you?")


# Set Microphone parameters
try:
    with sr.Microphone() as source:
        r.energy_threshold = 500
        r.dynamic_energy_threshold = False
except:
    print("⚠️ Warning: Microphone not available")


# Audio to String
def record_audio():
    try:
        with sr.Microphone() as source:
            print("🎤 Listening...")
            r.pause_threshold = 0.8
            voice_data = ''
            audio = r.listen(source, phrase_time_limit=5)

            try:
                print("🔄 Recognizing...")
                voice_data = r.recognize_google(audio)
                print(f"👤 You said: {voice_data}")
            except sr.RequestError:
                reply('Sorry my Service is down. Please check your Internet connection')
            except sr.UnknownValueError:
                print('❌ Could not recognize speech')
                pass
            return voice_data.lower()
    except Exception as e:
        print(f"Error in record_audio: {str(e)}")
        return ""


# Executes Commands (input: string)
def respond(voice_data):
    global file_exp_status, files, is_awake, path

    if not voice_data:
        return

    print(f"\n{'=' * 60}")
    print(f"📥 Original input: '{voice_data}'")

    # Remove 'proton' from the command
    voice_data = voice_data.replace('proton', '').strip()
    print(f"📝 Processed command: '{voice_data}'")
    print(f"{'=' * 60}\n")

    try:
        app.eel.addUserMsg(voice_data)
    except:
        pass

    # Check if bot is awake
    if is_awake == False:
        if 'wake up' in voice_data:
            is_awake = True
            wish()
        return

    # STATIC CONTROLS - Basic Interactions
    if 'hello' in voice_data or 'hi' in voice_data or 'hey' in voice_data:
        print("✅ Matched: Greeting")
        wish()

    elif 'what is your name' in voice_data or 'your name' in voice_data:
        print("✅ Matched: Name query")
        reply('My name is Proton!')

    elif 'date' in voice_data:
        print("✅ Matched: Date query")
        reply(today.strftime("%B %d, %Y"))

    elif 'time' in voice_data:
        print("✅ Matched: Time query")
        reply(str(datetime.datetime.now()).split(" ")[1].split('.')[0])

    # SEARCH & WEB CONTROLS
    elif 'search' in voice_data:
        print("✅ Matched: Search command")
        search_query = voice_data.replace('search', '').replace('for', '').strip()
        if search_query:
            reply('Searching for ' + search_query)
            url = 'https://google.com/search?q=' + search_query.replace(' ', '+')
            try:
                webbrowser.open(url)
                reply('Here are the results')
            except:
                reply('Please check your Internet')
        else:
            reply('What do you want me to search for?')

    elif 'location' in voice_data or 'locate' in voice_data or 'map' in voice_data:
        print("✅ Matched: Location command")
        location_query = voice_data.replace('location', '').replace('locate', '').replace('map', '').strip()

        if location_query and location_query not in ['my', 'me', 'current']:
            reply('Locating ' + location_query)
            url = 'https://www.google.com/maps/search/' + location_query.replace(' ', '+')
        else:
            reply('Which place are you looking for?')
            temp_audio = record_audio()
            try:
                app.eel.addUserMsg(temp_audio)
            except:
                pass
            reply('Locating...')
            url = 'https://www.google.com/maps/search/' + temp_audio.replace(' ', '+')

        try:
            webbrowser.open(url)
            reply('This is what I found')
        except:
            reply('Please check your Internet')

    elif 'wikipedia' in voice_data or 'wiki' in voice_data:
        print("✅ Matched: Wikipedia search")
        try:
            query = voice_data.replace('wikipedia', '').replace('wiki', '').replace('search', '').strip()
            if query:
                reply(f'Searching Wikipedia for {query}')
                result = wikipedia.summary(query, sentences=2)
                reply(result)
            else:
                reply('What do you want to search on Wikipedia?')
        except wikipedia.exceptions.DisambiguationError:
            reply('Multiple results found. Please be more specific')
        except wikipedia.exceptions.PageError:
            reply('No Wikipedia page found for that query')
        except:
            reply('Wikipedia search failed')

    elif 'weather' in voice_data:
        print("✅ Matched: Weather query")
        city = voice_data.replace('weather', '').replace('in', '').strip()
        if not city:
            city = 'current location'
        url = f'https://www.google.com/search?q=weather+{city.replace(" ", "+")}'
        try:
            webbrowser.open(url)
            reply(f'Showing weather for {city}')
        except:
            reply('Failed to open weather information')

    elif 'play' in voice_data and 'play' not in ['display', 'replay']:
        print("✅ Matched: Play music/video")
        song = voice_data.replace('play', '').strip()
        if song:
            url = f'https://www.youtube.com/results?search_query={song.replace(" ", "+")}'
            try:
                webbrowser.open(url)
                reply(f'Playing {song} on YouTube')
            except:
                reply('Failed to open YouTube')
        else:
            reply('What would you like me to play?')

    elif 'news' in voice_data:
        print("✅ Matched: News")
        try:
            url = 'https://news.google.com/'
            webbrowser.open(url)
            reply('Opening Google News')
        except:
            reply('Failed to open news')

    # SYSTEM CONTROLS - Applications
    elif 'notepad' in voice_data:
        print("✅ Matched: Open Notepad")
        try:
            os.system('notepad.exe')
            reply('Opening Notepad')
        except:
            reply('Failed to open Notepad')

    elif 'calculator' in voice_data:
        print("✅ Matched: Open Calculator")
        try:
            os.system('calc.exe')
            reply('Opening Calculator')
        except:
            reply('Failed to open Calculator')

    elif 'chrome' in voice_data:
        print("✅ Matched: Open Chrome")
        try:
            os.system('start chrome')
            reply('Opening Chrome Browser')
        except:
            reply('Failed to open Chrome')

    elif 'paint' in voice_data:
        print("✅ Matched: Open Paint")
        try:
            os.system('mspaint.exe')
            reply('Opening Paint')
        except:
            reply('Failed to open Paint')

    elif 'file explorer' in voice_data or ('open' in voice_data and 'explorer' in voice_data):
        print("✅ Matched: Open File Explorer")
        try:
            os.system('explorer.exe')
            reply('Opening File Explorer')
        except:
            reply('Failed to open File Explorer')

    # VOLUME CONTROLS
    elif 'volume up' in voice_data or 'increase volume' in voice_data or 'louder' in voice_data:
        print("✅ Matched: Volume Up")
        try:
            for i in range(5):
                pyautogui.press('volumeup')
            reply('Volume increased')
        except:
            reply('Failed to increase volume')

    elif 'volume down' in voice_data or 'decrease volume' in voice_data or 'quieter' in voice_data:
        print("✅ Matched: Volume Down")
        try:
            for i in range(5):
                pyautogui.press('volumedown')
            reply('Volume decreased')
        except:
            reply('Failed to decrease volume')

    elif 'mute' in voice_data or 'unmute' in voice_data:
        print("✅ Matched: Mute toggle")
        try:
            pyautogui.press('volumemute')
            reply('Volume toggled')
        except:
            reply('Failed to toggle volume')

    # SCREENSHOT
    elif 'screenshot' in voice_data or 'capture screen' in voice_data:
        print("✅ Matched: Screenshot")
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'screenshot_{timestamp}.png'
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            reply(f'Screenshot saved as {filename}')
        except:
            reply('Failed to take screenshot')

    # KEYBOARD SHORTCUTS
    elif 'copy' in voice_data and 'clipboard' not in voice_data:
        print("✅ Matched: Copy")
        with keyboard.pressed(Key.ctrl):
            keyboard.press('c')
            keyboard.release('c')
        reply('Copied')

    elif 'paste' in voice_data:
        print("✅ Matched: Paste")
        with keyboard.pressed(Key.ctrl):
            keyboard.press('v')
            keyboard.release('v')
        reply('Pasted')

    elif 'select all' in voice_data:
        print("✅ Matched: Select All")
        with keyboard.pressed(Key.ctrl):
            keyboard.press('a')
            keyboard.release('a')
        reply('Selected all')

    elif 'undo' in voice_data:
        print("✅ Matched: Undo")
        with keyboard.pressed(Key.ctrl):
            keyboard.press('z')
            keyboard.release('z')
        reply('Undone')

    elif 'redo' in voice_data:
        print("✅ Matched: Redo")
        with keyboard.pressed(Key.ctrl):
            keyboard.press('y')
            keyboard.release('y')
        reply('Redone')

    elif 'save file' in voice_data or ('save' in voice_data and 'file' in voice_data):
        print("✅ Matched: Save File")
        with keyboard.pressed(Key.ctrl):
            keyboard.press('s')
            keyboard.release('s')
        reply('File saved')

    # WINDOW MANAGEMENT
    elif 'minimize' in voice_data:
        print("✅ Matched: Minimize")
        try:
            pyautogui.hotkey('win', 'down')
            reply('Window minimized')
        except:
            reply('Failed to minimize window')

    elif 'maximize' in voice_data:
        print("✅ Matched: Maximize")
        try:
            pyautogui.hotkey('win', 'up')
            reply('Window maximized')
        except:
            reply('Failed to maximize window')

    elif 'close window' in voice_data or 'close tab' in voice_data:
        print("✅ Matched: Close window")
        try:
            pyautogui.hotkey('alt', 'f4')
            reply('Window closed')
        except:
            reply('Failed to close window')

    elif 'new tab' in voice_data:
        print("✅ Matched: New Tab")
        try:
            pyautogui.hotkey('ctrl', 't')
            reply('New tab opened')
        except:
            reply('Failed to open new tab')

    elif 'switch tab' in voice_data:
        print("✅ Matched: Switch Tab")
        try:
            pyautogui.hotkey('ctrl', 'tab')
            reply('Switched tab')
        except:
            reply('Failed to switch tab')

    # BOT CONTROLS
    elif 'bye' in voice_data or 'goodbye' in voice_data:
        print("✅ Matched: Goodbye")
        reply("Goodbye! Have a nice day.")
        is_awake = False

    elif 'exit' in voice_data or 'terminate' in voice_data or 'shut down' in voice_data:
        print("✅ Matched: Exit")
        reply("Shutting down. Goodbye!")
        app.ChatBot.close()
        sys.exit()

    # FILE NAVIGATION
    elif 'list files' in voice_data or 'list' in voice_data:
        print("✅ Matched: List files")
        counter = 0
        path = 'C://'
        files = listdir(path)
        filestr = ""
        for f in files:
            counter += 1
            print(str(counter) + ':  ' + f)
            filestr += str(counter) + ':  ' + f + '<br>'
        file_exp_status = True
        reply('These are the files in your root directory')
        try:
            app.ChatBot.addAppMsg(filestr)
        except:
            pass

    elif file_exp_status == True:
        counter = 0
        if 'open' in voice_data:
            try:
                file_num = int(voice_data.split(' ')[-1]) - 1
                if isfile(join(path, files[file_num])):
                    os.startfile(path + files[file_num])
                    file_exp_status = False
                    reply('File opened')
                else:
                    path = path + files[file_num] + '//'
                    files = listdir(path)
                    filestr = ""
                    for f in files:
                        counter += 1
                        filestr += str(counter) + ':  ' + f + '<br>'
                        print(str(counter) + ':  ' + f)
                    reply('Opened Successfully')
                    try:
                        app.ChatBot.addAppMsg(filestr)
                    except:
                        pass
            except:
                reply('You do not have permission to access this folder')

        if 'back' in voice_data:
            filestr = ""
            if path == 'C://':
                reply('Sorry, this is the root directory')
            else:
                a = path.split('//')[:-2]
                path = '//'.join(a)
                path += '//'
                files = listdir(path)
                for f in files:
                    counter += 1
                    filestr += str(counter) + ':  ' + f + '<br>'
                    print(str(counter) + ':  ' + f)
                reply('Going back')
                try:
                    app.ChatBot.addAppMsg(filestr)
                except:
                    pass

    else:
        print("❌ No matching command found")
        reply('Sorry, I am not programmed to do that yet!')


# ------------------Main Function--------------------
def main():
    """Main execution function"""
    print("\n" + "=" * 60)
    print("🚀 PROTON VOICE ASSISTANT")
    print("=" * 60)
    print("💡 Tips:")
    print("   - Say 'Proton' before each command")
    print("   - Available commands: hello, time, date, search, open apps")
    print("   - Say 'Proton exit' to quit")
    print("=" * 60 + "\n")

    # Start the ChatBot GUI in a separate thread
    t1 = Thread(target=app.ChatBot.start)
    t1.daemon = True
    t1.start()

    # Wait for Chatbot to initialize
    print("⏳ Starting Proton Assistant...")
    max_wait = 30  # Maximum 30 seconds wait
    wait_count = 0
    while not app.ChatBot.started and wait_count < max_wait:
        time.sleep(0.5)
        wait_count += 1
        if wait_count % 4 == 0:
            print(".", end="", flush=True)

    if not app.ChatBot.started:
        print("\n⚠️ Warning: GUI not started, running in console mode")
    else:
        print("\n✅ GUI Started!")

    # Greet the user
    wish()

    # Main loop
    voice_data = None
    while True:
        try:
            if app.ChatBot.isUserInput():
                # Take input from GUI
                voice_data = app.ChatBot.popUserInput()
                print(f"💬 GUI Input: {voice_data}")
                # Add 'proton' prefix if not present for GUI inputs
                if voice_data and 'proton' not in voice_data.lower():
                    voice_data = 'proton ' + voice_data
            else:
                # Take input from Voice
                voice_data = record_audio()

            # Process voice_data
            if voice_data and 'proton' in voice_data.lower():
                respond(voice_data)
            elif voice_data:
                print(f"⚠️ Command must start with 'Proton'. You said: '{voice_data}'")

        except SystemExit:
            print("👋 Exiting...")
            break
        except KeyboardInterrupt:
            print("\n👋 Shutting down...")
            reply("Shutting down...")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            continue


# ------------------Driver Code--------------------
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Proton Assistant stopped by user")
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        import traceback

        traceback.print_exc()
    finally:
        print("🛑 Proton Assistant shutdown complete")
        sys.exit(0)