#!/usr/bin/env python3
# -*- coding: utf-8 -*-
## A wrapper script to transcode video files to H264, AAC in MKV format, using
## ffmpeg and mkvmerge.
##
## Amaury Pupo Merino
## amaury.pupo@gmail.com
## February 2013
## Modified at May 2014
## Ported to python3 in November 2016.
##
## This small piece of code is released under GPL v3.
##

## Importing modules
import sys
import os
import optparse
import time
import random
import subprocess

## Classes
class Video:
    """Contains actual and proposed video information, and can transforme itself.
    
    """
    def __init__(self,filename):
        self.__in_filename=filename       
        self.__in_ok=False
        self.__in_duration=None
        self.__avlang = None        
        self.__CRF=None
        self.__ext_sub_files=[] # Now a list, for more than one sub files. This files are always kept.
        self.__int_sub_files=[] # Now a list, for more than one sub files. This files are removed after the script is completed.
        self.__sub_charsets={} # Now a dictionary, with each subfile as a key.
        self.__sub_exts=['.srt','.ass','.ssa','.txt']        
        self.__default_avlang='eng'
        self.__default_slang='spa'        
        self.__slangs = {} # To support multiple subtitles.
        self.__ffmpeg_output_ext='.mkv'
        self.__ffmpeg_output_postfix='_tmp-transcode2H264'
        self.__ffmpeg_output=os.path.splitext(self.__in_filename)[0]+self.__ffmpeg_output_postfix+self.__ffmpeg_output_ext
        self.__replace_original=False
        self.__output_postfix=None
        self.__threads=None
        self.__crop_data=None
        self.__get_input_data()

    def __get_input_data(self):
        if os.path.isfile(self.__in_filename):
            #cmd_in_file,cmd_output_error_file=os.popen4("ffmpeg -i \"%s\"" % self.__in_filename) # Depecrated in Python3
            #for line in cmd_output_error_file:   
            cproc = subprocess.run(["ffmpeg", "-i", self.__in_filename], stdout = subprocess.DEVNULL, stderr = subprocess.PIPE, universal_newlines = True)
            for line in cproc.stderr.split('\n'):
                line=line.strip()
                if ('Video' in line) and ('Stream' in line):
                    if 'ansi' not in line:
                        self.__in_ok=True
                    
                if ('Audio' in line) and ('Stream' in line):
                    if '(' in line.split(':')[1]:
                        self.__avlang = line.split(':')[1].split('(')[1].strip(')')
                        if "unk" in self.__avlang.lower() or "und" in self.__avlang.lower():
                            self.__avlang = None
                    
                if 'Duration' in line:
                    duration_string=line.split(',')[0].split()[1]
                    if not 'N/A' in duration_string:
                        self.__in_duration=dstring2dint(duration_string)

    def is_ok(self):
        """Returns true is video file exist and it is actually a video.
        
        """
        return self.__in_ok
    

    def __find_ext_subtitle(self):
        if self.__in_ok:
            subtitle_filename_root=os.path.splitext(self.__in_filename)[0]
            for subtitle_extension in self.__sub_exts:
                subtitle_filename=subtitle_filename_root+subtitle_extension
                if os.path.isfile(subtitle_filename):
                    self.__ext_sub_files.append(subtitle_filename)
                    return

    def __try_to_convert_sub_to_srt(self):
        for sub_file in self.__sub_files:
            subtitle_filename_root,subtitle_filename_ext=os.path.splitext(sub_file)
            
            if subtitle_filename_ext == '.srt':
                continue
            
            srt_sub_file=ass2srt(sub_file)
            if srt_sub_file:
                self.__int_sub_files.append(srt_sub_file)   
                
    def set_transcoding_options(self,crf,replace_original,avlang,slang,postfix,threads,auto_crop):
        if self.__in_ok:
            self.__CRF=crf
            self.__find_ext_subtitle()
            self.__find_int_subtitles()

            self.__replace_original = replace_original            
            self.__default_avlang = avlang
            self.__default_slang = slang
