from __future__ import unicode_literals
import youtube_dl

class Downloader:
    def __init__(self, url, file_parent_path, file_name):
        self.url = url
        self.file_name = file_name
        self.file_parent_path = file_parent_path
    
    def download_file_from_source(self):
        output_path = self.file_parent_path + '/' + self.file_name
        ydl_opts = {'outtmpl':output_path}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])
