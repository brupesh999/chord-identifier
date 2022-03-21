"""
    Description: This is the final project (imports chordIdentifier)
    Author: Bhadra Rupesh (used inspiration for piano GUI from online source because
    I hadn't used tkinter before but I modified a lot of the code and understand it)
    Date: 2021
"""




"""

Example chords to try (try other chords too):

Notes to play: C1, D#1, F#1, A2
Notes to select: C1, Eb1, Gb1, Bbb2
Should output: C°7

Notes to play: F1, G1, C2, D2
Notes to select: no need to select (same notes)
Should output: F sus2 6

Notes to play: D1, F1, G1, C2 (rearranged version of previous)
Notes to select: no need to select (same notes)
Should output: Dm7 add4

"""




#imports tkinter
from tkinter import Tk, Frame, BOTH, Label, PhotoImage

#imports the module for playing audio
import simpleaudio as sa

# necessary for simultaneous button clicking and audio playing
import time as t
from _thread import start_new_thread
from tkinter import *

# my previous program
import chordIdentifier as chord

# the song file will basically contain the notes that the user pressed
file = open('songs/song.txt', 'w')
file.close()

# global variables (will use later)
recording = False
noteDrop = []
noteOptionX = 0
noteOptionY = 300
selectedNote = ['']*20
noteCount = 0
result1 = ''
result2 = ''

# creates a state for the key with the image specified (there are four different types:
# white key, black key, and red and green for record and play) showing that is is pressed
def label_pressed(event):
    if len(event.widget.name) == 2:
        img = 'pictures/white_key_pressed.gif'
    elif len(event.widget.name) == 3:
        img = 'pictures/black_key_pressed.gif'
    elif event.widget.name == 'red_button':
        img = 'pictures/red_button_pressed.gif'
    else:
        img = 'pictures/green_button_pressed.gif'
    key_img = PhotoImage(file=img)
    event.widget.configure(image=key_img)
    event.widget.image = key_img

# clear note options when the user tries a new chord
def clear_note_options(event):
    global noteDrop
    global result1
    global result2
    global noteOptionX
    global noteOptionY
    global selectedNote
    global noteCount

    for drop in noteDrop:
        drop.destroy()
    noteOptionX = 0
    noteOptionY = 300
    result1.destroy()
    result2.destroy()
    noteCount = 0

# adds the dropdown menus for the enharmonic notes
def add_note_option(event, note):
    global noteOptionX
    global noteOptionY
    global selectedNote
    global noteCount
    global noteDrop

    # dropdown menu options
    options = chord.returnSelectOptions(note)

    # datatype of menu text
    selectedNote[noteCount] = StringVar()

    # initial menu text
    selectedNote[noteCount].set( note )

    # Create dropdown menu
    drop = OptionMenu( event.widget.root , selectedNote[noteCount] , *options )
    drop.place(x=noteOptionX, y=noteOptionY)
    noteDrop.append(drop)
    noteCount += 1
    if (noteOptionX) < (650):
        noteOptionX += 55
    else:
        noteOptionX = 0
        noteOptionY += 30

# function to play the wav files for the keys the user has pressed after they submit their chord
# also uses chordIdentifier to show result
def play(file_name, event):
    global result1
    global result2
    notes = []
    selNotes = []
    index = 0

    if result1 != '':
        result1.destroy()
        result2.destroy()

    # this is where I access the notes from the song file that the user pressed so I can play their notes back to them
    song_file = open(file_name, 'r')
    first_line = song_file.readline().split()
    note = first_line[0]
    notes.append(note)
    selNotes.append(selectedNote[index].get())
    index += 1
    for line in song_file:
        wave_obj = sa.WaveObject.from_wave_file('sounds/' + note + '.wav')
        wave_obj.play()
        line_elements = line.split()
        note = line_elements[0]
        notes.append(note)
        selNotes.append(selectedNote[index].get())
        index += 1
        t.sleep(.05)

    print("Input Notes      : ",notes)
    print("Selected Notes   : ",selNotes)
    print('\n')

    wave_obj = sa.WaveObject.from_wave_file('sounds/' + note + '.wav')
    wave_obj.play()

    # this is where I import my previous program
    try:
        mergedNoteChord = chord.mergeChord(selNotes)
        res1 = chord.findChord(mergedNoteChord)[0]
        res2 = chord.findChord(mergedNoteChord)[1]
    except:
        res1 = False
        res2 = False

    result1Str = StringVar()
    result1 = Label(event.widget.parent, textvariable=result1Str, font=("Futura", 30))
    result2Str = StringVar()
    result2 = Label(event.widget.parent, textvariable=result2Str, font=("Futura", 23))

    if res1 != False:

        #print(res1)
        result1Str.set("".join(res1))
        result1.place(x=0, y=350)
        if res2 != False:
            #print(res2)
            result2Str.set("".join(res2))
            result2.place(x=(len(res1)*30), y=340)

    else:
        result1Str.set("No chord found for this note combination.")
        result1.place(x=0, y=350)

    noteCount = 0

