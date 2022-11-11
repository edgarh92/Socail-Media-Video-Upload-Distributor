
import os
import subprocess
import datetime
import json
from shutil import which
from typing import List


class VideoProcessor():
    def __init__(self, source_file):
        self.video_file = source_file
        self.video_object = None

    def get_stream_duration(self) -> str:
        stream_duration = None

        for stream in self.video_object['streams']:
            
            if stream["codec_type"] == "video":
                stream_duration = str(stream["duration"])
            elif stream["codec_type"] == "audio":
                stream_duration = str(stream["duration"])

        formated_duration = stream_duration.replace(".", ":")
        return formated_duration

    def parse_stream_data(self) -> str:
        '''Returns JSON of video duration requested from ffprobe'''

        attributes_request = "stream=codec_type,duration,width,height"
        
        stdout, stderr = subprocess.Popen(
            [
                "ffprobe", "-sexagesimal", "-print_format", "json",
                "-show_entries", attributes_request,
                self.video_file, "-sexagesimal"],
                universal_newlines=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
                ).communicate() 
        self.video_object = json.loads(stdout)
        if self.video_object is not None:
            media_duration = self.get_stream_duration()
            if media_duration:
                return media_duration
            else:
                print("No attributes found")
                return None
        else:
            print("No attributes found")
            return None

def installed(program: str) -> bool:
    ''' Check if a program is installed'''
    if which(program):
        return True
    else:
        return False


def format_duration_to_seconds(duration: datetime.timedelta) -> str:
    return duration.total_seconds()


def get_total_duration(video_file_list: List[str]) -> datetime.timedelta:
    """Sum input file durations

    Args:
        video_file_list (List): List of input media files to process

    Returns:
        str: timedelta as string
    Example:
        get_total_duration(['0:00:56.110000'])
    >>>
        timedelta('0:00:56.110000')
    """    
    aggregated_durations = []
    for file in video_file_list:        
        media_duration = VideoProcessor(file).parse_stream_data()
        aggregated_durations.append(media_duration)

    duration_sum = datetime.timedelta()
    for media_duration in aggregated_durations:
        (h, m, s, ms) = media_duration.split(':')

        duration_time_delta = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s),microseconds=int(ms))
        duration_sum += duration_time_delta
    return duration_sum