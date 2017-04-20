# transcode2H264
Unattended video transcoder to H264 and ACC codecs, in MKV containers.

## What does this do?
This program transcode video files to H264 and AAC in MKV format. Output files are compatible with computers, Blu-ray and HD-players. Subtitles, if present, are automatically detected and soft subbed into the corresponding output files.

## How does it work?
transcode2H264 uses ffmpeg, mkmerge and other system tools to convert the input videos.

## How do I install it?
As a python script you can just run the transcode2H264.py file, or put a symbolic link in any directory of your PATH (e.g. /usr/local/bin)
The script needs ffmpeg and mkvtoolnix to work, so, if it can not find them in your system it will complain and exit.

## Do not many similar programs already exist?
Probably, but I use this. I like it and it works well for me, if you like it too, enjoy it.

## How do I use it?
Just do:
`transcode2H264.py video_file[s]`

It has some options (type `transcode2H264 -h` to see them), but defaults should work in most cases. Maybe you would like to play with the `-l` option, if you are a perfectionist as myself.

## Options
```
Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -p PRESET, --preset=PRESET
                        X264 preset [default: medium].
  -q CRF, --crf=CRF     CRF value [default: 23]. Determines the output video
                        quality. Smaller values gives better qualities and
                        bigger file sizes, bigger values result in less
                        quality and smaller file sizes. Default value results
                        in a nice quality/size ratio. Use crf=18 for
                        transparent (apparent lossless) encoding. CRF values
                        should be in the range of 1 to 50.
  -r, --replace-original-video-file
                        If True original video files will be erased after
                        transcoding [default: False]. WARNING: deleted files
                        can not be easily recovered!
  -l AVLANG, --avlang=AVLANG
                        Audio and video languages for MKV files obtained
                        [default: eng].
  -L SLANG, --slang=SLANG
                        Subtitle language of soft-subbed subtitles [default:
                        spa].
  -x FILENAME_POSTFIX, --filename-postfix=FILENAME_POSTFIX
                        Postfix to be added to newly created H.264 video files
                        [default: _h264].
  -t THREADS, --threads=THREADS
                        Indicates the number of processor cores the script
                        will use. 0 indicates to use as many as possible
                        [default: 0].
  -c, --auto-crop       Autocrop output files [default: False]. WARNING: Use
                        with caution as some video files has variable width
                        horizontal (and vertical) black bars, in those cases
                        you will probably lose data.
```
