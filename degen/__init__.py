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
		nargs = '?', # optional to allow for auto mode
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
	parser.add_argument(
		'-auto',
		'-a',
		action='store_true',
		help = "Automatic mode (look for and process clips based on filename, i.e. "
			   "'degen-11-20-vidname.mp4' would try to find and process 'vidname.mp4' "
			   "with a start time of 11 and end time of 20, and output 'vidname_auto.mp4')"
	)
	return parser

# use ffprobe subprocess to find length of given video
def getLengthInSeconds(filename):
	result = subprocess.Popen(['ffprobe', filename], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
	linesFound = [x for x in result.stdout.readlines() if "Duration".encode() in x] #list comprehension - equiv to: for x in readlines, if duration in x, return x (i.e. add to return list)
	result.kill()
	if len(linesFound) == 0:
		return #print something? does duration matter enough to halt?
	fullDurationStr = linesFound[0].decode().split(",")[0] #isolate "Duration" text section from other text
	timeList = fullDurationStr.split("Duration: ")[1].split(".")
	return sum(x * int(t) for x, t in zip([3600, 60, 1], timeList[0].split(":"))) + (float(timeList[1]) * 0.01)

# finds the first available filename given desired name and extension, appending a number at end of name until one doesn't exist
def getAvailableFilename(filename, fileExt):
	num = 0
	fileStr = filename
	while(os.path.isfile('./' + fileStr + '.' + fileExt) == True): # loop until we find one that doesn't exist
		num += 1
		fileStr = filename + str(num)
	return fileStr

def isVideoFile(file):
	return any(i for i in [(file[-4:] == str) for str in ['.mp4', '.avi']] if i != -1)

# checks if filename is valid, returning a bool,str tuple of whether it's valid and if it's invalid, which character invalidates it
def isValidFilename(filename):
	invalidchars = ['/','\\','?','%','*',':','|','"','<','>']
	for char in invalidchars:
		if char in filename:
			return False, char
	return True, '_'


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
	outFileExt = 'mp4' # always export to .mp4

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

	# check if the user included arguments to disable audio or compression
	if args.na:
		print('disable audio flag found')
	if args.nc:
		print('disable video compression flag found')

	# if auto arg is set, go into auto mode and quit after it's done
	if(args.auto):
		__autoMode(args, outFileExt)
		quit()

	# find file from args
	if args.file == None or os.path.isfile(args.file) == False:
		print('error: file not found')
		quit()

	file = args.file

	# check if file extension matches any from our known list of valid video formats to process
	if not(isVideoFile(file)):
		print('error: file is not a valid video format, aborting')
		quit()

	inVideoLength = getLengthInSeconds(file);

	start = "" if args.start == None else args.start
	end = "" if args.end == None else args.end

	# prompt for a filename for the output video
	name = ""
	while(name == ""):
		print('\nEnter clip name (without extension) (blank defaults "output"):')
		name = input()
		
		if name == "":
			name = getAvailableFilename('output', outFileExt)
			print('warning: no name entered, defaulting to "' + name + '"')
		else:
			# check if name has any invalid filename characters
			valid, char = isValidFilename(name)
			if not valid:
				print("error: invalid character '" + char + "' entered in filename")
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

	print('\n')

	__processVideo(file, outFileExt, start, end, args, name)


# runs ffmpeg subprocess with args on given file
def __processVideo(file, ext, start, end, args, outFilename):
	# build our list of arguments to send to ffmpeg
	includeaudio = not args.na
	compressvideo = not args.nc
	duration = float(end) - float(start)

	input_args = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-ss', str(start), '-i', file]
	vcodec_args = ['-c:v', 'h264', '-preset', 'fast', '-crf', '22'] if compressvideo else ['-c', 'copy', '-copyinkf'] #vcodec_args = ['-vcodec', 'h264']
	acodec_args = ['-c:a', 'copy'] if includeaudio else ['-an']
	output_args = ['-t', str(duration), outFilename+'.'+ext]

	print('processing clip "' + file + '" as "'+outFilename+'.'+ext+'", start:', start, 'end:', end, 'duration:', duration)
	starttime = time.time()

	process = subprocess.Popen(input_args + vcodec_args + acodec_args + output_args, stdout=subprocess.PIPE)
	process.communicate()
	exitcode = process.wait()

	timedelta = time.time() - starttime
	print('finished processing video "'+outFilename+'" with exit code', exitcode, 'in %.3f'%(timedelta)+'s')
	return

def __autoMode(args, ext):
	# find all files that start with our auto syntax ("degen-##-##-") and end with valid video file type
	print('automatic processing mode')
	videoFiles = [file for file in os.listdir(os.getcwd()) if isVideoFile(file)]

	# dict of filename:(starttime,endtime,outfilename)
	filesToProcess = {}
	for file in videoFiles:
		if file.startswith('degen-'):
			split = file.split('-')
			if len(split) >= 4 and split[1].isdigit() and split[2].isdigit():
				dashPositions = [pos for pos, char in enumerate(file) if char == '-'] # get indices of all dash characters in filename
				sanitizedFile = file[dashPositions[2] + 1:] # filename stripped of auto mode text (using this instead of split[3] allows for hyphens in the filename)
				print('found file: ' + sanitizedFile + ', start: ' + split[1] + ', end: ' + split[2])
				filesToProcess[file] = split[1], split[2], sanitizedFile

	for file, params in filesToProcess.items():
		outName = params[2][:-4] + '_auto'
		outExt = params[2][-3:]
		outName = getAvailableFilename(outName, outExt)
		__processVideo(file, ext, params[0], params[1], args, outName)
