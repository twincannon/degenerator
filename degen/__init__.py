#!/usr/bin/python

import sys
import subprocess
import os
from argparse import ArgumentParser
import time

#extra credit - upload to youtube
#todo - https://trac.ffmpeg.org/wiki/Seeking

def create_parser():
	parser = ArgumentParser(description = 'Usage: supply at least 1 argument '
		'of a video file in order to start processing. The first two integer '
		'arguments found will be used as the clip start/end time from the input '
		'video, though these parameters can also be set at runtime.'
	)
	parser.add_argument(
		'file',
		type = str,
		help = 'Input video file to process'
	)
	parser.add_argument(
		'start',
		type = int,
		nargs = '?',
		help = 'Start time in video to clip (optional)'
	)
	parser.add_argument(
		'end',
		type = int,
		nargs = '?',
		help = 'End time in video to clip (optional)'
	)
	parser.add_argument(
		'-na',
		'-an',
		'-noaudio',
		action='store_true',
		help = 'Disable audio in output video'
	)
	parser.add_argument(
		'-nc',
		'-nocompress',
		action='store_true',
		help = 'Disable h264 video compression pass'
	)
	return parser

def getLengthInSeconds(filename):
	result = subprocess.Popen(['ffprobe', filename], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
	linesFound = [x for x in result.stdout.readlines() if "Duration".encode() in x] #list comprehension - equiv to: for x in readlines, if duration in x, return x (i.e. add to return list)
	result.kill()
	if len(linesFound) == 0:
		return #print something? does duration matter enough to halt?
	fullDurationStr = linesFound[0].decode().split(",")[0] #isolate "Duration" text section from other text
	timeList = fullDurationStr.split("Duration: ")[1].split(".")
	return sum(x * int(t) for x, t in zip([3600, 60, 1], timeList[0].split(":"))) + (float(timeList[1]) * 0.01)

def getAvailableFilename(fileExt):
	num = 0
	fileStr = 'output'
	while(os.path.isfile('./' + fileStr + '.' + fileExt) == True): # loop until we find one that doesn't exist
		num += 1
		fileStr = 'output' + str(num)
	return fileStr

def processVideo(args):
	process = subprocess.Popen(args, stdout=subprocess.PIPE)
	process.communicate()
	exitcode = process.wait()
	return exitcode


#print(os.getcwd()) #current working dir
#import pdb; pdb.set_trace() #for debugging

def main():
	print(
	'|---------------------------------------------------------------|\n'
	'|                  .+/  `..:-`-: `-   +```-.       :hhyymMs`    |\n'
	'|                 `/yy::+yo:+:-. .-` .y./o.  ``       `:sdy:    |\n'
	'|                 .oyhds++:` `../yhs/shshmo//+o///:  `.--o+/-`  |\n'
	'|                 -ymMd/-./yyohNMMMMMMMMMMMMMMMMMMMMNy/`        |\n'
	'|                :hmmd/. sddyydmNMMMMMMMMMMMMMMMMMMMMMmo`       |\n'
	'|                +mdy:   oooyyhdNMMMMMMMMMMMMMMMMMMMMMMd-       |\n'
	'|                ``     -::.:shdmmhmMMMMMMMMMMMMMMMMMMNds       |\n'
	'|  .sdo/hhs            -.:/:sdmmmmmmNNNNNNNNNNNmdmmddNNdy.      |\n'
	'| -/hmo.yMm            `-:.`::..............--...........`      |\n'
	'| /odd+.yMm             ``  `              `--                  |\n'
	'| ssdd+-hMm             `   ``````....    .oo/`  `              |\n'
	'| dhmd+-hMm             :`  .--///ooo+    yNNmo`./              |\n'
	'| dMMd/:mMm      ``     o.             `+mMMMMMdo-`     ..      |\n'
	'| dNMd/-dMm      .-     -/`      ....::+mMNMMMMMNho///:::.      |\n'
	'| dNMd+-dMm      `.     .-.:////oyyyyhhods+osyyoydhdddhhh-      |\n'
	'| hNNh/-hNd       .o/   . .shhhhddddddNh/-`.-+/.`+dhshho+.      |\n'
	'| yMdo:-hNh       `/hh/    ://++/+ydMMMMmdhhyosmNMMMm:....      |\n'
	'| yMNh/-dNh        .sdh-   :/--//omNmhoo/:+osyhyo:/mMm/`.-      |\n'
	'| smmNyomNh         ..-`  -s+:.`odNNd.`/oydmmNNmmho-dMy.-.      |\n'
	'|`:yyho`sMNh               o+:. .+ymNNdyyyyyyyoos/+NNy/`     .+h|\n'
	'|`:/oyo :MNh               -:::-``::/yyyyyyymMMmddy+/`    `:yhy:|\n'
	'| : :o/ :mdy`             `.-``  `- ::osyhyysshhyyd+```so    .+-|\n'
	'| - ./: -ddh/:`           :oso/.       -///oooooo/: -::oy    .os|\n'
	'| ` .:: -mdo-o/::`        -:osyo-`      ----/:---- :o+-+y    `-:|\n'
	'| . .:: :MNy:`+sy-`.       :/+sos+.....:::::::::-. s/o/oy`     `|\n'
	'|`  .:. `+h-+/mNds:     -` .://+yyo////ohhhhhdhs+//+////s/.     |\n'
	'|`  `` ./+h`+yNmdm+     /`  -///osoo////+yyyyyyo///////sy+-`-.  |\n'
	'|       .yNMMMd/`/.:hh.+  `` `-://+ssys//sssssso//////syyso- `.`|\n'
	'|       -hhmMM+/-dmmMMmm./yy+-``.::/+yys/s+///////////yyoydo`   |\n'
	'|       .shdMMdmmMMMMMMMmNMNNmo.--``/ss/////////::///+yhyhNd+`  |\n'
	'|       .o+/oh. -hy/` /ddddNmmNMMMMm. ://.-:::-  .+dmmmMMMMMMMd.|\n'
	'|              .:.         s/shhhdmhs  -:` .-.  `ohhMMMMMMMMMMNy|\n'
	'|             -hm/-://///:/:`   `:/-..        `./hdsMMMMMMMMMMMm|\n'
	'|             ys+`/sohNmmNMm+`     -ys:..`  `.:shmmNMMMMMMMMMMMm|\n'
	'|             +.  `.`:+:+oo+/`   .ohMNdhs++/+ohmNNMMMMMMMMMMMMMN|\n'
	'|                                :MMMMMMMMMmmMMMMMMMMMMMMMMMMMMM|\n'
	'|---------------------------------------------------------------|\n'
	'|            T H E   C L I P   D E G E N E R A T O R            |\n'
	'|---------------------------------------------------------------|\n'
	)
	
	parser = create_parser()

	# check for ffmpeg in path
	env = os.environ['PATH']
	if env.find('ffmpeg') == -1:
		print('error: ffmpeg not found in path, aborting')
		quit()

	# check if there's any arguments
	if len(sys.argv) < 2: # first arg is always the execution path
		parser.print_help()
		quit()

	args = parser.parse_args()

	# find filename from args
	if args.file == None or os.path.isfile(args.file) == False:
		print('error: file not found')
		quit()

	filename = args.file

	if not(any(i for i in [(filename[-4:] == str) for str in ['.mp4', '.avi']] if i != -1)):
		print('error: file is not a valid video format, aborting')
		quit()

	outFileExt = 'mp4' # always export to .mp4, but as a reminder, use filename[-3:] to get the extension from filename var
	inVideoLength = getLengthInSeconds(filename);

	start = "" if args.start == None else args.start
	end = "" if args.end == None else args.end

	# prompt for a filename for the output video
	name = ""
	while(name == ""):
		print('\nEnter clip name (blank defaults "output"):')
		name = input()
		
		if name == "":
			name = getAvailableFilename(outFileExt)
			print('warning: no name entered, defaulting to "' + name + '"')
		else:
			# check if name has any invalid filename characters
			invalidchars = ['/','\\','?','%','*',':','|','"','<','>']
			for char in invalidchars:
				if char in name:
					print('error: invalid character "', char,'" entered in filename')
					name = ""

	# make sure we found a start time
	while(start == ""):
		print('\nEnter start time (blank defaults to start of video):')
		start = input()
		if start == "":
			print('warning: no start time entered, using start of video')
			start = 0
		elif not start.isdigit():
			print('error: invalid start time')
			start = ""
		elif float(start) > inVideoLength:
			print('error: start time is beyond video length')
			start = ""

	# make sure we found an end time
	while(end == ""):
		print('\nEnter end time (blank defaults to end of video):')
		end = input()
		if end == "":
			print('warning: no end time entered, using end of video')
			end = inVideoLength
		elif not end.isdigit():
			print('error: invalid end time')
			end = ""
		elif float(end) > inVideoLength:
			print('warning: end time entered is beyond video length, using end of video')
			end = inVideoLength

	duration = float(end) - float(start)

	print('\nprocessing clip "' + filename + '" as "'+name+'.'+outFileExt+'", start:', start, 'end:', end, 'duration:', duration) 

	# check if the user included arguments to disable audio or compression
	includeaudio = not args.na
	compressvideo = not args.nc

	# build our list of arguments to send to ffmpeg
	input_args = ['ffmpeg', '-hide_banner', '-loglevel', 'warning', '-ss', str(start), '-i', filename]
	vcodec_args = ['-c:v', 'h264', '-preset', 'fast', '-crf', '22'] if compressvideo else ['-c', 'copy', '-copyinkf'] #vcodec_args = ['-vcodec', 'h264']
	acodec_args = ['-c:a', 'copy'] if includeaudio else ['-an']
	output_args = ['-t', str(duration), name+'.'+outFileExt]

	starttime = time.time()
	exitcode = processVideo(input_args + vcodec_args + acodec_args + output_args)
	timedelta = time.time() - starttime

	print('finished processing video "'+name+'" with exit code', exitcode, 'in %.3f'%(timedelta)+'s')
