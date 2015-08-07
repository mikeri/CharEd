# This is a poor mans config file, the program will currently crash
# is this is not formatted correctly.
# Will hopefully be improved soon!

# C64 color palette
colors = [
        [0,(000,000,000),'black'],
        [1,(255, 255, 255),'white'],
        [2,(104, 055, 043),'red'],
        [3,(112, 164, 178),'cyan'],
        [4,(111, 061, 134),'purple'],
        [5,(80, 141, 067),'green'],
        [6,(040, 040, 121),'blue'],
        [7,(184, 199, 111),'yellow'],
        [8,(111, 79, 037),'orange'],
        [9,(067, 057, 000),'brown'],
        [10,(154, 103, 89),'pink'],
        [11,(68, 68, 68),'dark grey'],
        [12,(108, 108, 108),'grey'],
        [13,(54, 210, 132),'light green'],
        [14,(8, 94, 181),'light blue'],
        [15,(149, 149, 149),'light grey']]

# Name of the file with the code for char pushing. The charset data will be
# appended to this file without load address.
previewprg = 'charedpush.prg'

# Command to run for pushing preview program.
previewcommand = 'x64'

# Default working directory,
workdir = ''

# Temporary file for pushing previews
tempfile = 'chartest.prg'
