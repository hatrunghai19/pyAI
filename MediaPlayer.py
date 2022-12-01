# ==== Importing all the necessary libraries
import speech_recognition as sr
import pyttsx3
import datetime
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import os, easygui
from threading import Thread
import webbrowser as wb
import vlc
# ==== Class Assistant
class assistance_gui:
    def __init__(self):
        self.root = Tk()
        self.root.title("Chatter")

        self.st = ScrolledText(self.root)
        
    
    def run(self):
        ACCEPT_THREAD = Thread(target=self.start)
        ACCEPT_THREAD.start()
        self.root.mainloop()
    def show(self,text):
        self.st.insert(END, text+"\n")
        self.st.pack()
    # def start(self):
    def start(self):
        listener = sr.Recognizer()
        engine = pyttsx3.init()
        engine.setProperty('volume', 1.0)
        # ==== Voice Control
        def speak(text):
            self.show("Robot: "+ text)
            engine.say(text)
            engine.runAndWait()
        # ==== start wellcome
        def wellcome():
            listener = sr.Recognizer()
            # ==== Wish Start
            hour = int(datetime.datetime.now().hour)
            if hour >= 0 and hour < 12:
                wish = "Good Morning!"
            elif hour >= 12 and hour < 18:
                wish = "Good Afternoon!"
            else:
                wish = "Good Evening!"
            robot_speech = wish+ "Can i help you?"
            speak(robot_speech)
            # ==== Wish End

        # ==== Take Command
        def take_command():
            try:
                # speech to text
                with sr.Microphone() as data_taker:
                    listener.adjust_for_ambient_noise(data_taker, duration=1)
                    voice = listener.listen(data_taker)
                    try:
                        instruction = listener.recognize_google(voice)
                    except sr.UnknownValueError:
                        instruction = ""
                    
                    return instruction
            except:
                pass

        # ==== Run command
        def run_command():
            instruction = take_command().lower()
            self.show("You: "+instruction)
            try:
                if 'open file' in instruction:
                    speak('Opening file.')
                    ACCEPT_THREAD = Thread(target=play_media)
                    ACCEPT_THREAD.start()
                elif 'shutdown' in instruction:
                    # shutting down
                    speak('I am shutting down')
                    self.close_window()
                    return False
                elif 'listen to music' in instruction:
                    #chooose music on off
                    speak('Do you want to listen to music online or offline?')
                    onoff = take_command().lower()
                    self.show("You: "+ onoff)
                    if 'online' in onoff:
                        speak('Do you want to listen to music youtube or google?')
                        gy = take_command().lower()
                        self.show("You: "+ gy)
                        if 'gooogle' in gy:
                            # listen on google
                            speak("What song do you want to listen to?")
                            search = take_command().lower()
                            self.show("You: "+ search)
                            url = f"https://www.gooogle.com/search?q={search}"
                            wb.get().open(url)
                            speak(f'Here is your {search} on gooogle')
                        elif 'youtube' in gy:
                            #listen on youtube
                            speak("What song do you want to listen to?")
                            search = take_command().lower()
                            self.show("You: "+ search)
                            url = f"https://www.youtube.com/search?q={search}"
                            wb.get().open(url)
                            speak(f'Here is your {search} on youtbe')
                    elif 'offline' in onoff:
                        # nghe nhac offline
                        speak('Opening file.')
                        ACCEPT_THREAD = Thread(target=play_media)
                        ACCEPT_THREAD.start()
                elif '' in instruction:
                    speak('I am listening')
                else:
                    speak('I did not understand, can you repeat again')
            except:
                speak('Waiting for your response')
            return True
        # set playmedia
        def play_media():
            media = easygui.fileopenbox(title="Choose media to open")
            player = vlc.MediaPlayer(media)
            while True:
                choice = easygui.buttonbox(title="nhóm 1",msg="Press Play to start",choices=["Play","Pause","Stop","New","Exit"])
                print(choice)
                if choice == "Play":
                    player.play()
                elif choice == "Pause":
                    player.pause()
                elif choice == "Stop":
                    player.stop()
                elif choice == "New":
                    media = easygui.fileopenbox(title="Choose media to open")
                    player = vlc.MediaPlayer(media)
                elif choice == "Exit":
                    quit()
                else:
                    break
        # ====Default Start calling
        wellcome()
            # ====To run assistance continuously
        while True:
            if run_command():
                run_command()
            else:
                break
        # ==== Close window
    def close_window(self):
        self.root.quit()
        
# main      
if __name__=="__main__":
    obj = assistance_gui()
    obj.run()
