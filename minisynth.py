# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    minisynth.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: emende & aviholai                          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/05/25 11:07:02 by emende            #+#    #+#              #
#                                                     ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#/	The goal of the assignment is to create a synthesizer tool called
#/	"Minisynth" that reads and plays a musical "sheet" in a '.synth' extension.
#/	The synthesizer runs in a 'pygame' engine and also requires the following
#/	libraries.

import os, sys, math, numpy as np
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" #/	Hides the community message.
from multiprocessing.pool import ThreadPool as Pool
import pygame

np.seterr(divide='ignore', invalid='ignore') # ignoring divide with 0

SAMPLERATE = 44100
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.mixer.set_num_channels(26) # Max number of tracks
pygame.init()

screen = pygame.display.set_mode([500, 500])
font = pygame.font.SysFont("Impact", 32)
bg = pygame.image.load('img/skyline.jpeg')
logo = pygame.image.load('img/logo.png')
pygame.display.set_caption('minisynth')
clock = pygame.time.Clock()

#/	Note frequencies converted to global variables.
#/	The names correspond to the western notation with "r" representing "rest".

notation_frequency = {
	"c0" : 16.35, "c#0" : 17.32, "db0" : 17.32, "d0" : 18.35, "d#0" : 19.45,
	"eb0" : 19.45, "e0" : 20.60, "f0" : 21.83, "f#0" : 23.12, "gb0" : 23.12,
	"g0" : 24.50, "g#0" : 25.96, "ab0" : 25.96, "a0" : 27.50, "a#0" : 29.14,
	"bb0" : 29.14, "b0" : 30.87, "c1" : 32.70, "c#1" : 34.65, "db1" : 34.65,
	"d1" : 36.71, "d#1" : 38.89, "eb1" : 38.89, "e1" : 41.20, "f1" : 43.65,
	"f#1" : 46.25, "gb1" : 46.25, "g1" : 49.00, "g#1" : 51.91, "ab1" : 51.91,
	"a1" : 55.00, "a1#" : 58.27, "bb1" : 58.27, "b1" : 61.74, "c2" : 65.41,
	"c#2" : 69.30, "db2" : 69.30, "d2" : 73.42, "d#2" : 77.78, "eb2" : 77.78,
	"e2" : 82.41, "f2" : 87.31, "f#2" : 92.50, "gb2" : 92.50, "g2" : 98.00,
	"g#2" : 103.83, "ab2" : 103.83, "a2" : 110.00, "a#2" : 116.54, "bb2" : 116.54,
	"b2" : 123.47, "c3" : 130.81, "c#3" : 138.59, "db3" : 138.59, "d3" : 146.83,
	"d#3" : 155.56, "eb3" : 155.56, "e3" : 164.81, "f3" : 174.61, "f#3" : 185.00,
	"gb3" : 185.00, "g3" : 196.00, "g#3" : 207.65, "ab3" : 207.65, "a3" : 220.00,
	"a#3" : 233.08, "bb3" : 233.08, "b3" : 246.94, "c4" : 261.63, "c#4" : 277.18,
	"db4" : 277.18, "d4" : 293.66, "d#4" : 311.13, "eb4" : 311.13, "e4" : 329.63,
	"f4" : 349.23, "f#4" : 369.99, "gb4" : 369.99, "g4" : 392.00, "g#4" : 415.30,
	"ab4" : 415.30, "a4" : 440.00, "a#4" : 466.16, "bb4" : 466.16, "b4" : 493.88,
	"c5" : 523.25, "c#5" : 554.37, "db5" : 554.37, "d5" : 587.33, "d#5" : 622.25,
	"eb5" : 622.25, "e5" : 659.25, "f5" : 698.46, "f#5" : 739.99, "gb5" : 739.99,
	"g5" : 783.99, "g#5" : 830.61, "ab5" : 830.61, "a5" : 880.00, "a#5" : 932.33,
	"bb5" : 932.33, "b5" : 987.77, "c6" : 1046.50, "c#6" : 1108.73, "db6" : 1108.73,
	"d6" : 1174.66, "d#6" : 1244.51, "eb6" : 1244.51, "e6" : 1318.51, "f6" : 1396.91,
	"f#6" : 1479.98, "gb6" : 1479.98, "g6" : 1567.98, "g#6" : 1661.22, "ab6" : 1661.22,
	"a6" : 1760.00, "a#6" : 1864.66, "bb6" : 1864.66, "b6" : 1975.53, "c7" : 2093.00,
	"c#7" : 2217.46, "db7" : 2217.46, "d7" : 2349.32, "d#7" : 2489.02, "eb7" : 2489.02,
	"e7" : 2637.02, "f7" : 2793.83, "f#7" : 2959.96, "gb7" : 2959.96, "g7" : 3135.96,
	"g#7" : 3322.44, "ab7" : 3322.44, "a7" : 3520.00, "a#7" : 3729.31, "bb7" : 3729.31,
	"b7" : 3951.07, "c8" : 4186.01, "c#8" : 4434.92, "db8" : 4434.92, "d8" : 4698.63,
	"d#8" : 4978.03, "eb8" : 4978.03, "e8" : 5274.04, "f8" : 5587.65, "f#8" : 5919.91,
	"gb8" : 5919.91, "g8" : 6271.93, "g#8" : 6644.88, "ab8" : 6644.88, "a8" : 7040.00,
	"a#8" : 7458.62, "bb8" : 7458.62 , "d8" : 7902.13,
	"r" : 0
}

missing_octave = [
	'c', 'c#', 'db', 'd', 'd#', 'eb', 'e', 'f', 'f#',
	'gb', 'g', 'g#', 'ab', 'a', 'a#', 'bb', 'b']

