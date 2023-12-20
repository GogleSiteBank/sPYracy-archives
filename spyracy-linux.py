import youtube_search
import yt_dlp
import os
from tkinter import filedialog
import sys
sys.stdout = open(os.devnull, "w").close()
import pygame
sys.stdout = sys.__stdout__
del os

print("\033[38;2;0;255;100msPYracy   for Linux  is loading...")
version = "BETA Release 2"
import requests
rawApp = "https://raw.githubusercontent.com/GogleSiteBank/sPYracy-TUI/main/.ver"
try:
    rawContent = requests.get(rawApp).text
    if rawContent != version: print("This version of sPYracy is outdated, consider an update here: https://github.com/GogleSiteBank/sPYracy-TUI")
    # nest moment :skull: 
except: print("Couldn't locate sPYracy's latest version, are we offline?  ")
del requests


songs = []
pygame.mixer.init()
songIndex = 0
# load animation keys
keys = []
try:
    f = open("config.spyc", "r")
    for l in f.read().split("Animation: ")[1].split(" SPY")[0]:
        keys.append(l)
    f.close()
except Exception as e:
    f = open("config.spyc", "w")    
    f.write("Animation: #~ SPY\nvExtensions: flac,mp3,ogg SPY")
    f.close()
    keys = ["#", "~"]
    print(e)

debug = True
errors = {
    "wronginput": "Incorrect integer input value!"
}

def search(song : str):
    print("\033[38;2;0;255;100mSearching...")
    unsplit = youtube_search.YoutubeSearch(search_terms=song, max_results=1).to_json()
    
    print("\033[38;2;0;255;100mSong found, grabbing id...")
    beforeid = unsplit.split("id\": \"")[1]
    return beforeid.split("\", \"")[0]

def searchSongs(query: str, maxresults=3):
    unsplit = youtube_search.YoutubeSearch(search_terms=query, max_results=maxresults).to_json()
    for i in range(maxresults):
        print("#%s: %s - ID: %s" % (i+1, unsplit.split("title\": \"")[i + 1].split("\",")[0], unsplit.split("id\": \"")[i+1].split("\", \"")[0]))
        

class Logger:
    def debug(self, msg):
        if not msg.startswith('[debug] '):
            self.info(msg)
    def info(self, msg): pass
    def warning(self, msg): pass
    def error(self,msg): print("\033[38;2;0;255;100mERROR: %s" % msg) 

status = 0
def hook(d):
    global status
    if d["status"] == "downloading":
        if round(float((d['downloaded_bytes'] / d['total_bytes'])) * 100) >= round(status) + 10:
            sec = round(round(float((d['downloaded_bytes'] / d['total_bytes'])) * 100) / 10)
            print("\033[38;2;0;255;100m\033[-%sC" % sec, end="")
            [print(keys[0], end="") for _ in range(sec)]
            print("\033[38;2;0;255;100m\033[%sD" % sec, end="") 
        # print(f"Downloading video... speed: {d['speed']}, time elapsed: {d['elapsed'] / 1000}, percent downloaded {float((d['downloaded_bytes'] / d['total_bytes'])) * 100}%)")

def download(id: str):
    print("\033[38;2;0;255;100m[%s]" % "".join(keys[1] for i in range(10)), end="")
    print("\033[38;2;0;255;100m\033[11D", end="")
    config = {"outtmpl": "%(title)s",
        "format": "bestaudio/best",
        "progress_hooks": [hook],
        "logger": Logger(),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio","preferredcodec": "flac",
                }
                ],
            }

    yt_dlp.YoutubeDL(config).download(id)

def getSongExtensions():
    try:
        with open("config.spyc") as f:
            print(f.readlines())
    except Exception as e:
        print(e)