# uses threading to play note when label (key) is clicked and make it appear pressed
def play_back(event):
    label_pressed(event)
    # This line starts a new thread and runs the method
    # play on that new thread. Go concurrency!
    start_new_thread(play, ('songs/song.txt',event))

# lets user input their notes using the record button
def record_on_off(event):
    global recording
    recording = not recording
    recordText = Label(event.widget.parent, text='RECORDING... (to restart recording, toggle Red button again)', font=("Futura"))
    if recording:
        label_pressed(event)
        recordText.place(x=200, y=100)
    else:
        event.widget.init()
        clear_note_options(event)
        recordText.destroy()
        file = open('songs/song.txt', 'w')
        file.close()

# related to previous function
def record(file_name, note):
    song_file = open(file_name, 'a')
    song_file.write(note)
    song_file.write('\n')

# if the button is pressed it will play the sound and if recording it adds the button to the note list
def button_pressed(event):
    if event.widget.pressed == 0:
        wave_obj = sa.WaveObject.from_wave_file('sounds/' + event.widget.name + '.wav')
        wave_obj.play()
        if recording:
            add_note_option(event,event.widget.name)
            record('songs/song.txt', event.widget.name)
            label_pressed(event)
            event.widget.pressed = 1

# class for piano
class Piano(Frame):

    def __init__(self, parent):

        # initialization of the window along with coloring for background
        Frame.__init__(self, parent, background='White')

        self.parent = parent
        self.init_user_interface()

    # two dimensional array for for position, name, and button pressed of keys
    # was easier to modify and access in this format rather than dictionary
    def init_user_interface(self):
        keys = [
            [0, 'A1', 0],
            [35, 'A#1', 0],
            [50, 'B1', 0],
            [100, 'C1', 0],
            [135, 'C#1', 0],
            [150, 'D1', 0],
            [185, 'D#1', 0],
            [200, 'E1', 0],
            [250, 'F1', 0],
            [285, 'F#1', 0],
            [300, 'G1', 0],
            [335, 'G#1', 0],
            [350, 'A2', 0],
            [385, 'A#2', 0],
            [400, 'B2', 0],
            [450, 'C2', 0],
            [485, 'C#2', 0],
            [500, 'D2', 0],
            [535, 'D#2', 0],
            [550, 'E2', 0],
            [600, 'F2', 0],
            [635, 'F#2', 0],
            [650, 'G2', 0],
            [685, 'G#2', 0]
        ]

        # checks if white key or black key (if # in note and note lenghth greater than 2 it is a black key)
        for key in keys:
            if len(key[1]) == 2:
                img = 'pictures/white_key.gif'
                key.append(self.create_key(img, key))

        for key in keys:
            if len(key[1]) > 2:
                img = 'pictures/black_key.gif'
                key.append(self.create_key(img, key))

        img = PhotoImage(file='pictures/red_button.gif')
        record_button = Label(self, image=img, bd=0)
        record_button.image = img
        record_button.place(x=700, y=100)
        record_button.name = 'red_button'
        record_button.init = self.init_user_interface
        record_button.parent = self
        record_button.bind('<Button-1>', record_on_off)

        img = PhotoImage(file='pictures/green_button.gif')
        play_button = Label(self, image=img, bd=0)
        play_button.image = img
        play_button.place(x=700, y=150)
        play_button.name = 'green_button'
        play_button.parent= self.parent
        play_button.bind('<Button-1>', play_back)

        self.parent.title('Chord Finder')


        # instructions at top
        instructionY=0
        instructionX=0
        instruction1 = Label( self, text='Press the red button to start recording the notes to input for identifying the chord.', font=("Futura"))
        instruction1.place(x=instructionX, y=instructionY+0)
        instruction3 = Label( self, text='Select which of the enharmonic notes you would like to choose from the dropdown generated.', font=("Futura"))
        instruction3.place(x=instructionX, y=instructionY+20)
        instruction2 = Label( self, text='Press the green button to submit/play/find the chord.', font=("Futura"))
        instruction2.place(x=instructionX, y=instructionY+40)

        # window settings
        w = 750
        h = 500
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.pack(fill=BOTH, expand=1)

    # creates a key
    def create_key(self, img, key):
        key_image = PhotoImage(file=img)
        label = Label(self, image=key_image, bd=0)
        label.image = key_image
        label.place(x=key[0], y=100)
        label.name = key[1]
        label.pressed = key[2]
        label.root = self.parent
        label.bind('<Button-1>', button_pressed)
        return label

def main():
    root = Tk()
    app = Piano(root)
    app.mainloop()

if __name__ == '__main__':
    main()
