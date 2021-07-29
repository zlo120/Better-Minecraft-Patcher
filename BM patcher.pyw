import tkinter
from typing import Sized
import dropbox
import os
from dropbox.dropbox_client import BadInputError
import shutil
from zipfile import ZipFile
from tkinter import *
from PIL import Image, ImageTk
import random
import threading
from time import sleep
import ctypes
from tkinter import messagebox
import datetime
import csv

if random.randint(0,1) == 0:
    isDayMode = True
else:
    isDayMode = False

threads = 0

cancel = False

patch = []
needToRemove = []

try:
    with open ("data.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            for mod in row:
                if mod.startswith("!") or mod.startswith(" !"):
                    removeMod = str(mod).replace("!", "")
                    needToRemove.append(removeMod)
                else:
                    patch.append(mod)
        
        file.close()
except:
    messagebox.showinfo("Error!", "You need to have data.csv in the same folder as this program. You can find it on the discord, put it in the same folder as this application, then restart this.")
    exit()

print("PATCH", patch)
print("NEED TO REMOVE", needToRemove)


directory = os.path.expanduser("~\\curseforge\\minecraft\\Instances\\Better Minecraft [FORGE]\\mods\\")
PatcherAssetsDir = directory + "PatcherAssets\\"
patches = ["PatchBM.zip"]
TOKEN = '0UntGWELjUYAAAAAAAAAAZx_gLt8svNnDrFgAvvetYEjPALGY5gCxmGuXH18QyNI'
dbx = dropbox.Dropbox(TOKEN)

list_of_mods = []

class settingsMenu():
    def __init__(self):
        self.window = Tk()
        self.window.title("Settings")
        iconImage = PhotoImage(file='PatcherAssetsDir\\settings.gif')
        self.window.tk.call('wm', 'iconphoto', self.window._w, iconImage)
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()
        width = round(width / 1.5)
        height = round(height / 1.3)

        self.window.geometry(str(width) + "x" + str(height))

        self.window.mainloop()

class LoadAnimation(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.day = []
        self.night = []
        

    def run(self):
        if not os.path.exists(PatcherAssetsDir + "\\dayFrames"):
            os.mkdir(PatcherAssetsDir + "dayFrames")
            # ctypes.windll.kernel32.SetFileAttributesW("dayFrames", 2)
        
        if not os.path.exists(PatcherAssetsDir + "\\nightFrames"):
            os.mkdir("Assets\\nightFrames")
            # ctypes.windll.kernel32.SetFileAttributesW("nightFrames", 2)
        
        dayPath = PatcherAssetsDir  + "dayFrames"
        nightPath = PatcherAssetsDir  + "nightFrames"
        self.day_num_files = len([f for f in os.listdir(dayPath)if os.path.isfile(os.path.join(dayPath, f))])
        self.night_num_files = len([f for f in os.listdir(nightPath)if os.path.isfile(os.path.join(nightPath, f))])

        for file in range(self.day_num_files):
            image_o = Image.open(PatcherAssetsDir + f"dayFrames\\dayFrame({file+1}).png")
            self.day.append(image_o)

        for file in range(self.night_num_files):
            image_o = Image.open(PatcherAssetsDir +  f"nightFrames\\nightFrame({file+1}).png")
            self.night.append(image_o)

    def returnAnimation(self):
        return (self.day, self.night)

class Installer(threading.Thread):
    def __init__(self, label, randnum):
        threading.Thread.__init__(self)
        self.daemon = True
        self.label = label
        self.random_num = randnum

        self.pComplete = False
        
        # self.label.configure(text = "Installing... please wait...")

    def run(self):
        jokes = [
            [("Starting", 3), ("Downloading some files", 5), ("Looking through some of your files", 5), ("Woah that's a lot of porn", 4), ("Oh my, do I have to report this to the police?", 4), 
            ("Nah its all good", 3), ("Just tell me where you got it from", 5), ("Yo I'm just joking", 3), ("The installation should be finalising", 1)],

            [("Starting", 3), ("Downloading some files", 5), ("This might take a little bit of time", 5), 
            ("Know any jokes?", 4), ("Yeah me neither", 4), 
            ("Well this is awkward", 3), ("Did you hear how Joe caught Ligma", 5), ("I hope he gets better", 3), ("The installation should be finalising", 1)],

            [("Starting", 3), ("Downloading some files", 5), ("Snooping around in your files", 5), 
            ("Oh wow so you download your porn?", 4), ("Interesting", 2), 
            ("You're into some weird stuff", 3), ("Okay, okay, okay", 3), ("No judgement", 3), ("The installation should be finalising", 1)],

            [("Starting", 3), ("Downloading some files", 5), ("Looking through your emails", 6), 
            ("Dude how many times are you gonna fall for these scams", 6), ("Please just save your money", 4), 
            ("Okay buddy", 3), ("Alright fine", 3), ("Sure he is", 3), ("The installation should be finalising", 1)]
            ]

        loader = Loader(self.label, jokes[random.randint(0,3)])       
        loader.start()
        
        for dirpath, dirnames, filenames in os.walk(directory):
            for f in filenames:
                if ".jar" in f:
                    list_of_mods.append(str(os.path.join(f)))

        try:
            checkPatch(patch)
            self.pComplete = True
        except MissingMods:
            installPatch(patches[0])

        checkToRemove(patch)
        print("Check successful")  

        loader.stop()

        if self.pComplete:
            self.label.configure(text = "YOU'RE ALREADY UP TO DATE!")
        else:
            self.label.configure(text = "DONE!")
            messagebox.showinfo("Done!", "Your installation is complete!\nYou may see an extra file called 'BMPatch.zip', you can delete this file.")

class Loader(threading.Thread):

    def __init__(self, label, messages, place = []):
        threading.Thread.__init__(self)
        self.daemon = True
        self.label = label
        self.messages = messages
        self.place = place

    def run(self):
        for msg, time in self.messages:

            if (msg, time) == self.messages[-1]:

                self.label.configure(text = msg + ".")
                while True:
                    self.label.configure(text = msg + ".")
                    sleep(1.5)
                    self.label.configure(text = msg + "..")
                    sleep(1.5)
                    self.label.configure(text = msg + "...")
                    sleep(3)

            self.label.configure(text = msg + ".")
            sleep(time / 3)
            self.label.configure(text = msg + "..")
            sleep(time / 3)
            self.label.configure(text = msg + "...")
            sleep(time / 3)

    def get_id(self):
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
   
    def stop(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)

class needToRemoveMod(Exception):
    pass

class MissingMods(Exception):
    pass
    
class backgroundAnimator(threading.Thread):
    def __init__(self, isDayMode, frames, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.daemon = True
        self.killed = False
        self.isDayMode = isDayMode
        self.dayFrames = frames[0]
        self.nightFrames = frames[1]

    def run(self):
        global threads
        x = datetime.datetime.now()
        print(str(x) + " Thread starting")
        threads += 1
        if threads > 1:
            self.stop(True)

        global cancel        
        if self.isDayMode:
            while True:
                for image in self.dayFrames:
                    if cancel:
                        self.stop()
                        break
                    self.img = image.resize((width, height))
                    bg_image = ImageTk.PhotoImage(self.img)
                    bg.configure(image = bg_image)
                    bg.image = bg_image 
                    sleep(0.025)

        if not self.isDayMode:
            while True:
                for image in self.nightFrames:
                    if cancel:
                        self.stop()
                        break
                    self.img = image.resize((width, height))
                    bg_image = ImageTk.PhotoImage(self.img)
                    bg.configure(image = bg_image)
                    bg.image = bg_image 
                    sleep(0.075)

    def get_id(self):
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def stop(self, tryAgain = False):
        global threads
        x = datetime.datetime.now()
        print(str(x) + " Thread closing")
        threads -= 1
        self.cancel = True
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)

class installingAssets(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

    def run(self):
        if not os.path.exists(PatcherAssetsDir):
            os.mkdir(PatcherAssetsDir)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        try:
            print("Downloading patcher assets")
            with open("BMPatcherAssets.zip", "wb") as f:
                ctypes.windll.kernel32.SetFileAttributesW("/" + "BMPatcherAssets.zip", 2)
                metadata, res = dbx.files_download("/" + "BMPatcherAssets.zip")
                f.write(res.content)

        except BadInputError:
            print("Need better token")

        # Moving the patch
        print("Moving patcher assets")
        original = "BMPatcherAssets.zip"
        target = PatcherAssetsDir + "BMPatcherAssets.zip"
        shutil.copy(original, target)

        # Deleting from the mods folder
        print("Deleting local patcher assets")
        if os.path.exists(dir_path + "\\" + "BMPatcherAssets.zip"):
            os.remove(dir_path + "\\"  + "BMPatcherAssets.zip")

        # Unzipping the patch
        print("Unzipping patcher assets")
        with ZipFile(PatcherAssetsDir + "BMPatcherAssets.zip", 'r') as zipObj:
            # Extract all the contents of zip file in current directory
            zipObj.extractall(PatcherAssetsDir)

        print("Deleting patcher assets")
        # Deleting from the mods folder
        if os.path.exists(PatcherAssetsDir + "BMPatcherAssets.zip"):
            os.remove(PatcherAssetsDir + "BMPatcherAssets.zip")

def checkToRemove(Patch):
    print(list_of_mods)
    for mod in needToRemove:
        print(mod)
        if mod in list_of_mods:
            if os.path.exists(directory + mod):
                os.remove(directory + mod)

def checkPatch(Patch):
    success = 0
            
    for mod in Patch:
        
        if mod == Patch[-1]:
            if mod in list_of_mods:
                success += 1
                if success != len(Patch):
                    raise MissingMods
                    break
        if mod in list_of_mods:
            success += 1
            continue

        elif mod not in list_of_mods:
            raise MissingMods

def installPatch(Patch):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # Downloading the patch
    try:
        with open(Patch, "wb") as f:
            ctypes.windll.kernel32.SetFileAttributesW("/" + Patch, 2)
            metadata, res = dbx.files_download("/" + "BMpatch.zip")
            f.write(res.content)

    except BadInputError:
        print("Need better token")

    # Moving the patch
    original = Patch
    target = str(directory + Patch)
    shutil.copy(original, target)

    # Deleting from the mods folder
    if os.path.exists(dir_path + "\\" + Patch):
        os.remove(dir_path + "\\"  + Patch)

    # Unzipping the patch
    with ZipFile(directory + Patch, 'r') as zipObj:
        # Extract all the contents of zip file in current directory
        zipObj.extractall(directory)

    # Deleting from the mods folder
    if os.path.exists(directory + Patch):
        os.remove(directory + Patch)

def initiateInstallation():

    start_button['state'] = DISABLED
    
    installer = Installer(start_button, random.randint(0,3))
    installer.start()
 
def changeTheme():
    global frames
    global isDayMode
    global cancel

    cancel = True

    sleep(0.10)
    
    if isDayMode:
        
        sun_ = Image.open(PatcherAssetsDir + "\\sun.gif")
        length_of_button = int(height * 0.0651041667)
        resized_sun = sun_.resize((length_of_button,length_of_button))
        sun = ImageTk.PhotoImage(resized_sun)

        theme.configure(image = sun)
        theme.image = sun

        settings_ = Image.open(PatcherAssetsDir + "\\night_settings.gif")
        resized_settings = settings_.resize((length_of_button,length_of_button))
        settings = ImageTk.PhotoImage(resized_settings)
        settings_button.configure(image=settings)
        settings_button.image = settings
        
        img = Image.open(PatcherAssetsDir + "\\night_theme.gif")
        img2 = img.resize((width, height))
        bg_image = ImageTk.PhotoImage(img2)
        bg.configure(image = bg_image)
        bg.image = bg_image   

        isDayMode = False        
    
    else:

        moon_ = Image.open(PatcherAssetsDir + "\\moon.gif")
        length_of_button = int(height * 0.0651041667)
        resized_moon = moon_.resize((length_of_button,length_of_button))
        moon = ImageTk.PhotoImage(resized_moon)

        theme.configure(image = moon)
        theme.image = moon

        settings_ = Image.open(PatcherAssetsDir + "\\day_settings.gif")
        resized_settings = settings_.resize((length_of_button,length_of_button))
        settings = ImageTk.PhotoImage(resized_settings)
        settings_button.configure(image=settings)
        settings_button.image = settings

        img = Image.open(PatcherAssetsDir + "\\day_theme.gif")
        img2 = img.resize((width, height))
        bg_image = ImageTk.PhotoImage(img2)
        bg.configure(image = bg_image)
        bg.image = bg_image

        isDayMode = True

    cancel = False
    new_animator = backgroundAnimator(isDayMode, frames)
    new_animator.start()

def openSettings():
    
    messagebox.showinfo("Ain't nothing here", "I haven't added any functionality to this button yet. Check back later in future versions.")

def initialiseAnimation():
    # Loading in the gif frames for bg animation
    animation.start()

def on_closing():
    day_animator.stop()
    night_animator.stop()
    window.quit()
    window.destroy()

# Animation object
animation = LoadAnimation()

def closeIniter():
    instantiateMessage.stop()
    initer.destroy()

def afterIniter():
    assetsDownloader.start()
    instantiateMessage.start()

# Starter window initialisation
if not os.path.exists(PatcherAssetsDir):
    initer = Tk()
    initer.title("Welcome")
    initer.overrideredirect(1)
    initer.eval('tk::PlaceWindow . center')
    # Setting geometry of initer
    width = initer.winfo_screenwidth()
    height = initer.winfo_screenheight()
    width = round(width / 4)
    height = round(height / 3.5)
    initer.geometry(str(width) + "x" + str(height))
    initer.resizable(False, False)
    waitMessage = Label(initer, text = "", font = ("DengXian", 15))
    waitMessage.place(x = width / 5, y = height / 2.3)

    instantiateMessage = Loader(waitMessage, [("Hey there welcome to Patcher", 2), ("Please wait while we install some assets", 1.5)])
    assetsDownloader = installingAssets()
    
    initer.after(ms = 1, func = afterIniter)
    initer.after(ms = 10000, func=closeIniter)
    initer.mainloop()

dayFrames, nightFrames = animation.returnAnimation()
frames = (dayFrames, nightFrames)
day_animator = backgroundAnimator(isDayMode, frames)
night_animator = backgroundAnimator(isDayMode, frames)

# Window initialisation
window = Tk()
window.after(ms = 1, func=initialiseAnimation)
window.title("Better Minecraft Patcher made by Zachary Lo")
img = PhotoImage(file=PatcherAssetsDir + 'icon.png')
window.tk.call('wm', 'iconphoto', window._w, img)
window.resizable(False, False)
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
# Setting geometry of window
width = round(width / 1.6)
height = round(height / 1.5)
window.geometry(str(width) + "x" + str(height))
window.protocol("WM_DELETE_WINDOW", on_closing)

# Loading in gifs for the day/night buttons
moon_ = Image.open(PatcherAssetsDir + "\\moon.gif")
length_of_button = int(height * 0.0651041667)
resized_moon = moon_.resize((length_of_button,length_of_button))
moon = ImageTk.PhotoImage(resized_moon)

sun_ = Image.open(PatcherAssetsDir + "\\sun.gif")
resized_sun = sun_.resize((length_of_button,length_of_button))
sun = ImageTk.PhotoImage(resized_sun)

# Setting background and button images depending on what random mode the client starts on
if isDayMode:
    settings_ = Image.open(PatcherAssetsDir + "\\day_settings.gif")
    resized_settings = settings_.resize((length_of_button,length_of_button))
    settings = ImageTk.PhotoImage(resized_settings)

    img = Image.open(PatcherAssetsDir + "\\day_theme.gif")
    resized_image = img.resize((width, height))
    bg_image = ImageTk.PhotoImage(resized_image)
    bg = Label(window, image = bg_image)
    bg.place(x=0,y=0, relwidth=1, relheight = 1)

    theme = Button(window, image = moon, border = 0, borderwidth = 0, highlightthickness = 0, bd = 0, command = changeTheme)
    
else:
    img = Image.open(PatcherAssetsDir + "\\night_theme.gif")
    resized_image = img.resize((width, height))
    bg_image = ImageTk.PhotoImage(resized_image)

    settings_ = Image.open(PatcherAssetsDir + "\\night_settings.gif")
    resized_settings = settings_.resize((length_of_button,length_of_button))
    settings = ImageTk.PhotoImage(resized_settings)

    bg = Label(window, image = bg_image)
    bg.place(x=0,y=0, relwidth=1, relheight = 1)

    theme = Button(window, image = sun, border = 0, borderwidth = 0, highlightthickness = 0, bd = 0, command = changeTheme)

# Placing the widgets on screen (above bg)
settings_button = Button(window, image = settings, border = 0, borderwidth = 0, highlightthickness = 0, bd = 0, command = openSettings)
start_button = Button(window, font = ("DengXian", 15), text = "Install Patch", command = initiateInstallation, width = int(width / 25))
start_button.place(x = width - width / 1.40, y = height - height / 1.05)
theme.place(x =  width - width /16.5, y = height - height / 10)
settings_button.place(x = width /50, y = height - height / 10)

def checkAnim():
    print(len(animation.returnAnimation()[0]), len(animation.returnAnimation()[1]))

def startAnimation():

    global isDayMode
    if isDayMode:
        day_animator.start()
    else:
        night_animator.start()
        
window.after(ms = 10, func = startAnimation)

window.mainloop()