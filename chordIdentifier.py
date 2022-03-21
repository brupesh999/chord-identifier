"""
    Description: just the chord identifier, is imported later in final (finalPiano.py)
    Author: Bhadra Rupesh
    Date: 2021
"""
import pyaudio # this is only necessary for a function at the end that generates tones of audio, not used in final
import numpy as np # this is also used for the tone generating function
import json # necessary for the json files I created noteDict.json and intervalsDict.json (explained later)


# these create globabl variables for the dictionaries in the json files
with open("noteDict.json", "r") as notes:
    NOTE_DICT = json.load(notes)

with open("intervalsDict.json", "r") as intervals:
    INTERVALS_DICT = json.load(intervals)

# not used in final, but for command line interface of chordIdentifier, gets a note from user
def inputNote(prompt, chosenNotes):
    """
    Purpose: It gets an input integer from the user after asking a prompt, and if the
    user doesn't enter an integer it informs the user and asks them to try again.
    Parameters: The prompt (str)
    Return: The integer that the user entered (int)
    """
    while True:
        userInput = input(prompt).lower()

        if userInput == "end":
            return ""
        try:
            int(userInput[-1])
        except:
            print("\nPlease enter a valid note.")
            continue

        if 0 < int(userInput[-1]) < 4:

            noteEndIndex = (len(userInput) - 1)
            userNote = userInput[:noteEndIndex]

            if userNote in NOTE_DICT and userInput not in chosenNotes:
                if userNote not in ["fbb", "e##", "b##", "cbb"]:
                    return userInput
                else:
                    print("\nUnfortunately, your note is not valid because it is double diminished or augmented.\n")
            else:
                print("\nPlease enter a valid note.\n")
                continue

        else:
            print("\nPlease enter a valid note.\n")
            continue

# just for aesthetic reasons; converts something from all lowercase (like in json file) to formatted
def convertToFormatted(note):
    formattedNote = ""
    formattedNote += note[0].upper()
    formattedNote += note[1:]
    return formattedNote

# also not used in final, just for command line interface of chordIdentifier.py, gets user list of chord notes
def getUserNotesListChord(prompt):
    notes = list(NOTE_DICT.keys())
    userNoteList = []
    while True:
        if len(userNoteList) == 14:
            print("This is the maximum number of notes in your chord.")
        else:
            userNote = inputNote(prompt, userNoteList)
            if userNote == "" and (len(userNoteList) == 1 or len(userNoteList) == 0):
                print("\nPlease enter more notes.")
                continue
            elif userNote == "" and len(userNoteList) == 2:
                print("Because this is only two notes, this will be analyzed as an interval.")
            elif userNote != "":
                userNoteList.append(convertToFormatted(userNote))
                print("\n\nThe chord is now %s.\n" % userNoteList)
                continue
        if len(userNoteList) > 2:
            print("\n\nThe final chord you are submitting is:\n%s\n" % userNoteList)
        else:
            print("\n\nThe interval you are submitting is:\n%s\n" % userNoteList)
        return userNoteList

# this is used later (a generic function)
def getKey(dict, val):
    for key, value in dict.items():
        if val == value:
            return key

# makes the notes in order from lowest to highest
def mergeChord(userNoteList):
    userNoteDict = {}
    for note in userNoteList:
        orderedNote = note[:len(note)]
        if orderedNote not in userNoteDict.keys():
            userNoteDict[orderedNote] = numberOfNote(orderedNote)
    sortedMergedNotes = dict(sorted(userNoteDict.items(), key=lambda item: item[1]))
    return(sortedMergedNotes)

# not used in code, but could be used in future update for finding key signature
def findMajorKeySignatureList(note):
    keyList = ["a", "b", "c", "d", "e", "f", "g"]
    if note == "c":
        accidentalList = []
    elif (note != "b" and "b" in note) or note == "f":
        flatCircle = ["b", "e", "a", "d", "g", "c", "f"]
        accidentalList = flatCircle[:((flatCircle.index(note[0]) + 1) % 7)]
        for element in accidentalList:
            keyList[keyList.index(element)] = element + "b"
    elif "#" not in note or note == "f#" or "c#":
        sharpCircle = ["f", "c", "g", "d", "a", "e", "b"]
        accidentalList = sharpCircle[:((sharpCircle.index(note[0]) - 1) % 7)]
        for element in accidentalList:
            keyList[keyList.index(element)] = element + "#"

    #finalKeySignatureList = [keyList.index(note):(keyList.index(note) - 7) ]

    return keyList