##            self.__sub_exts.append(extra_sub_ext)
            self.__output_postfix = postfix
            self.__threads = threads
            if auto_crop:
                sys.stdout.write('Finding crop dimensions...')
                sys.stdout.flush()
                self.__get_crop_data()
                
            self.__transcoding_options_set = True
            
    def __find_int_subtitles(self):
            n = 1
            in_filename_root,in_filename_ext=os.path.splitext(self.__in_filename)
            if in_filename_ext == '.mkv':
                for line in os.popen("mkvmerge -i \"{}\" -F verbose-text".format(self.__in_filename)):
                    if 'subtitles' in line:
                        track_id=int(line.strip().split(":")[0].split()[-1])
                        sub_type=line.strip().split('(')[1].split(")")[0]
                        slang = line[line.index("language:"):].split(':')[1].split()[0]
                        sub_ext='.srt'
                        if sub_type in ['ASS','SSA', 'SubStationAlpha']:
                            sub_ext='.ass'
                            
                        while(os.path.isfile(in_filename_root+"_"+str(n)+sub_ext)):
                            n+=1
                            
                        sub_filename = in_filename_root+"_"+str(n)+sub_ext
                            
                        os.system("mkvextract tracks \"{}\" {:d}:\"{}\"".format(self.__in_filename, track_id, sub_filename))
                        
                        self.__int_sub_files.append(sub_filename)
                        self.__slangs[sub_filename] = slang
                        
                        
    def transcode(self):
        if self.__transcoding_options_set:
            cmd_line='ffmpeg -i \"{}\" -vcodec libx264 -crf {:d}'.format(self.__in_filename, self.__CRF)
            if self.__crop_data:
                cmd_line+=' -vf crop={}'.format(self.__crop_data)
                
            cmd_line+=' -acodec aac -ar 48k -ab 192k -strict experimental -sn -threads {:d} -y \"{}\"'.format(self.__threads, self.__ffmpeg_output)
            sys.stdout.write('> {}\n'.format(cmd_line))
            exit_code=os.system(cmd_line)
            
            if not exit_code:
                if not self.__create_complete_mkv():
                    return False
                
                if self.__replace_original:
                    sys.stderr.write("WARNING: Deleting file {} as commanded with -r option.\nThis file won't be easily recovered.\n".format(self.__in_filename))
                    os.remove(self.__in_filename)
                        
                return True
        
        return False
    
    def __create_complete_mkv(self):
        if self.__ffmpeg_output:
            ffmpeg_output_root=os.path.splitext(self.__ffmpeg_output)[0].replace(self.__ffmpeg_output_postfix,'')
            mkv_output=ffmpeg_output_root+self.__output_postfix+'.mkv'
            if not self.__avlang:
                self.__avlang = self.__default_avlang
                
            cmd_line="mkvmerge --default-language {} -o \"{}\" \"{}\"".format(self.__avlang,mkv_output,self.__ffmpeg_output)
            sub_files = self.__ext_sub_files + self.__int_sub_files
            if sub_files:
                for sub_file in sub_files:
                    if sub_file in self.__slangs:
                        slang = self.__slangs[sub_file]
                        
                    else:
                        slang = self.__default_slang
                        
                    cmd_line+="  --language 0:{}".format(slang)
                    self.__find_sub_charset(sub_file)
                    if self.__sub_charsets[sub_file]:
                        cmd_line+=" --sub-charset 0:{}".format(self.__sub_charsets[sub_file])
                        
                    cmd_line+=(" \"{}\" ".format(sub_file))
                
                
            sys.stdout.write('> {}\n'.format(cmd_line))
            exit_status=os.system(cmd_line)
            if not exit_status:
                #os.remove(self.__ffmpeg_output)
                #self.__ffmpeg_output=None
                return True        
        
        return False
    
    def __find_sub_charset(self, filename):
        cmd_output=os.popen("file -bi \"{}\" | sed -e 's/.*charset=//'".format(filename))
        for line in cmd_output:
            line=line.strip()
            if line:
                self.__sub_charsets[filename]=line
        
    def __get_crop_data(self):
        crop_data=None
        crop_list=[]
        tmp_output_filename=os.path.splitext(self.__in_filename)[0]+'_tmp_transcode2H264-autocrop.mkv'
        input_duration=self.__in_duration
        if input_duration:
            ss_list=[input_duration/x for x in random.sample(range(1,100),5)] # Cheacking autocrop in 5 random sites in the video.
            for ss in ss_list:
                #cmd_in_file,cmd_output_error_file=os.popen4("ffmpeg -ss %d -i \"%s\" -t 1 -filter cropdetect -y \"%s\"" % (ss,self.__in_filename,tmp_output_filename))
                cproc = subprocess.run(["ffmpeg", "-ss", str(ss), "-i", self.__in_filename, "-t", "1", "-filter", "cropdetect", "-y", tmp_output_filename], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, universal_newlines=True)
                for line in cproc.stderr.split('\n'):
                    line=line.strip()
                    if ('cropdetect' in line) and ('=' in line):
                        crop_list.append(line.split('=')[1])
                        
            os.remove(tmp_output_filename)            
            crop_set=set(crop_list)
            crop_mode_cont=0
            for crop in crop_set:
                if crop_list.count(crop) > crop_mode_cont:
                    crop_data=crop
                    crop_mode_cont=crop_list.count(crop)
            
        sys.stdout.write('{}\n'.format(crop_data))
        self.__crop_data=crop_data
        
    def __purge_int_sub_files(self):
        if self.__int_sub_files:
            for sub_file in self.__int_sub_files:
                print("Removing temporary file '{}'.".format(sub_file))
                os.remove(sub_file)
                
    def clean(self):
        print("Removing temporary file '{}'.".format(self.__ffmpeg_output))
        os.remove(self.__ffmpeg_output)
        self.__ffmpeg_output = None
        self.__purge_int_sub_files()
    