def executeOption(option):
    global keys, songs, songIndex
    prvmsg = None
    animations = [
        "#~",
        "#-",
        "o-",
        "o~",
    ]
    if option == 1:
        song = input("Song Name: ").encode()
        songID = search(song=song)
        print("\033[38;2;0;255;100mDownloading With ID: %s" % songID)
        download(songID)
        prvmsg = "Downloaded song \"%s\"" % song.decode()
    elif option == 2:
        _songs = []
        _songCount = int(input("Song count (int): "))
        for _ in range(_songCount):
            _songs.append(input("Song #%s: " % str(_ + 1)))
        for _song in _songs:
            download(search(_song))
            print("Song %s/%s downloaded]" % (str(_songs.index(_song) + 1), str(_songCount)))
    elif option == 3:
        searchSongs(input("Song Input: "), int(input("Search Count: ")))
    elif option == 4:
        download(input("ID: "))
    elif option == 5:
        _songs = []
        _songCount = int(input("Song count (int): "))
        for _ in range(_songCount):
            _songs.append(input("ID #%s: " % str(_ + 1)))
        for _song in _songs:
            download(_song)
            print("Song %s/%s downloaded]" % (str(_songs.index(_song) + 1), str(_songCount)))
    elif option == 6:
        pygame.mixer.music.unload()
        pygame.mixer.music.load(songs[songIndex-2])
        pygame.mixer.music.play()
        songIndex -= 2
    elif option == 7:
        pygame.mixer.music.pause()
    elif option == 8:
        pygame.mixer.music.unpause()
    elif option == 9:
        pygame.mixer.music.unload()
        pygame.mixer.music.load(songs[songIndex])
        pygame.mixer.music.play()
        songIndex += 1
    elif option == 10:
        pygame.mixer.music.rewind()
    elif option == 11:
        print("\033[39m") 
        sys.exit()
    elif option == 12:
        pygame.mixer.music.set_pos(float(input("Seek position: ")))

    elif option == 13:
        try:
            pygame.mixer.music.unload()
        except: ...
        songs.clear()
        songIndex = 0
        for file in filedialog.askopenfilenames():
            songs.append(file)
        pygame.mixer.music.load(songs[songIndex])
        for song in songs:
          pygame.mixer.music.queue(song) 
        pygame.mixer.music.play()
        songIndex += 1
    elif option == 14:
        for _index, _song in enumerate(songs) + 1:
            print("#%s - %s" % (_index, _song))
        pygame.mixer.music.unload()
        pygame.mixer.music.load(songs[int(input("\nSong Number: ")) + 1])
    elif option == 15:
        currentAnimation = "[%s]" % ("".join(["".join(keys[0]) for i in range(3)]) + "".join(["".join(keys[1] for i in range(2))]))
        print("\033[38;2;0;255;100m\n== Animation Changer ==\n\nCURRENT: %s\nAnimation 1: [####~~]\nAnimation 2: [###--]\nAnimation 3: [ooo--]\nAnimation 4: [ooo~~]\nAnimation 5: CUSTOM" % currentAnimation)
        newAnimation = int(input("Input Animation (INT): "))
        if 1 > newAnimation or newAnimation > 5:
            print("\033[38;2;0;255;100mInvalid Option") 
        else:
            if 5 >= newAnimation >= 1: 
                f = open("config.spyc", "r+")
                content = f.read()
                getAnimation = content.split("Animation: ")[1].split(" SPY")[0]
                f.seek(0)
                f.truncate()
                keys.clear()
                loadingAnimation = ""
                try:
                    for l in animations[newAnimation-1]:
                        keys.append(l)
                    loadingAnimation = animations[newAnimation-1]
                except:
                    if debug: ...
                if newAnimation == 5:
                    loadingAnimation = input("First part of animation (???~~): ") + input("Second part of animation (###??): ")
                    keys.clear()
                    for l in loadingAnimation:
                        keys.append(l)
                f.write(content.replace("Animation: " + getAnimation + " SPY", "Animation: %s SPY" % loadingAnimation))
                print("\033[38;2;0;255;100mAnimation has been changed to: [%s]" % ("".join(["".join(keys[0]) for i in range(3)]) + "".join(["".join(keys[1] for i in range(2))])))
                f.close()  
    elif option == 16:
        print(open("config.spyc", "r").read())
    elif option == 17:
        with open("config.spyc", "r") as f:
            print(f.read().split("vExtensions: ")[1].split("SPY")[0])
    elif option == 18:
        print(pygame.mixer.music.get_busy())
    elif option == 19:
        pygame.mixer.music.load("Anthem.flac")
        pygame.mixer.music.play()
    elif option == 20:
        print(len(songs))
    elif option == 21:
        for _numeration, _song in enumerate(songs):
            print("#%s: %s" % (_numeration + 1, _song))
    elif option == 22:
        previewOptions()
    else:
        print("\033[38;2;0;255;100mThis option does not exist!")
    previewOptions(prvmsg)

