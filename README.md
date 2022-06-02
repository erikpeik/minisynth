# minisynth 🔊
 
 A Rush project at **Hive Helsinki**, is a 2-3 days project designed to take us way out of our comfort zone and try something new.

# Made by: [emende](https://github.com/erikpeik) and [aviholai](https://github.com/Anviles)

## ❔ What is it?
 The objective of this rush is to create a tool called *minisynth*, able to read in a specific music description file format and play it.

## 💽 How to run it?

1. If you want to try this yourself clone this repository: `git clone https://github.com/erikpeik/minisynth.git`

2. There should be a bash script called `minisynth`.

3. We are using python, and it requires two things: `pygame` & `numpy`

4. To install requirements: `./minisynth install`

5. Simply invoke the tool with the command, where file: `./minisynth file` 
- (there are a bunch of audio description files in the examples folder)

6. `ESC` will quit the application.


## 📝 Music description format

The **minisynth** program accepts the following file format (examples come with the extension .synth, not required):
- The file format is text-based
- Any empty line or line starting with a `#` character is ignored as a comment
- The first non-comment line must be in the format `tempo <N>`, where `<N>` is an integer, representing the tempo of the piece in beats per minute
- The next non-comment line must be `tracks` followed by a comma-separated list of instruments:
```tracks <instument>[,<instument>,...]```
 - Each entry in this list represents a track, numbered from 1 to the total number of tracks. See further for the list of instruments to support.
 - All remaining non-comment lines must be in the following format: `<track>:<notes>`, where `<track> `is the track number, and `<notes>` represents notes to be added to the given track.

## 🎵 Notes format

The `<notes>` part of each line is parsed for all substrings matching the following pattern: `<pitch>[<alteration>][<octave>][/<duration>]`
- `<pitch>` is any lowercase letter from a to g, representing the usual pitch names in Western notation, or the letter r to represent a rest (silence)
- `<alteration>` is optional, and can either be # or b, indicating that the note should be sharp or flat (note that these are the hash symbol and the lowercase letter B, representable in ASCII, not the sharp and flat musical symbols available in Unicode)
- `<octave>` is an optional integer from 0 to 9 representing the octave of the note (using the standard scientific pitch notation, so that middle C is c4)
- `<duration>` is optional and preceded with a / when present: it is a decimal number, possibly fractional, representing the duration of the note in beats

More information about notes format and generally about this project you can find in [pdf](https://github.com/erikpeik/minisynth/blob/master/subject.pdf).

## ✨ Audio synthesizer

Each track generates notes according to the instrument assigned, as indicated by the `tracks` line in the document. Your tool must support the following waveform generation:
- sine waves
- saw waves
- square waves
- triangle waves

Therefore, the possible values for `<instrument>` are sine, saw, square, and triangle.

## 🔨 TO-DO

Because this was 2-3 days Rush project there is still much that could be improved:
- Audio visualizer
- More sounds
- Cleaning up code
- Better audio quality
- etc...

If this could be done now again, `pygame` is not the best tool in python. The hardest part was getting everything synchronized.

There is also `pyaudio` that is more specified for sounds, with that tool visualization and other stuff would be more doable.