class Reporter:
    """Holds information about the transcoding process and elaborate a final report.
    
    """
    def __init__(self):
        self.__files_ok_counter=0
        self.__files_with_error=[]
        self.__ignored_files=[]
        
    def count_file_ok(self):
        self.__files_ok_counter+=1
        
    def add_file_with_errors(self,filename):
        self.__files_with_error.append(filename)
        
    def add_ignored_file(self,filename):
        self.__ignored_files.append(filename)
        
    def print_final_report(self):
        """Print report after all transcoding is made.
        """
        print('\n==== Transcoding finished ====')
        if self.__ignored_files:
            print ('== There following files were ignored: ==')
            for filename in self.__ignored_files:
                print('\t* {}'.format(filename))
                
            print(75*'=')
            print('\n')
            
        if self.__files_with_error:
            print('== There were errors transcoding the files: ==')
            for filename in self.__files_with_error:
                print('\t* {}'.format(filename))
                
            print(75*'=')
            print('\n')
            
        print('==== Final report ====')
        output='\t {:d} file'.format(self.__files_ok_counter)
        if self.__files_ok_counter!=1:
            output+='s'
            
        output+=' transcoded OK.\n'
        output+='\t {:d} file'.format(len(self.__files_with_error))
                    
        if len(self.__files_with_error)!=1:
            output+='s'
            
        output+=' with errors.\n'
        
        sys.stdout.write(output)
            
        print(75*'=')
        print('\n')

## Functions
def check_the_required_programs():
    if os.system("ffmpeg -h > /dev/null 2>&1"):
        sys.stderr.write("ERROR: ffmpeg is not installed in your system.\nThis script can not work properly without it.\nIf you are using Ubuntu just type:\n\tsudo apt-get install ffmpeg\n\n")
        exit()
        
    if os.system("mkvmerge -h > /dev/null"):
        sys.stderr.write("ERROR: mkvtoolnix is not installed in your system.\nThis script can not work properly without it.\nIf you are using Ubuntu just type:\n\tsudo apt-get install mkvtoolnix\n\n")
        exit()
        
def print_duration(seconds):
    output=''
    seconds_per_minute=60
    seconds_per_hour=60*seconds_per_minute
    seconds_per_day=24*seconds_per_hour
    
    days=int(seconds/seconds_per_day)
    hours=int((seconds % seconds_per_day)/seconds_per_hour)
    minutes=int((seconds % seconds_per_hour)/seconds_per_minute)
    seconds=seconds%60
    
    if days:
        #output+=('%d' % (days))
        output+=('{:d}'.format(days))
        if days==1:
            output+=' day '
            
        else:
            output+=' days '
            
    if hours:
        #output+=('%2d' % (hours))
        output+=('{:2d}'.format(hours))
        if hours==1:
            output+=' hour '
            
        else:
            output+=' hours '
            
    if minutes:
        #output+=('%2d' % (minutes))
        output+=('{:2d}'.format(minutes))
        if minutes==1:
            output+=' minute '
            
        else:
            output+=' minutes '
            
    if seconds:
        #output+=('%4.2f' % (seconds))
        output+=('{:4.2f}'.format(seconds))
        if seconds==1:
            output+=' second '
            
        else:
            output+=' seconds '
                
    return output.strip()

    
def ass2srt(in_filename):
    out_filename=os.path.splitext(in_filename)[0]+'.srt'
    in_file=open(in_filename,'r')
    out_file=open(out_filename,'w')
    dialog_counter=0
    for line in in_file:
        dialog=''
        line=line.strip()
        if line[:9] == 'Dialogue:':
            dialog_counter+=1
            fields=line[10:].split(',')
            ftime=line[10:].split(',')[1]
            ltime=line[10:].split(',')[2]
            for sentence in fields[3:]:
                dialog+=(sentence+',')
                
            dialog=dialog.rstrip(',')
            ftime_hour,ftime_min,ftime_seconds=ftime.split(':')
            ftime_hour,ftime_min=int(ftime_hour),int(ftime_min)
            ftime_seconds,ftime_mseconds=ftime_seconds.split('.')
            ftime_seconds,ftime_mseconds=int(ftime_seconds),int(ftime_mseconds)*10

            ltime_hour,ltime_min,ltime_seconds=ltime.split(':')
            ltime_hour,ltime_min=int(ltime_hour),int(ltime_min)
            ltime_seconds,ltime_mseconds=ltime_seconds.split('.')
            ltime_seconds,ltime_mseconds=int(ltime_seconds),int(ltime_mseconds)*10
            
            output_line="{:d}\n{:02d}:{:02d}:{:02d},{:03d} --> {:02d}:{:02d}:{:02d},{:03d}\n{}\n\n".format(dialog_counter,ftime_hour,ftime_min,ftime_seconds,ftime_mseconds,ltime_hour,ltime_min,ltime_seconds,ltime_mseconds,dialog)
            out_file.write(output_line)
            
    
    in_file.close()
    out_file.close()
    
    return out_filename

