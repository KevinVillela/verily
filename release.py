# Run this Script to create a new binary of the Python project that can be run from anywhere.

import PyInstaller.__main__
import os

if __name__ == '__main__':
  PyInstaller.__main__.run([
    '--name=%s' % 'printer.exe',
    '--onefile',
    '--windowed',
    # '--add-binary=%s' % os.path.join('resource', 'path', '*.png'),
    # '--add-data=%s' % os.path.join('resource', 'path', '*.txt'),
    # '--icon=%s' % os.path.join('resource', 'path', 'icon.ico'),
    os.path.join('', 'printer.py'),
   ])