# functionality to get interval above note (not used in GUI yet)
def majIntervalAboveNote(rootNote, intervalNum):
    keyList = findMajorKeySignatureList(rootNote)
    rootNoteNum = numberOfNote(rootNote)
    beginning = keyList.index(rootNote[:len(rootNote) - 1])
    endNote = keyList[(beginning + intervalNum - 1) % 7]
    if numberOfNote(endNote + "1") < rootNoteNum:
        endNote = endNote + "2"
    else:
        endNote = endNote + "1"
    return endNote

# related to previous function
def reversedInterval(rootNote, note2):
    reversedNoteRoot = note2[:len(note2) - 1] + rootNote[-1]
    reversedNote2 = rootNote[:len(note2) - 1] + note2Num[-1]
    flippedInterval = getInterval(reversedNoteRoot, reversedNote2)
    quality = flippedInterval[0]

    if quality == "d":
        newQuality = "A"
    elif quality == "A":
        newQuality= "d"
    elif quality == "M":
        newQuality = "m"
    elif quality == "m":
        newQuality = "M"

    reverseInterval = newQuality + str(9 - flippedInterval[1])
    return reverseInterval

# necessary for getInterval
def getNaturalIndex(rootNote):
    naturalList = ["a1", "b1", "c1", "d1", "e1", "f1", "g1", \
    "a2", "b2", "c2", "d2", "e2", "f2", "g2", \
    "a3", "b3", "c3", "d3", "e3", "f3", "g3"]

    if "Ab" not in rootNote:
        rootNoteNaturalIndex = naturalList.index(rootNote[0].lower() + rootNote[-1])
    else:
        rootNoteNaturalIndex = naturalList.index("a" + str(int(rootNote[-1]) + 1))

    return rootNoteNaturalIndex

# similar to previous function, necessary for getInterval
def naturalNoteFromIndex(naturalNoteIndex):
    naturalList = ["a1", "b1", "c1", "d1", "e1", "f1", "g1", \
    "a2", "b2", "c2", "d2", "e2", "f2", "g2", \
    "a3", "b3", "c3", "d3", "e3", "f3", "g3"]

    naturalNoteFromIndex = naturalList[naturalNoteIndex]

    return naturalNoteFromIndex

# uses previous function, necessary for getInterval
def getNaturalInterval(rootNote, note2):
    rootNoteNaturalIndex = getNaturalIndex(rootNote)
    note2NaturalIndex = getNaturalIndex(note2)

    plainInterval = (note2NaturalIndex - rootNoteNaturalIndex) % 21 + 1

    return plainInterval

# this is one of the most important functions in my code: it gets the interval between any two notes
def getInterval(rootNote, note2):
    #print("get interval", rootNote, note2)
    intervalNameList = list(INTERVALS_DICT.keys())

    if getJustNote(rootNote) in ["fbb", "e##", "b##", "cbb"] or getJustNote(note2) in ["fbb", "e##", "b##", "cbb"]:
        return False

    #print(rootNote, note2)
    note1Num = numberOfNote(rootNote)
    note2Num = numberOfNote(note2)
    intervalNum = (note2Num - note1Num) % 24

    if note1Num > note2Num:
        rootNote, note2 = note2, rootNote

    posPlainInterval = []
    for posInterval in intervalNameList:
        if intervalNum in INTERVALS_DICT[posInterval]:
            posPlainInterval.append(posInterval)

    #print("pos plain interval list", posPlainInterval)

    if len(posPlainInterval) > 1:
        plainInterval = getNaturalInterval(rootNote, note2)
    elif len(posPlainInterval) == 1:
        plainInterval = posPlainInterval[0]
    else:
        return False

    #print("plainInterval", plainInterval)

    for plainIntervalNum in posPlainInterval:

        # gets the quality and value (number) of interval
        if plainIntervalNum == str(plainInterval):
            intervalIndex = INTERVALS_DICT[str(plainInterval)].index(intervalNum)
            lenPosIntervals = len(INTERVALS_DICT[str(plainInterval)])
            if intervalIndex == 0:
                intervalQuality = "d"
            elif intervalIndex == lenPosIntervals - 1:
                intervalQuality = "A"
            elif lenPosIntervals == 3:
                intervalQuality = "P"
            elif intervalIndex == lenPosIntervals - 2:
                intervalQuality = "M"
            elif intervalIndex == lenPosIntervals - 3:
                intervalQuality = "m"
            else:
                return False

    finalInterval = (intervalQuality + str(plainInterval))
    return finalInterval

