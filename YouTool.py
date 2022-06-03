from sys import argv as args
from os.path import exists
import json
from youtube_fetcher import *

VERSION = 1.0
HELP = f"""
YouTool - {VERSION}
General:
    Download YouTube video's simple

    Thanks for using this product.
    Made by MoMMde and open source on my GitHub
    https://github.com/MoMMde/YouTool

Args:
    help, h:
        You are just reading the output. Nothing more, nothing less.
    <url>:
        URL will be validated, if this video exists, if its a playlist etc...
        Just read what the Programm tells you
    e, exit, ^C, quit, q:
        Exists the program with status code = 0
    c, config, settings, s:
        See the config or modify it
        Example:
            config hello world str
            cmd    key   value type
            
            The key can't contain a ';;' becouse this will count as a new command
"""
SPLITERATOR = '++'
DEBUG = False
ENDED = False
CONFIG_FILE = '.cnfg.json'

config = {
    'file_extension': 'mp4',
    'create_new_folder_for_each_playlist': True,
    'download_directory': './output/'
}

if exists(CONFIG_FILE):
    config = json.load(open(CONFIG_FILE, 'r'))

def write_config(config: dict):
    with open(CONFIG_FILE, 'w') as f:
        f.write(json.dumps(config, indent=4))
        f.close()
        print('Wrote config to file.')

def execute_download_url(url: str):
    path = url.split('/')[-1]
    if path.startswith('playlist'):
        print('[ i ] Recognized Playlist URL -> Downloading as playlist')
        download_playlist(config, url)
    elif path.startswith('watch'):
        print('[ i ] Recognized Watch URL -> Downloding single video')
        download_video(config, url)
    else:
        print('[ i ] Could not recognize any URL pattern: assuming this is just an id')

def run_command(raw_command: str):
    global ENDED
    if raw_command == '' or raw_command == None:
        return
    raw_command = raw_command.split(' ')
    command = raw_command[0].strip()
    c_args = raw_command[1:]
    print(raw_command)
    if DEBUG:
        print(f'[D] Executing {command} {c_args}')
    match command:
        case 'h'|'help'|'?':
            print(HELP)
        case 'c'|'config'|'settings'|'s':
            if len(c_args) >= 1:
                if c_args[0].lower() == 'del':
                    key = c_args[1]
                    if key in config:
                        del config[key]
                        print(f'[ c ] Deleted key: {key}')
                    else:
                        print(f'[ c ] Could not delete key: {key} becouse it doesnt exist.')
                    return
                key, value, v_type = c_args
                if v_type not in ['int', 'str', 'bool', 'dict', 'list']:
                    print('[ c ] Value Type can only be int, str, bool')
                else:
                    print(f'[ c ] Settings {key} to {value} as {v_type}')
                    match v_type:
                        case 'int':
                            value = int(value)
                        case 'bool':
                            value = bool(value)
                    config[key] = value
                    print('[ C ] Updated Successfully... Writing to cache when ending (at least when you end it properly)')
            else:
                print(json.dumps(config, indent=4))
        case 'e'|'exit'|'^C'|'quit'|'q':
            ENDED = True
        case _:
            url = command
            if url.startswith('https://www.youtube.com'):
               execute_download_url(url) 
            else:
                print('[ w ]] Argument does not start with https://youtube.com... aborting => Check your provided URL')

print(f'Welcome to YouTool - {VERSION}')
commands = ' '.join(args[1:]).split(SPLITERATOR)
if len(args) > 1:
    print('[ a ] Given args will be auto-executed as code')
    commands_str = f'commands' if len(commands) > 1 else 'command'
    raw_commands_str = '\n   -> '.join(commands)
    print(f'[ i  ] Found following {commands_str}: \r\n   -> {raw_commands_str}')
    for command in commands:
        run_command(command)

while not ENDED:
    try:
        commands =  input('[ > ] ').split(SPLITERATOR)
        for command in commands:
            run_command(command)
    except Exception as e:
        if DEBUG:
            print(type(e))
            print(e.args)
            print(e)
        print('[ E ] Something went horrible wrong')
        pass

print('[ < ] Ending... Bye')
write_config(config=config)
exit(0)
