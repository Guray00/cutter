#!/usr/bin/env python3

import sys, re, os, tempfile

def elaborate(input_file, ffmpeg_cmd, n=-40, d=0.8):
	selectionsList = []
	timeSelection = "between(t,0,"
	filename = inputFile = end = start = None
 
	tmp_path= tempfile.gettempdir()
	tmp = f'{tmp_path}/remsi.txt'
	command = f'{ffmpeg_cmd} -i "{input_file}" -hide_banner -af silencedetect=n={n}dB:d={d} -preset ultrafast -f null -  > {tmp} 2>&1'
	os.system(command)
 
	file_stream = open(f"{tmp}", "r")

	# read standard input once, line by line
	for line in file_stream.readlines():
		# detect a start of silence, which is an end of our selection
		end = re.search(r"silence_start: (\d+\.?\d+)", line)
		# detect an end of silence, which is a start of our selection
		start = re.search(r"silence_end: (\d+\.?\d+)", line)

		if filename is None:
			# find the input filename
			filename = re.search(r"Input .+ from '(.+)':", line)
		else:
			if inputFile is None:
				inputFile = filename.group(1)

		if start is not None:
			timeSelection = "between(t," + start.group(1) + ","
		if end is not None:
			timeSelection += end.group(1) + ")"
			selectionsList.append(timeSelection)

	file_stream.close()
	# Note: silencedetect apparently handles properly files that start and/or end in silence
	# so we don't need to check for that and complete filters with no start or no end
	selectionFilter = "'" + "+".join(selectionsList) + "'"

	tmp_path= tempfile.gettempdir()

	# file audio
	text_file = open(f"{tmp_path}/afilter.txt", "w") 
	text_file.write(f"afftdn=nr=10:nf={n}:tn=1, aselect=" + selectionFilter + ",asetpts=N/SR/TB" ) 
	text_file.close()

	# file video
	text_file = open(f"{tmp_path}/vfilter.txt", "w") 
	text_file.write("select=" + selectionFilter + ",setpts=N/FRAME_RATE/TB") 
	text_file.close()
	
	if (os.path.exists(tmp)):
		os.remove(tmp)
	
 
 
 
"""
MIT License

Copyright (c) 2022 Emmanuel Bégué

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. 
"""
