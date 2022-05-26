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
#/	"Minisynth" that reads and plays a musical "sheet" in a '.synth'
#/	extension.
#/	The synthesizer runs in a 'pygame' engine and also requires the libraries
#/	'numpy', 'sys', 'threading' and 'multiprocessing'.

from asyncio import SafeChildWatcher
from audioop import mul
from operator import length_hint
import pygame
import numpy as np
import sys
import threading
from multiprocessing import Process

np.seterr(divide='ignore', invalid='ignore')
SAMPLERATE = 44100

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()


#/	Note frequencies converted to global variables.
#/	The names correspond to the western notation with "r" representing "rest".

noteFreqs = {
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

	"c" : 261.63, "c#" : 277.18, "db" : 277.18, "d" : 293.66, "d#" : 311.13,
	"eb" : 311.13, "e" : 329.63, "f" : 349.23, "f#" : 369.99, "gb" : 369.99,
	"g" : 392.00, "g#" : 415.30, "ab" : 415.30, "a" : 440.00, "a#" : 466.16,
	"bb" : 466.16, "b" : 493.88,

	"r" : 0
}



#/	The math processing for the synthesis of the sound wave, duration and frequency.

""" def synth(frequency, duration):
	arr = np.sin(2 * np.pi * np.arange(SAMPLERATE * duration) * frequency / SAMPLERATE)
	sound = np.asarray([32767 * arr, 32767 * arr]).T.astype(np.int16)
	sound = pygame.sndarray.make_sound(sound.copy())
	return sound """

def square_wave(frequency, duration):
	num_steps = int(duration * SAMPLERATE)
	s = []
	length_of_plateau = int(44100 / (2 * frequency))
	counter = 0
	state = 1
	for n in range(num_steps):
		s.append(state)
		counter += 1
		if counter == length_of_plateau:
			counter = 0
			state *= -1
	sound = np.asarray([32767 * s, 32767 * s]).T.astype(np.int16)
	sound = pygame.sndarray.make_sound(sound.copy())
	return sound


def synth(frequency=440.0, duration=1.0, wave='sine', vol=1.0):
	(pb_freq, pb_bits, pb_chns) = pygame.mixer.get_init()
	multiplier = int(frequency * duration)
	if frequency != 0:
		duration = max(1, int(float(pb_freq) / frequency * multiplier))
	else:
		duration = max(1, 0)
	lin = np.linspace(0.0, multiplier, duration, endpoint=False)
	if wave == 'sine':
		arr = np.sin(lin * 2 * np.pi)
	if wave == 'saw':
		arr = 2.0 * ((lin + 0.5) % 1.0) - 1.0 # saw
	if wave == 'square':
		arr = np.zeros(duration)
		arr[lin % 1.0 < 0.5] = 1.0
		arr[lin % 1.0 >= 0.5] = -1.0
	if pb_chns == 2:
		arr = np.repeat(arr[..., np.newaxis], 2, axis=1)
	if pb_bits == 8:
		snd_arr = arr * vol * 127.0
		return pygame.sndarray.make_sound(snd_arr.astype(np.uint8) + 128)
	elif pb_bits == -16:
		snd_arr = arr * vol * float((1 << 15) - 1)
		return pygame.sndarray.make_sound(snd_arr.astype(np.int16))

def play_track(track, beat):
	for note in track:
		if len(note) >= 2:
			noteDuration = float(note[1])
		s = synth(noteFreqs[note[0]], noteDuration * beat, 'sine', 0.5)
		s.set_volume(0.6)
		s.play()
		pygame.time.wait(int((noteDuration * beat) * 1000))

def main():
	if (len(sys.argv) > 1):
#		screen = pygame.display.set_mode([500, 500])
#		font = pygame.font.SysFont('Comic Sans MS', 30)
#		pygame.display.set_caption('minisynth')
#		screen.fill((0,0,0))

		tracks = []
		f = open(sys.argv[1])
		for line in f.readlines():
			if line[0] != '#' and len(line) > 1:
				line = line.split()
				if line[0] == "tempo":
					bpm = int(line[1])
					beat = float(1 / (bpm / 60))
				elif line[0] == "tracks":
					# do something later
					print()
				else:
					line.pop(0)
					track = []
					for note in line:
						note = note.split('/')
						track.append(note)
					tracks.append(track)

		processes = []
		for track in tracks:
			p = Process(target=play_track, args=(track, beat, ))
			processes.append(p)
			p.start()

#		running = True
#		while running:
#			for event in pygame.event.get():
#				if event.type == pygame.QUIT:
#					running = False
#				if event.type == pygame.KEYDOWN:
#					running = False
		for p in processes:
			p.join()
			p.terminate()
		pygame.mixer.quit()
		pygame.quit()
	else:
		print("usage: python3 minisynth.py [filename]")

if __name__ == "__main__":
	main()
