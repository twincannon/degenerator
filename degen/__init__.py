#!/usr/bin/python
import sys
import subprocess
import os
import time
import random
import re
from argparse import ArgumentParser


#extra credit - upload to youtube
#todo - https://trac.ffmpeg.org/wiki/Seeking


def create_parser():
	"""Setup and return our ArgumentParser"""
	parser = ArgumentParser(description = 'The degenerator is a command line '
		'helper that interfaces with ffmpeg to process videos to .mp4 format '
		'for easy upload to platforms like YouTube.\n\n Supply at least 1 '
		'argument of a video file in order to start processing. The second '
		'third arguments found will be used as the clip start/end time from '
		'the input video, though these parameters can also be set at runtime. '
		'ffmpeg is required, which can be found here: '
		'https://www.ffmpeg.org/download.html'
	)
	parser.add_argument(
		'file',
		type = str,
		nargs = '?', # optional to allow for auto mode
		help = 'Input video file to process'
	)
	parser.add_argument(
		'start',
		type = str,
		nargs = '?',
		help = 'Start time in video to clip (optional, supports formatting '
			   'such as "45" or "1:15" or "1m15s")'
	)
	parser.add_argument(
		'end',
		type = str,
		nargs = '?',
		help = 'End time in video to clip (optional, see above)'
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
			   "output 'vidname_auto.mp4' - also supports '1m30s' formatting)"
	)
	return parser