def previewOptions(previewmessage=None):
    print("\033[38;2;0;255;100m\nsPYracy   for Linux   - %s" % version)
    DownSearch = [
        "Download Song   (1)",
        "Download multiple songs   (2)",
        "Search for Songs   (3)",
        "Download Song VIA ID   (4)",
        "Download Multiple Songs VIA IDs   (5)",
        "Back Home   (22)"
    ]
    Controls = [
        "Reverse   (6)",
        "Pause  (7)",
        "Resume  (8)",
        "Skip   (9)" ,
        "Restart Song   (10)",
        "Exit   (11)",
        "Seek   (12)",
        "Queue Songs   (13)",
        "Play Song From List (14)  ",
        "Back Home   (22) "
    ]
    Debugs = [
        "Change Download Animation   (15)",
        "Read config.spyc   (16)",
        "Read valid song extensions from config.spyc   (17)",
        "Get business of pygame   (18)",
        "Play test audio   (19)",
        "Get Songs len   (20)",
        "Get playlist    (21)",
        "Back Home   (22)"
    ]
    subSections = [
        "Downloading/Searching   ",
        "Controls     ",
        "Debugging "
    ]
    intToSection = {
        1 : DownSearch,
        2: Controls,
        3: Debugs
    }
    if previewmessage != None:
        print("\033[38;2;0;255;100m\n\n")
        print(previewmessage)
    # [print("\033[38;2;0;255;100mOption #%s - %s" % (_ + 1, __)) for _, __ in enumerate(options)]
    for _x, section in enumerate(subSections): print("  %s: %s" % (_x + 1, section))
    print("\n", end="")
    print("\n".join(intToSection[int(input("Input Section (int): "))]))
  
    executeOption(int(input("Input Option (int): ")))