# gets just the quality of the interval
def getQuality(interval):
    return interval[0]

# gets just the value (number) of the interval
def getNumber(interval):
    return interval[1:]

# gets just the note (without the octave number)
def getJustNote(note):
    noteCharList = list(note)
    try:
        int(note[-1])
    except:
        justNote = "".join(noteCharList)
        return justNote.lower()

    noteCharList.remove(note[-1])
    justNote = "".join(noteCharList)
    return justNote.lower()

# gets the number corresponding to a note from noteDict.json variable NOTE_DICG
def numberOfNote(note):
    numOfNote = NOTE_DICT[getJustNote(note)]
    numOfNote += (int(note[-1]) - 1) * 12

    return numOfNote

# gets the list of possible notes that could correspond to a number
def notesOfNumber(number):
    notes = []

    modNumber = number % 12
    octaveNumber = int(number // 12) + 1

    for note in NOTE_DICT.keys():
        possibleNoteNum = NOTE_DICT[note]
        if possibleNoteNum == number % 12:
            notes.append(note + str(octaveNumber))

    return notes

# related to previous function
def getNoteFromIndexWithPos(index, posNoteList):
    possibleNotes = notesOfNumber(index)
    finalNote = ""
    for note in possibleNotes:
        posNote = convertToFormatted(note)
        if posNote in posNoteList:
            finalNote = posNote
    return finalNote

# this function doesn't quite work yet but it wasn't necessary for my code
def getArrangements(sortedMergedNotes):
    chordArrangements = []
    notesTuplesList = list(sortedMergedNotes.items())

    justNoteList = []
    for notesTuple in notesTuplesList:
        justNoteList.append(notesTuple[0])

    for rootIndex, rootTuple in enumerate(notesTuplesList):
        arrangement = []

        for noteIndex, noteTuple in enumerate(notesTuplesList):
            arrangement.append(notesTuplesList[(rootIndex + noteIndex) % len(notesTuplesList) - 1])

        chordArrangements.append(dict(arrangement))
        print("chordArrangements", chordArrangements)

    for posArrangement in chordArrangements:
        arrangementList = list(posArrangement.values())
        print("\narrangementList", arrangementList)
        for index, num in enumerate(arrangementList):
            possibleChangeNote = getNoteFromIndexWithPos(num, justNoteList)
            print("possibleChangeNote", possibleChangeNote)
            if index + 1 < len(arrangementList):
                nextNoteNum = arrangementList[index + 1]
                nextNote = getNoteFromIndexWithPos(nextNoteNum, justNoteList)
                print("nextNote", nextNote)

                if nextNote[-1] < possibleChangeNote[-1]:
                    posArrangement.update({possibleChangeNote: num - 12})
                    posArrangement[convertToFormatted(getJustNote(possibleChangeNote)) + "1"] = posArrangement.pop(possibleChangeNote)
                    arrangementList = list(posArrangement.values())
                    posArrangement = dict(sorted(posArrangement.items(), key=lambda item: item[1]))
                    print("posArrangement", posArrangement)

            if index > 0:
                prevNoteNum = arrangementList[index]
                prevNote = getNoteFromIndexWithPos(prevNoteNum, justNoteList)
                print("prevNote", prevNote)

                if prevNote[-1] > possibleChangeNote[-1]:
                    posArrangement.update({possibleChangeNote: num + 12})
                    posArrangement[convertToFormatted(getJustNote(possibleChangeNote)) + "2"] = posArrangement.pop(possibleChangeNote)
                    arrangementList = list(posArrangement.values())
                    posArrangement = dict(sorted(posArrangement.items(), key=lambda item: item[1]))
                    print("posArrangement", posArrangement)


    return chordArrangements

# necessary to get all intervals of pairs of notes within a chord to identify chord
def getAllIntervals(chord):
    intervals = []
    chordNotes = list(chord.keys())
    for nonRoot in chordNotes[1:]:
        root = chordNotes[0]
        interval = getInterval(root, nonRoot)
        if interval != False:
            intervals.append(interval)
        else:
            return False
    return intervals

# makes sure chord doesnt have repeated notes
def checkNoRepeats(chord):
    for note in list(chord.keys()):
        for distinctNote in chord.remove(note):
            if note[0] in distinctNote:
                return False
    return True

# classes for interval and chord (were kind of unnecessary but i wanted to practice classes
# as I use them in my finalPiano program)
class Interval:
    def __init__(self, name):
        self.quality = getQuality(name)
        self.number = int(getNumber(name))
        self.name = name

class Chord:
    def __init__(self, name):
        self.name = name

# one of the most important functions along with getInterval because this identifies chords based on an algorithm i figured out
def findChord(chordArrangement):
    finalChord = [convertToFormatted(getJustNote(list(chordArrangement.keys())[0]))]
    superscript = []

    second = False
    third = False
    fourth = False
    fifth = False
    seventh = False
    other = []

    allIntervals = getAllIntervals(chordArrangement)
    if allIntervals != False:
        for interval in getAllIntervals(chordArrangement):
            #print(interval)
            intervalObject = Interval(interval)
            #plainInterval = interval[-1]
            intervalNumber = intervalObject.number
            if intervalNumber == 5:
                fifth = interval
            elif intervalNumber == 3:
                third = interval
            elif intervalNumber == 2:
                second = interval
            elif intervalNumber == 4:
                fourth = interval
            elif intervalNumber == 7:
                seventh = interval
            elif intervalNumber in [6, 9, 11, 13]:
                other.append(interval)
            else:
                return False
        major = False
        minor = False
        augmented = False
        diminished = False

        add = False
        sus = False

        if second != False or fourth != False:
            if third != False:
                add = "add"
                superscript.append(add)
            else:
                sus = "sus"
                superscript.append(sus)
        else:
            superscript.append("")

        if third == False and fifth == False:
            return False
        elif fifth == False:
            fifth = "P5"
        elif third == False:
            if fifth == "P5" or fifth == "A5":
                third = "M3"
            else:
                third = "m3"

        if second != False:
            if second == "A2":
                superscript.append("#2")
            elif second == "m2":
                superscript.append("b2")
            elif second == "d2":
                return False
            else:
                superscript.append("2")

        if fourth != False:
            if fourth == "A4":
                superscript.append("#4")
            elif fourth == "P4":
                superscript.append("4")
            else:
                return False

        if third == "M3" and fifth == "P5":
            major = "M"
        elif third == "m3" and fifth == "P5":
            minor = "m"
            finalChord.append(minor)
        elif third == "M3" and fifth == "A5":
            augmented = "aug"
            finalChord.append(augmented)
        elif fifth == "d5":
            if seventh == "m7":
                diminished = "ø"
                finalChord.append(diminished)
            elif third == "m3" or seventh == "d7":
                diminished = "°"
                finalChord.append(diminished)
            else:
                major = "M"
                diminished = "b5"
                superscript.append(diminished)


        if seventh != False:
            if seventh == "M7":
                finalChord.append("maj7")
            else:
                finalChord.append("7")
        else:
            finalChord.append("")


        for dissonance in other:
            quality = dissonance[0]
            intervalNum = dissonance[1:]

            if quality == "m":
                superscript.append("b%s" % intervalNum)
            elif quality == "A":
                superscript.append(" #%s" % intervalNum)
            elif quality == "d":
                return False
            else:
                superscript.append(" %s" % intervalNum)

    else:
        return False

    return finalChord, superscript
    # i can explain the algorithm in class if I have time

# not used
def allChordsFind(chordArrangement):
    if checkNoRepeats(chord) == False:
        print("This chord has one or more natural notes repeated.")
    return

# good function to get interval above note but not used in final GUI
def getIntervalAboveNote(rootNote, interval):
    quality = interval[0]
    intervalNum = interval[1:]
    intervalQuality = interval[0]

    intervalSemitonesPossible = INTERVALS_DICT[str(intervalNum)]

    lenPosSemitones = len(intervalSemitonesPossible)

    if intervalQuality == "d":
        intervalSemitones = intervalSemitonesPossible[0]
    elif intervalQuality == "A":
        intervalSemitones = intervalSemitonesPossible[lenPosSemitones - 1]
    elif lenPosSemitones == 3:
        intervalSemitones = intervalSemitonesPossible[1]
    elif intervalQuality == "M":
        intervalSemitones = intervalSemitonesPossible[lenPosSemitones - 2]
    elif intervalQuality == "m":
        intervalSemitones = intervalSemitonesPossible[lenPosSemitones - 3]

    rootNoteNum = numberOfNote(rootNote)
    possibleEndNotes = notesOfNumber(rootNoteNum + intervalSemitones)

    rootNoteNaturalIndex = getNaturalIndex(rootNote)
    note2NaturalIndex = rootNoteNaturalIndex + int(intervalNum) - 1

    note2Natural = naturalNoteFromIndex(note2NaturalIndex)

    for pos in possibleEndNotes:
        if getJustNote(note2Natural) == getJustNote(pos)[0]:
            note2 = pos

    return note2

# tone generator function (not used as I have wav files in piano GUI that are more realistic)
# used inspiration from online source because i didn't know how to use samples and pyaudio
def playSound(note, duration = 2.0):

    startNoteName = "a"
    startNoteFreq = 440

    noteNum = numberOfNote(note.lower())
    intervalNum = (noteNum)

    p = pyaudio.PyAudio()

    volume = 0.5     # range [0.0, 1.0]
    fs = 44100       # sampling rate, Hz, must be integer
    duration = 2.0   # in seconds, may be float
    f = startNoteFreq * 2**(intervalNum/12)       # sine frequency, Hz, may be float

    # generate samples, note conversion to float32 array
    samples = (np.sin(2 * np.pi * np.arange(fs * duration) * f / fs)).astype(np.float32)

    # for paFloat32 sample values must be in range [-1.0, 1.0]
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=fs, output=True)

    # play. May repeat with different volume values (if done interactively)
    stream.write(volume*samples)

    stream.stop_stream()
    stream.close()

    p.terminate()

