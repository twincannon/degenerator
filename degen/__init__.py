#!/usr/bin/python
import sys
import subprocess
import os
import time
import random
from argparse import ArgumentParser


#extra credit - upload to youtube
#todo - https://trac.ffmpeg.org/wiki/Seeking


def create_parser():
	"""Setup and return our ArgumentParser"""
	parser = ArgumentParser(description = 'Usage: supply at least 1 argument '
		'of a video file in order to start processing. The first two integer '
		'arguments found will be used as the clip start/end time from the '
		'input video, though these parameters can also be set at runtime.'
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
		'-noaudio',
		'-na',
		'-an', # to mirror ffmpeg's parameter
		action = 'store_true',
		help = 'Disable audio in output video'
	)
	parser.add_argument(
		'-nocompress',
		'-nc',
		action = 'store_true',
		help = 'Disable h264 video compression pass'
	)
	parser.add_argument(
		'-auto',
		'-a',
		action = 'store_true',
		help = "Automatic mode (look for and process clips based on filename, "
			   "i.e. 'degen-11-20-vidname.mp4' would try to find and process "
			   "'vidname.mp4' with a start time of 11 and end time of 20, and "
			   "output 'vidname_auto.mp4')"
	)
	return parser


def get_length_in_seconds(filename):
	"""Run ffprobe subprocess and return length of video file"""
	result = subprocess.Popen(['ffprobe', filename],
		stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
	# Isolate "Duration" line from other lines
	duration_line = [x for x in result.stdout.readlines() if "Duration".encode() in x]
	result.kill()
	if len(duration_line) == 0:
		print("error: couldn't get duration (yet we got this far somehow?)")
		return
	# Isolate "Duration" text segment from rest of line
	duration_text = duration_line[0].decode().split(",")[0]
	time = duration_text.split("Duration: ")[1].split(".") # 00:00:00 format
	seconds = sum(x * int(t) for x, t in zip([3600, 60, 1], time[0].split(":")))
	milliseconds = (float(time[1]) * 0.01)
	return seconds + milliseconds


def get_available_filename(filename, file_ext):
	"""Finds the first available filename given desired name and extension,
	appending a number at the end of the name in sequential order until one
	is found that doesn't exist
	"""
	# TODO: make it so if file_ext starts with a period, it strips it
	num = 0
	out_filename = filename
	while(os.path.isfile('./' + out_filename + '.' + file_ext) == True):
		num += 1
		out_filename = filename + str(num)
	return out_filename


def is_video_file(file):
	"""Checks to see if file ends with a valid video extension"""
	return any(i for i in [(file[-4:] == str) for str in ['.mp4', '.avi']] if i != -1)


def is_valid_filename(filename):
	"""Checks if filename is valid, returning a (bool,str) tuple of whether
	it's valid, and if it's invalid, which character invalidates it
	"""
	invalid_chars = ['/','\\','?','%','*',':','|','"','<','>']
	for char in invalid_chars:
		if char in filename:
			return False, char
	return True, '_'


_ARNOLD_QUOTES = [
	"HASTA LA VISTA, CLIPPY",
	"I NEED YOUR CLIPS, YOUR BOOTS, AND YOUR MOTORCYCLE",
	"WHAT IS BEST IN LIFE? TO TAKE YOUR CLIPS, SEE THEM PROCESSED BEFORE "
		"YOU, AND HEAR THE DEGENERATION OF YOUR VIDEOS",
	"I HOPE YOU HAVE ENOUGH ROOM FOR MY CLIP BECAUSE I'M GOING TO RAM IT "
		"INTO YOUR HARD DRIVE",
	"WHO IS YOUR CLIPPY, AND WHAT DOES HE DO",
	"'YOU WERE GONNA PROCESS THAT CLIP?' - OF COURSE, I'M THE DEGENERATOR",
	"COME WITH ME IF YOU WANT TO CLIP",
	"DILLON! YOU SON OF A CLIP",
	"GET TO THE CLIPPA",
	"YOUR CLIP IS DEGENERATED",
	"GET YOUR CLIP TO MARS",
	"I'M A CLIP YOU IDIOT",
	"IF IT DEGENS, WE CAN CLIP IT",
	"CLIP IT, CLIP IT NOW!",
	"I'LL BE CLIP",
]

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
	out_file_ext = 'mp4' # always export to .mp4

	# Check for ffmpeg in path as it's required
	env = os.environ['PATH']
	if env.find('ffmpeg') == -1:
		print('error: ffmpeg not found in path, aborting')
		quit()

	#TODO: browse for ffmpeg if it doesnt exist
	#TODO: safeguard against ffprobe too (though default to check same dir ffmpeg was found in)

	# Check for arguments (first sys.argv is always command executed)
	if len(sys.argv) < 2:
		parser.print_help()
		quit()

	args = parser.parse_args()

	if args.noaudio:
		print('disable audio flag found')
	if args.nocompress:
		print('disable video compression flag found')

	# If auto arg is set, go into auto mode and quit after it's done
	if(args.auto):
		__auto_mode(args, out_file_ext)
		quit()

	if args.file == None or os.path.isfile(args.file) == False:
		print('error: file not found')
		quit()

	file = args.file

	if not(is_video_file(file)):
		print('error: file is not a valid video format, aborting')
		quit()

	in_video_length = get_length_in_seconds(file);

	start = "" if args.start == None else args.start
	end = "" if args.end == None else args.end

	# Prompt for a filename for the output video
	name = ""
	while(name == ""):
		print('\nEnter clip name (without extension) (blank defaults "output"):')
		name = input()
		if name == "":
			name = get_available_filename('output', out_file_ext)
			print('warning: no name entered, defaulting to "' + name + '"')
		else:
			# check if name has any invalid filename characters
			valid, char = is_valid_filename(name)
			if not valid:
				print("error: invalid character '" + char + "' entered in filename")
				name = ""

	# Make sure we found a start time
	while(start == ""):
		print('\nEnter start time (blank defaults to start of video):')
		start = input()
		if start == "":
			print('warning: no start time entered, using start of video')
			start = 0
		elif not start.isdigit():
			print('error: invalid start time')
			start = ""
		elif float(start) > in_video_length:
			print('error: start time is beyond video length')
			start = ""

	# Make sure we found an end time
	while(end == ""):
		print('\nEnter end time (blank defaults to end of video):')
		end = input()
		if end == "":
			print('warning: no end time entered, using end of video')
			end = in_video_length
		elif not end.isdigit():
			print('error: invalid end time')
			end = ""
		elif float(end) > in_video_length:
			print('warning: end time is beyond video length, using end of video')
			end = in_video_length

	print('\n')

	__process_video(file, out_file_ext, start, end, args, name)


def __process_video(file, ext, start, end, args, out_filename):
	"""Runs ffmpeg subprocess with args on given file"""
	duration = float(end) - float(start)

	full_filename = out_filename + '.' + ext

	# Build our list of arguments to send to ffmpeg
	input_args = ['ffmpeg', '-hide_banner','-loglevel', 'error',
		'-ss', str(start), '-i', file]
	compress_args = ['-c:v', 'h264', '-preset', 'fast', '-crf', '22']
	nocompress_args = ['-c', 'copy', '-copyinkf']
	vcodec_args = nocompress_args if args.nocompress else compress_args
	acodec_args = ['-an'] if args.noaudio else ['-c:a', 'copy']
	output_args = ['-t', str(duration), full_filename]
	ffmpeg_args = input_args + vcodec_args + acodec_args + output_args

	print('processing clip "{}" as "{}", start: {} end: {} '
		  'duration: {}'.format(file, full_filename, start, end, duration))

	starttime = time.time()
	process = subprocess.Popen(ffmpeg_args, stdout=subprocess.PIPE)
	process.communicate()
	exit_code = process.wait()
	time_delta = time.time() - starttime

	print('finished processing video "{}" with exit code {} '
		  'in {:.3f}s'.format(full_filename, exit_code, time_delta))
	print(random.choice(_ARNOLD_QUOTES))
	return


def __auto_mode(args, ext):
	""" Find all files in local directory whose filenames start with a specific
	string ("degen-##-##-") and end with a valid video type, and then process
	the videos using any supplied optional arguments
	"""
	print('automatic processing mode')
	video_files = [file for file in os.listdir(os.getcwd()) if is_video_file(file)]

	# Create dict of {filename : (starttime, endtime, outfilename)}
	files_to_process = {}
	for file in video_files:
		if file.startswith('degen-'):
			# Split file str into parts and account for weird dash usage
			split = [str for str  in file.split('-') if len(str) > 0]
			if len(split) >= 4 and split[1].isdigit() and split[2].isdigit():
				# Get indices of all dash characters in filename
				dash_pos = [pos for pos, char in enumerate(file) if char == '-']
				# Filename stripped of auto mode text (using this instead
				# of split[3] allows for hyphens in the filename)
				sanitized_file = file[dash_pos[2] + 1:]
				print('found file: {}, start: {}, '
					  'end: {}'.format(sanitized_file, split[1], split[2]))
				files_to_process[file] = split[1], split[2], sanitized_file

	for file, params in files_to_process.items():
		out_name = params[2][:-4] + '_auto'
		out_ext = params[2][-3:]
		out_name = get_available_filename(out_name, out_ext)
		__process_video(file, ext, params[0], params[1], args, out_name)
