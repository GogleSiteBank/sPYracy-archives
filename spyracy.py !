import youtube_search
import yt_dlp
import os; os.system("")
import time

errors = {
    "wronginput": "Incorrect integer input value!"
}

def search(song : str):
    print("Searching...")
    unsplit = youtube_search.YoutubeSearch(search_terms=song, max_results=1).to_json()
    print("Song found, grabbing id...")
    beforeid = unsplit.split("id\": \"")[1]
    return beforeid.split("\", \"")[0]

class Logger:
    def debug(self, msg):
        if msg.startswith('[debug] '):
            pass
        else:
            self.info(msg)
    def info(self, msg): pass
    def warning(self, msg): pass
    def error(self,msg): print("ERROR: %s" % msg) 

status = 0
def hook(d):
    global status
    if d["status"] == "downloading":

        if round(float((d['downloaded_bytes'] / d['total_bytes'])) * 100) >= round(status) + 10:
            sec = round(round(float((d['downloaded_bytes'] / d['total_bytes'])) * 100) / 10)
            print("\033[-%sC" % sec, end="")
            [print("#", end="") for _ in range(sec)]
            print("\033[%sD" % sec, end="")

    
        # print(f"Downloading video... speed: {d['speed']}, time elapsed: {d['elapsed'] / 1000}, percent downloaded {float((d['downloaded_bytes'] / d['total_bytes'])) * 100}%)")

def download(id: str):
    print("[~~~~~~~~~~]", end="")
    print("\033[11D", end="")
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


def executeOption(option):
    prvmsg = None
    if option == 1:
        song = input("Song Name: ").encode()
        download(search(song=song))
        prvmsg = "Downloaded song \"%s\"" % song.decode()
    elif option == 2:
        songs = []
        for index, file in enumerate(os.listdir()):
            print(f"#{index}: {file}")
            songs.append(file)
        songtoplay = songs[0]
    else:
        print("Incorrect Value!")
        return
    previewOptions(prvmsg)

def raiseError(error):
    print("\n[sPYracy - an error has occured]\n")
    print("Error: %s" % error)

def previewOptions(previewmessage=None):
    options = [
        "Download Song",
        "Play Song"
    ]
    print("\x1B[2J\x1B[H", end="")
    if previewmessage != None:
        print(previewmessage)
    [print("Option #%s - %s" % (_ + 1, __)) for _, __ in enumerate(options)]
    try:
        grabInput = int(input("Input Option (int): "))
        if grabInput > 2: raiseError("Invalid integer input")
        executeOption(grabInput)
    except:
        raiseError("Invalid integer input")

# input previewOptions
previewOptions()