print("\033[38;2;0;255;100msPYracy has completed loading\n")
print("\033[38;2;0;255;100m⢳⢕⢇⢗⢕⢇⢗⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⠕⡕⢕⠕⡕⢕⠕⡕⢕⠕⡕⢕⢕⠕⡕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⡕⡵⡱⡣⡳⡱⣣⢳⡹⡜⣎⢗⢵\n⢇⢗⢝⢜⢕⢕⡕⡕⡕⡕⡕⡕⡕⢕⢅⢇⢎⢆⢇⠇⡇⢇⢣⠣⡣⢣⠣⡣⢣⢣⢱⠱⡱⡑⡕⡜⡔⡕⡜⡔⢕⢱⢸⢰⠱⡡⡣⡱⡡⡣⡱⣱⣵⣷⣷⣧⡇⡇⡇⡇⡇⡇⡇⡇⡇⡗⡝⡜⡎⡮⣪⢺⢜⢎⢧\n⡸⡱⡹⡸⡱⡱⡱⡱⡱⡱⡑⡕⡜⢜⢌⢆⢇⠎⡆⢇⢣⠣⡃⡇⡣⡃⡇⡣⡣⡱⡸⡘⡌⡎⡪⡢⢣⠪⡢⢣⠣⡣⡱⡪⡪⢪⢸⢨⢪⠸⣸⣳⣿⣿⣿⣿⣿⡎⡜⡌⡎⢎⢎⢎⢮⢪⢪⢪⢺⢸⢜⢎⢮⢳⢹\n⢮⢪⢣⢣⢣⢣⠣⡣⡱⡸⡘⡌⣎⣮⣮⣶⣷⣷⣷⣷⣷⣧⣧⣕⢅⢇⢕⠕⡜⢔⢅⢇⢕⢅⠇⡎⡪⡊⡎⡪⡊⡎⢜⢻⣎⢎⠆⡇⢎⢎⢺⡏⡎⡽⡇⡝⣏⢇⢇⢕⠕⡕⣅⣷⢏⢎⢎⢎⢎⢎⢮⢺⢸⢪⡣\n⡣⡣⡣⡣⡣⡣⡣⢣⠣⣱⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣔⣕⢱⢑⠕⡜⢔⢕⢱⢑⢅⢇⢕⢅⢇⢎⢎⢪⢹⣷⣕⢕⢱⠡⡝⡻⣿⣭⣻⡾⡟⡢⡣⢪⢊⣮⣾⡓⡕⢕⢱⢱⢱⢱⢱⢱⢕⢇⢗\n⡜⡜⡜⡜⡜⡌⡎⣮⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⡪⡊⡎⡪⢢⢣⠱⡡⡣⢪⠢⡣⢪⢸⢨⢢⡙⡻⣷⣵⡑⡕⢽⣚⣻⠫⣺⢜⢌⢎⣮⣾⢟⢕⢜⠜⡜⢜⢜⢸⢸⢸⢸⢸⢜⢎\n⢜⢜⢜⢜⢔⢵⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣜⢌⢎⢪⠢⡣⢣⠪⡊⡎⡪⡊⡆⢇⢕⠜⡜⢜⢻⣯⡪⣎⡻⠶⡟⢇⡧⣞⡿⡻⡱⡑⡕⢜⢜⢸⢘⢌⢎⠎⡎⡎⡎⡎⡮\n⢇⢇⢇⢕⢬⣿⣿⣿⡿⡿⡻⡛⡟⡫⡫⡹⡩⡫⡛⡻⡛⡟⡿⢿⣿⣿⣿⣿⣿⣿⣿⣎⢎⠆⡇⡣⡃⡇⡣⡱⡡⡣⡱⡑⡅⡇⡝⡕⡱⡰⣙⡳⢭⡺⡜⣕⢏⢇⢣⢱⢪⢪⢊⢎⢢⢣⢱⢑⢅⢇⢣⠣⡣⡣⡣\n⢕⢕⢕⢱⣿⣿⣿⣿⢸⢨⢢⢣⢱⣱⣸⣰⣱⣨⣪⡸⡨⡢⢣⠣⡊⡎⡛⠿⣿⣿⣿⣿⡜⡜⡌⢎⢪⢸⢨⠪⡢⢣⠪⡊⡎⡪⡢⡣⡣⢝⢢⢓⢕⢜⢜⢪⠪⡕⡕⡕⡕⢕⢱⢡⢣⢱⠸⡨⡪⡸⡨⡪⢪⢪⢪\n⡪⡢⡣⣹⣿⣿⣿⣿⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣵⣑⢕⢕⢢⣿⣿⣿⣯⢢⠣⡣⢣⠱⡡⡣⡃⡇⡣⣣⣧⣧⣮⣊⢮⣎⢎⢪⡦⡣⡪⡊⡎⡪⡸⡨⡪⢪⢊⢎⢢⢃⢇⢕⢜⠔⡕⢜⠜⡔⡕\n⡣⡱⡑⣿⣿⣿⣿⣿⣿⢻⢙⢍⢇⠎⡆⡕⡜⢔⢱⢩⠫⡛⡻⠿⣿⣿⣿⣾⣾⣿⣿⣿⣿⢕⢕⢱⢑⢕⠕⡜⣾⡻⢗⢼⣿⣢⣹⡿⡨⡻⣾⡟⡕⣿⡿⢇⢻⣛⢷⣕⣼⡞⡟⡷⡹⣧⢣⣿⢱⢑⢕⢱⢑⢕⢕\n⠪⡊⡎⣿⣿⣿⣿⣿⣿⣼⣼⣬⣶⣷⣷⣾⣾⣾⣾⣦⣧⣣⡣⡹⡨⢍⠿⣿⣿⣿⣿⣿⣿⢕⢇⢇⢕⢅⢇⢕⣭⣻⡷⣺⣿⡙⡝⢜⢌⢎⣿⢪⠪⣿⣏⠪⣿⣹⣽⡧⡻⣧⣣⡮⣘⢻⣽⢇⢣⢱⢡⢣⢱⢱⢱\n⡪⡪⡪⢺⣿⣿⣿⣿⣿⣿⡿⢿⠿⢟⢻⢛⢟⢻⢻⠿⣿⣿⣿⣿⣾⣬⣾⣿⣿⣿⣿⣿⡿⡱⡝⣜⢔⢕⠜⡌⢎⢕⢕⢢⢢⢣⠪⡪⢢⠣⡪⡢⢣⠣⡒⡍⢎⢕⠜⡌⢎⢪⢙⢌⠶⢿⢫⠪⡊⡆⡇⡕⡕⢕⢕\n⡸⡨⡪⡪⣿⣿⣿⣿⣿⣇⣇⣣⣭⣮⣮⣮⣼⣬⣦⣓⣔⠬⡹⡹⠿⣿⣿⣿⣿⣿⣿⣿⢏⢞⡜⡎⡮⡢⡣⢣⠣⡱⡸⢰⠱⡸⡘⡜⡌⡎⢆⢇⢣⢃⢇⢕⠕⡅⢇⢣⠣⡃⡇⡕⢕⢕⢱⢑⢕⠕⣼⣜⢜⢜⢜\n⡜⡜⡌⡎⣚⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣼⣸⣿⣿⣿⣿⣿⣿⢯⢫⢕⢝⡜⡵⡱⡕⢕⢍⢎⢪⢱⢩⠪⡊⡎⡪⢪⠱⡑⡕⢕⢱⢑⢍⢎⢕⠕⡍⡎⡪⡪⡱⡑⡕⢕⠕⡍⣛⢏⢎⢎⢎\n⡪⡪⡪⡊⡆⢞⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡫⣣⢳⢱⡣⡳⡱⡣⡫⡪⡢⢣⠱⡑⡜⢜⢌⢎⢪⢊⢎⢪⣾⢿⣾⡜⡔⢕⠜⣜⢌⢎⢜⠔⡕⢜⢸⢘⢜⢜⢔⢕⢕⢕⢕\n⡸⡸⡸⡘⡜⡜⡌⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⢱⢕⢵⢱⢣⢳⢹⡸⣱⢹⡸⡸⡘⡜⢜⢸⢨⠪⡣⢣⠱⡑⠽⣿⣽⣿⢗⢕⢱⠱⡸⡑⡕⢜⢸⢘⢜⢌⢎⢆⢇⢕⢕⢕⢕⢝\n⡎⡎⡎⡎⡎⡆⡇⡎⡎⡟⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⢏⢗⢕⢇⢗⢵⢹⢜⢕⢵⡱⡕⡵⣱⢹⡸⡘⡜⡌⡆⡇⢇⢣⠣⡣⡋⡎⢝⢱⠱⡸⡰⡱⡑⡕⢜⢜⢌⠎⡆⢇⢕⢜⢜⢜⢜⢜⢜⢎\n⢎⢮⢪⢪⢪⢊⢆⢇⢎⢎⢮⢪⡫⡻⡻⢿⢿⢿⢿⢿⢿⢻⢻⡹⡪⡣⡳⡹⣸⢱⢝⢜⢎⢮⢣⢇⢧⢳⢹⢸⢜⢼⢸⢰⠱⡘⡜⡸⡨⡪⡢⢣⠪⡪⡊⡎⢆⢣⢪⢸⢨⠪⡢⡃⡇⡣⡣⡣⡣⡣⡣⡣⡣⡳⡱\n⡕⣇⢧⢣⢣⢣⢣⢣⢱⢸⠸⡸⡜⡎⡮⡣⡣⡇⡧⣣⢳⢹⡸⡜⡎⣇⢏⢞⢜⢎⡎⡧⡫⣪⢺⡸⡪⣪⢣⡳⡱⡣⡳⡱⡱⡑⡕⡱⡸⢰⢑⢕⢱⢡⠣⡪⡪⡊⡆⢇⢕⠕⡅⡇⡣⡣⡣⡪⡪⡪⡪⡪⣪⢣⡫\n⡱⡕⡵⡱⡕⣕⢕⢕⢕⢕⢕⢕⢕⢝⡜⡎⣇⢏⢮⢪⢎⢇⢧⢣⡫⣪⢪⡣⣫⢪⢎⢞⡜⣎⢮⢪⡺⡸⣱⢱⡹⡜⣕⢝⡜⡌⡎⡜⡌⡎⡪⡸⡨⡢⡣⡣⢪⢪⢸⢸⢰⢱⠱⣑⢕⢕⢜⢜⢜⢜⢜⢎⢮⡪⡺\n⡕⣝⢜⡎⡮⡪⣪⢪⢪⢪⢪⢪⢪⢪⡪⡺⡸⡪⡣⡳⡱⡝⣜⢕⡕⡵⡱⣕⢕⢇⡏⡮⡪⡎⣎⢇⢧⢫⡪⡎⡮⡪⡎⡮⡪⡎⡎⡆⡇⡕⢕⢅⢇⢕⢜⠜⡜⢔⢕⢕⢜⢜⢜⢔⢕⢕⢕⢕⢵⢹⡸⡱⣕⢵⢝")

previewOptions()