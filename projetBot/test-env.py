"""Test module for environment variable. Message come from input() method."""

import os


TOKEN = ''
if os.environ.get('TOKEN'):
    TOKEN = os.environ.get('TOKEN')
    print(TOKEN)
else:
    print('Discord token not defined in environment variable')
    exit('token error')