#/	The math processing for the synthesis of the sound wave, duration and frequency.
def synthesizer(frequency=440.0, duration=1.0, wave='sine', vol=0.01):
	range = np.arange(SAMPLERATE * duration) * frequency / SAMPLERATE
	if wave == 'sine' or wave == 'kick' or wave == 'snare':
		arr = np.sin(2 * np.pi * range)
	if wave == 'saw':
		arr = 2.0 * ((range + 0.5) % 1.0) - 1.0 # saw
	if wave == 'square':
		arr = np.array([1 if math.floor(2 * t) % 2 == 0 else 0 for t in range])
	if wave == 'triangle':
		arr = 1 - np.abs(range % 4) - 2
	return arr

#/ Opening file and reading and parsing everything to arrays
def read_file(file_name):
	tracks = {}
	f = open(file_name)
	for line in f.readlines():
		if line[0] == '#':
			print("\033[1;35m" +line + "\033[0m")
		if line[0] != '#' and len(line) > 1:
			line = line.split()
			if line[0] == "tempo":
				beats_per_minute = int(line[1])
				beat = float(60 / beats_per_minute)
			elif line[0] == "tracks":
				track_instruments = line[1].split(',')
			else:
				track_count = int(line[0].replace(':', ''))
				line.pop(0)
				note_track = []
				for note_key in line:
						note_key = note_key.split('/')
						if note_key[0] in notation_frequency or note_key[0] in missing_octave:
							note_track.append(note_key)
				if track_count not in tracks:
					tracks[track_count] = note_track
				else:
					tracks[track_count] += note_track
	return tracks, beat, track_instruments

#/ Appending notes to one long track. Fixing also missing octaves etc.
def parse_sheet(note_track, beat, track_number, vol=0.3, wave='sine'):
	(pb_freq, pb_bits, pb_chns) = pygame.mixer.get_init()
	s = np.zeros(0)
	note_length = 1.0
	latest_octave = '4'
	for note_key in note_track:
		if len(note_key) >= 2:
			note_length = float(note_key[1])
		if note_key[0] in missing_octave:
			note_key[0] = note_key[0] + str(latest_octave)
		elif note_key[0] != 'r' and note_key[0] in notation_frequency:
			latest_octave = note_key[0][-1]
		if note_key[0] in notation_frequency:
			note = synthesizer(notation_frequency[note_key[0]], note_length * beat, wave, 0.01)
			s = np.append(s, note)

	#/ Different multipliers for every waveform, to get volumes match more
	if wave == 'sine': mult = 1.0
	if wave == 'saw': mult = 0.25
	if wave == 'square': mult = 0.35
	if wave == 'triangle': mult = 0.12
	vol = vol * mult

	#/ If stereo, make both channels with repeat
	if pb_chns == 2:
		s = np.repeat(s[..., np.newaxis], 2, axis=1)

	#/ Making pygame sound array, with two different version: 8 bit or 16 bit
	if pb_bits == 8:
		snd_arr = s * vol * 127.0
		sound = pygame.sndarray.make_sound(snd_arr.astype(np.uint8) + 128)
	elif pb_bits == -16:
		snd_arr = s * vol * float((1 << 15) - 1)
		sound = pygame.sndarray.make_sound(snd_arr.astype(np.int16))
	print("\033[0;32mCreated track number: \033[1;32m" + str(track_number) + "\033[0m")
	compiled_tracks.append(sound)

compiled_tracks = []

cord = [19, 206]
ofs = 1

def move_logo():
	global ofs
	ofs += 0.02
	if ofs > 360:
		ofs -= 360
	logo_cord = cord.copy()
	logo_cord[1] += math.sin(ofs) * 2 * math.pi
	return logo_cord

def update_screen():
	move_logo()
	screen.fill((0,0,0))
	screen.blit(bg, (0, 0))
	screen.blit(logo, move_logo())
	text = font.render('ESC will close window', False, (2, 84/2, 172/2))
	screen.blit(text, (250 - text.get_width() / 2, 500 - (text.get_height() * 1.5) + 3))
	text = font.render('ESC will close window', False, (2, 84, 172))
	screen.blit(text, (250 - text.get_width() / 2, 500 - text.get_height() * 1.5))
	pygame.display.flip()

def play_track(note_track, vol=0.7):
	pygame.mixer.Sound.set_volume(note_track, 0.7)
	pygame.mixer.find_channel(True).play(note_track)

def main():
	if (len(sys.argv) > 1):
		(tracks, beat, track_instruments) = read_file(sys.argv[1])

		#/ Make a pool of processes to parse every track asynchronously.
		pool = Pool(len(tracks))
		for i in range(1, len(tracks) + 1):
			pool.apply_async(parse_sheet, (tracks[i], beat, i, 0.05, track_instruments[i - 1],))
		pool.close()
		pool.join()

		print("\033[1;36mAll tracks finished. Playing the compilation...\033[0m")

		#/ Play tracks asynchronously.
		pygame.mixer.set_num_channels(len(compiled_tracks))
		track_pool = Pool(len(compiled_tracks))
		for note_track in compiled_tracks:
			track_pool.apply_async(play_track, (note_track,))
		track_pool.close()
		track_pool.join()

		#/ Loop for pygame, waiting for your escape
		running = True
		while running:
			update_screen()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				if event.type == pygame.KEYDOWN:
					running = False
			clock.tick(60)
		pygame.mixer.quit()
		pygame.quit()
	else:
		print("\033[0;32mExecute with: \033[1;32m./minisynth file\033[0m")

if __name__ == "__main__":
	main()