# related to previous function
def playChordSeparate(notesList):
    for note in notesList:
        playSound(note)
    return

# this gets the options to select in finalPiano.py
def returnSelectOptions(note):
    numOfNote = numberOfNote(note)
    possibleNotes = notesOfNumber(numOfNote)
    finalPosSelect = []
    for posSelect in possibleNotes:
        finalPosSelect.append(convertToFormatted(posSelect))
    return finalPosSelect

# mainly has test code but all commented out
if __name__ == "__main__":

    print()
    #promptChord = ("\nPlease enter the notes in your chord in order (type the letter, flats/sharps if necessary, and a number (1 or 2) to indicate the octave).\nFor example, you can type: Eb1, C#1, or A2. Press enter after each individual note. When you are done, please sumbit 'end' after another enter.\n\n")
    #userNoteChord = getUserNotesListChord(promptChord)
    #print(userNoteChord)

    #print(returnSelectOptions("Ebb1"))
    #print(returnSelectOptions("A2"))

    #print(findMajorKeySignatureList("f#"))

    #print(getArrangements({"A1": 0, "C1": 3, "E1": 7}))
    #mergedNoteChord = mergeChord(userNoteChord)
    #print(mergedNoteChord)

    ##print(getArrangements(mergedNoteChord))

    #print(getIntervalAboveNote("ab3", "m6"))
    #playChordSeparate(userNoteChord)

    #print(findChord(mergedNoteChord))

    #findChord(getArrangements(mergedNoteChord)[1])
    #print("".join(findChord(mergedNoteChord)[0]), "".join(findChord(mergedNoteChord)[1]))
