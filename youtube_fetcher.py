from pytube import YouTube, Playlist
from pytube.cli import on_progress
import os
import re
from os.path import exists


def prepare_outcome(config: dict):
    if not exists(config['download_directory']):
        os.mkdir(config['download_directory'])
    output_folder = config['download_directory']
    if config['create_new_folder_for_each_playlist'] and config['url_type'] == 'playlist':
        output_folder += '/' + config['yid'].replace('/', 'slash')
        if not exists(output_folder):
            os.mkdir(output_folder)
    return output_folder

def download_playlist(config: dict, url: str):
    config.update({
        'url_type': 'playlist',
        'yid': url
    })
    output = prepare_outcome(config)
    playlist = Playlist(url)
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
    print(f'[ i ] Downloading playlist with a total of {len(playlist.video_urls)} videos in it')
    for index, video in enumerate(playlist.videos):
        video.streams.get_highest_resolution().download(output)
        print(f' {index}. - {video._title}  | Downloaded')

def download_video(config: dict, url: str):
    config.update({
        'url_type': 'video'
    })
    output = prepare_outcome(config)
    yt = YouTube(url, on_progress_callback=on_progress)
    yt = yt.streams.filter(progressive=True, file_extension=config['file_extension']).order_by('resolution').desc().first()
    yt.download(output)