def get_length_in_seconds(filename):
	"""Run ffprobe subprocess and return length of video file"""
	result = subprocess.Popen([_ffmpeg_path + 'ffprobe', filename],
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


def is_mmss_format(time_str):
	"""Checks if string satisfies 'mm:ss' time format"""
	try:
		time.strptime(time_str, '%M:%S')
		return True
	except ValueError:
		return False


def convert_mmss_to_seconds(mm_ss_str):
	"""Converts a string such as 'mm:ss' or '1m30s' returns seconds (integer),
	returns None if failed to convert string. Returns a digit directly.
	"""
	mslist = re.split('m|:', mm_ss_str.lower().rstrip('s'))

	# Handle single numbers by just returning them
	if len(mslist) == 1:
		return mslist[0] if mslist[0].isdigit() else None

	if len(mslist) != 2 or not mslist[0].isdigit() or not mslist[1].isdigit():
		return

	return sum(x * int(t) for x, t in zip([60, 1], mslist))


_OUT_FILE_EXT = 'mp4' # Always export to .mp4
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

_ffmpeg_path = ''

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

	# Check for arguments (first sys.argv is always command executed)
	if len(sys.argv) < 2:
		parser.print_help()
		quit()

	# Check for ffmpeg in path as it's required, or prompt to enter path
	env = os.environ['PATH'].lower()
	if env.find('ffmpeg') == -1:
		print('error: ffmpeg not found in environment PATH!\n'
			  '       ffmpeg can be downloaded from: https://www.ffmpeg.org/download.html\n'
			  '       enter file path to ffmpeg.exe here to try again:')
		found_ffmpeg = False
		while not found_ffmpeg:
			path = input().strip('"')
			path_tests = [
				path,
				path + 'ffmpeg.exe',
				path + '\\' + 'ffmpeg.exe',
			]
			foundpath = [x for x in path_tests if os.path.isfile(x)]
			if len(foundpath) > 0:
				# Sanitize and strip path for later use
				_ffmpeg_path = foundpath[0].strip('"').rstrip('ffmpeg.exe')
				break
			print('\nffmpeg.exe not found. Enter file path to try again:')

	args = parser.parse_args()

	if args.noaudio:
		print('disable audio flag found')
	if args.nocompress:
		print('disable video compression flag found')

	# If auto arg is set, go into auto mode and quit after it's done
	if(args.auto):
		__auto_mode(args, _OUT_FILE_EXT)
		quit()

	if args.file == None or os.path.isfile(args.file) == False:
		print('error: file not found')
		quit()

	file = args.file

	if not(is_video_file(file)):
		print('error: file is not a valid video format, aborting')
		quit()

	in_video_length = get_length_in_seconds(file)

	start = None if args.start == None else convert_mmss_to_seconds(args.start)
	end = None if args.end == None else convert_mmss_to_seconds(args.end)

	# Prompt for a filename for the output video
	name = ""
	while(name == ""):
		print('\nEnter clip name (without extension) (blank defaults "output"):')
		name = input()
		if name == "":
			name = get_available_filename('output', _OUT_FILE_EXT)
			print('warning: no name entered, defaulting to "' + name + '"')
		else:
			# check if name has any invalid filename characters
			valid, char = is_valid_filename(name)
			if not valid:
				print("error: invalid character '" + char + "' entered in filename")
				name = ""

	# Make sure we found a start time
	while(start == None):
		print('\nEnter start time (blank defaults to start of video):')
		start = convert_mmss_to_seconds(input())
		
		if start == None:
			print('warning: invalid start time entered, using start of video')
			start = 0
		elif float(start) > in_video_length:
			print('error: start time is beyond video length ({:.2f})'.format(in_video_length))
			start = None

	# Make sure we found an end time
	while(end == None):
		print('\nEnter end time (blank defaults to end of video):')
		end = convert_mmss_to_seconds(input())

		if end == None:
			print('warning: invalid end time entered, using end of video')
			end = in_video_length
		elif float(end) > in_video_length:
			print('warning: end time is beyond video length, using end of video')
			end = in_video_length

	print()
	__process_video(file, _OUT_FILE_EXT, start, end, args, name)


def __process_video(file, ext, start, end, args, out_filename):
	"""Runs ffmpeg subprocess with args on given file"""
	duration = float(end) - float(start)
	full_filename = out_filename + '.' + ext

	# Build our list of arguments to send to ffmpeg
	input_args = [_ffmpeg_path + 'ffmpeg', '-hide_banner','-loglevel', 'error',
		'-ss', str(start), '-i', file]
	compress_args = ['-c:v', 'h264', '-preset', 'fast', '-crf', '22']
	nocompress_args = ['-c', 'copy', '-copyinkf']
	vcodec_args = nocompress_args if args.nocompress else compress_args
	acodec_args = ['-an'] if args.noaudio else ['-c:a', 'copy']
	output_args = ['-t', str(duration), full_filename]
	ffmpeg_args = input_args + vcodec_args + acodec_args + output_args

	print('processing clip "{}" as "{}", start: {} end: {} '
		  'duration: {:.3f}'.format(file, full_filename, start, end, duration))

	starttime = time.time()
	process = subprocess.Popen(ffmpeg_args, stdout=subprocess.PIPE)
	process.communicate()
	exit_code = process.wait()
	time_delta = time.time() - starttime

	print('finished processing video "{}" with exit code {} '
		  'in {:.1f}s'.format(full_filename, exit_code, time_delta))
	print(random.choice(_ARNOLD_QUOTES))
	return


def __auto_mode(args, ext):
	""" Find all files in local directory whose filenames start with a specific
	string ("degen-##-##-") and end with a valid video type, and then process
	the videos using any supplied optional arguments
	"""
	print('* automatic processing mode *\n')
	video_files = [file for file in os.listdir(os.getcwd()) if is_video_file(file)]

	# Create dict of {filename : (starttime, endtime, outfilename)}
	files_to_process = {}
	for file in video_files:
		if file.startswith('degen-'):
			# Split file str into parts and account for weird dash usage
			splitstr = [str for str  in file.split('-') if len(str) > 0]
			start = splitstr[1].rstrip('s')
			end = splitstr[2].rstrip('s')

			# Support '1m30s' text format in the start/end portions
			if re.match("^[0-9]+m\d{2}(?:s)?$", start):
				temp = start.rstrip('s').split('m')
				start = str(convert_mmss_to_seconds(temp[0]+':'+temp[1]))
			if re.match("^[0-9]+m\d{2}(?:s)?$", end):
				temp = end.rstrip('s').split('m')
				end = str(convert_mmss_to_seconds(temp[0]+':'+temp[1]))

			duration = get_length_in_seconds(file)
			if float(start) > duration:
				print('processing of {} failed: start time {} > duration {}'
					  .format(file, start, duration))
				continue
			elif start > end:
				print('processing of {} failed: start time {} > end time {}'
					  .format(file, start, end))
				continue

			if len(splitstr) >= 4 and start.isdigit() and end.isdigit():
				# Get indices of all dash characters in filename
				dash_pos = [pos for pos, char in enumerate(file) if char == '-']
				# Filename stripped of auto mode text (using this instead
				# of splitstr[3] allows for hyphens in the filename)
				sanitized_file = file[dash_pos[2] + 1:]
				print('found file: {}, start: {}, '
					  'end: {}'.format(sanitized_file, start, end))
				files_to_process[file] = start, end, sanitized_file
	print()

	for file, params in files_to_process.items():
		out_name = params[2][:-4]
		out_ext = params[2][-3:]
		out_name = get_available_filename(out_name, out_ext)
		__process_video(file, ext, params[0], params[1], args, out_name)
		print()