def dstring2dint(duration_string):
    hours,minutes,seconds=duration_string.split(':')
    hours,minutes,seconds=int(hours),int(minutes),int(round(float(seconds)))
    duration_seconds=3600*hours+60*minutes+seconds
    return duration_seconds

def run_script():
    """Function to be called to actually run the script.
    """
    check_the_required_programs()
    initial_time=time.time()
    usage="%prog [options] video_file[s]"
    description="This program transcode video files to H264 and AAC in MKV format. Output files are compatible with computers, Blu-ray and HD-players. Subtitles, if present, are automatically detected and soft subbed into the corresponding output files."
    version='%prog 3.0.3'
    parser=optparse.OptionParser(usage=usage,description=description,version=version)
    parser.add_option('-p','--preset',default='medium',help='X264 preset [default: %default].')
    parser.add_option('-q','--crf',type=int,default=23,help='CRF value [default: %default]. Determines the output video quality. Smaller values gives better qualities and bigger file sizes, bigger values result in less quality and smaller file sizes. Default value results in a nice quality/size ratio. Use crf=18 for transparent (apparent lossless) encoding. CRF values should be in the range of 1 to 50.')
    parser.add_option('-r','--replace-original-video-file',action='store_true',default=False,dest='replace',help='If True original video files will be erased after transcoding [default: %default]. WARNING: deleted files can not be easily recovered!')
##    parser.add_option('-s','--add-subtitle',action='store_true',default=False,help='Add subtitles (softly) in the resulting video files. Subtitles are searched in the same location of the video file and they must have the same name of the video and one of the following extensions (in this order): .srt, .ass, .ssa, .txt. The first subtitle found, if any, is added.[default: %default].')    
##    parser.add_option('-e','--extra-subtitle-extension',default='',help='If you want to automatically add a (only one) subtitle extension not included in the script defaults.')
    parser.add_option('-l','--avlang',default='eng',help='Audio and video languages for MKV files obtained [default: %default].')
    parser.add_option('-L','--slang',default='spa',help='Subtitle language of soft-subbed subtitles [default: %default].')
    parser.add_option('-x','--filename-postfix',default='_h264',help='Postfix to be added to newly created H.264 video files [default: %default].')
    parser.add_option('-t','--threads',type=int,default=0,help='Indicates the number of processor cores the script will use. 0 indicates to use as many as possible [default: %default].')
    parser.add_option('-c','--auto-crop',action='store_true',default=False,help='Autocrop output files [default: %default]. WARNING: Use with caution as some video files has variable width horizontal (and vertical) black bars, in those cases you will probably lose data.')    
    
    (options,args)=parser.parse_args()
##    if options.show_devices_and_presets:
##        show_devices_and_presets()
##        exit()
        
    if not len(args):
        parser.error('You need to specify at least one video file.\nSee help (-h, --help) for more options.')
        
    if options.crf < 1 or options.crf > 50:
        parser.error('CRF values should be in the range of 1 to 50.')
        
    if options.threads < 0:
        parser.error('The number of threads must be 0 or possitive.')
        
    reporter=Reporter()
    file_counter=0
    for filename in args:
        file_counter+=1        
        print('\n==== Transcoding file {:d}/{:d} ===='.format(file_counter,len(args)))
        video=Video(filename)
        if not video.is_ok():
            sys.stderr.write("File {} is not a proper video file.\n".format(filename))
            reporter.add_ignored_file(filename)
            continue
        
        video.set_transcoding_options(options.crf,options.replace,options.avlang,options.slang,options.filename_postfix,options.threads,options.auto_crop)
        if video.transcode():
            reporter.count_file_ok()
            
        else:
            reporter.add_file_with_errors(filename)

        video.clean() # Always clean, not only in success, please...
            
        print(75*'=')
            
    reporter.print_final_report()
        
    final_time=time.time()
    
    print('Work finished in {}.'.format(print_duration(final_time-initial_time)))
    print('Exiting OK.')
    
## Running the script
if __name__ == "__main__":
    run_script()
