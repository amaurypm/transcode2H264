# transcode2H264
Unattended video transcoder to H264 and ACC codecs, in MKV containers.

## What does this do?
This program transcode video files to H264 and AAC in MKV format. Subtitles,
if present, are automatically detected and soft subbed into the corresponding
output files.

## How does it work?
transcode2H264 uses ffmpeg, mkmerge and other system tools to convert the input 
videos.

## How do I install it?
As a python script you can just run the transcode2H264.py file, or put a symbolic link in any directory of your PATH (e.g. /usr/local/bin)
The script needs ffmpeg and mkvtoolnix to work, so, if it can not find them in your system it will complain and exit.

## Do not many similar programs already exist?
Probably, but I use this. I like it and it works well for me, if you like it too, enjoy it.

## How do I use it?
Just do:
`transcode2H264.py video_file[s]`

It has some options (type `transcode2H264 -h` to see them), but defaults should work in most cases. Maybe you would like to play with the `-l` option, if you are a perfectionist as myself.

