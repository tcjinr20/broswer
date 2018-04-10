#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
from os import listdir
from os.path import isfile, join
import subprocess



ffmpegpath='.\\bin\\ffmpeg'


def videoToMP4(source_path,out_path):
    format=['.3gp','.mov','.avi','.mkv']
    onlyfiles = [f for f in listdir(source_path) if isfile(join(source_path, f))]
    for file_name in onlyfiles:
        for fn in format:
            file_new=file_name.replace(fn ,'.mp4')
        source_file = join(source_path, file_name)
        out_file = join(out_path, file_new)
        comm = ffmpegpath+' -i {0} -strict -2 {1}'.format(source_file, out_file)
        subprocess.Popen(comm)


def mp4ToHLS(source_path,out_path):
    onlyfiles = [f for f in listdir(source_path) if isfile(join(source_path, f))]
    for file_name in onlyfiles:
        newfilefold = file_name.replace('.mp4', '')
        newout_path=join(out_path,newfilefold)
        if not os.path.exists(newout_path):
            os.makedirs(newout_path)
        source_file = join(source_path, file_name)
        out_file = join(newout_path, newfilefold)
        comm = ffmpegpath+' -i '+source_file+' -codec:v libx264 -codec:a mp3 -map 0 -f ssegment -segment_format mpegts -segment_list '+out_file+'.m3u8 -segment_time 10 '+out_file+'%03d.ts'
        subprocess.Popen(comm)

def addm3u8diamon(diamon,sourcefile,outfile):
    if os.path.exists(outfile):
        return None
    f=open(sourcefile,'r')
    le=f.readline()
    lines = []
    while le:
        le = f.readline()
        if le.strip('\n').endswith('.ts'):
            if(diamon.endswith('/')):
                le = diamon + le
            else:
                le = diamon + "/" + le
        lines.append(le)
    rf = open(outfile,'w')
    rf.writelines(lines)
    rf.close()
    f.close()
    return True

if __name__ =="__main__":

    # videoToMP4(source_path,out_path)
    # mp4ToHLS('v','h')
    # addm3u8diamon('www.baidu.com','l.m3u8','q.m3u8')