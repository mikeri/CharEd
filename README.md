#CharEd

A crossplatform wxWidgets based character/font editor for Commodore 64 character sets written in Python. It's been tested on Linux and Windows, with wxPython 2.8 and 3.0.

It only supports hires 1x1 chars, but it has a few useful features:
- Auto create reversed charsets. Copies the first 128 chars to the latter 128 and reverses the latter.
- Import Amiga font files. Only 8x8 bitmap fonts is supported. As far as I know no other similar tools does this.
- Both the standard kernal charsets are included in the editor.

More features hopefully to come soon.

Windows users that does not want to install Python can use the stand alone binary at http://mikeri.net/CharEd.zip, but please note that this is not always up to date.
