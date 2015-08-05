#!/usr/bin/python
#coding=latin
import subprocess
import wx
import binascii
import gui
import struct
import config

# All globals go here
version = '1.2'
# Current colors for the editing panel
bgcolor = 6
fgcolor = 14
# Size and the editing panel
drawsize = 0
# Current character buffer
chars = ''
# Upper case C64 kernal characters
upchars = ''
# Upper and lower case C64 kernal characters
lochars = ''
# Character set beeing edited
custchars = ''
# Bit array containing all bits
charbits = []
# Index number of the character beeing edited
charnum = 0
# Real pixel size in editing buffer
blocksize = 0
# Filename of loaded charset
charfilename = ''
# State of drawing (drawing or editing) when holding the mouse button down
drawstate = False

for line in range (0,8):
    charbits.append([0,0,0,0,0,0,0,0])
    
class CharEditFrame(gui.MainFrame):
    def __init__(self,parent):
        global chars
        global upchars
        global custchars
        global lochars
        global charbits
        global version
        self.loadaddrsub = []
        self.changed = False
        gui.MainFrame.__init__(self,parent)
        col=0
        row=0
        charfile = open("chars.raw",'r')
        orgchars = charfile.read()
        upchars = orgchars[0:2049]
        lochars = orgchars[2048:4096]
        chars = lochars
        self.new(None)
        self.charbitmaps = []
        self.fgcolor.name = 'fg'
        self.bgcolor.name = 'bg'

        self.Bind(wx.EVT_MENU, self.OnClose, self.menuexit )
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_SIZE, self.OnResize)
        self.drawpanel.Bind(wx.EVT_PAINT, self.on_paint)
        self.fgcolor.Bind( wx.EVT_LEFT_DOWN, self.setcolor)
        self.bgcolor.Bind( wx.EVT_LEFT_DOWN, self.setcolor)
        
        self.rendercharset(upchars)
#        self.fgcolor.Bind(wx.EVT_GRID_RANGE_SELECT, self.colormotion) 
#        self.bgcolor.Bind(wx.EVT_GRID_RANGE_SELECT, self.colormotion) 
        index = 0
        itemnum = 0
        addresses = ['0800',
                    '2000',
                    '2800',
                    '3000',
                    '3800',
                    '4000',
                    '4800',
                    '5000',
                    '5800',
                    '6000',
                    '6800',
                    '7000',
                    '7800',
                    '8000',
                    '8800',
                    'a000',
                    'a800',
                    'b000',
                    'b800',
                    'c000',
                    'c800',
                    'e000',
                    'e800',
                    'f000',
                    'f800']
        self.loadtable = {}
        for adr in addresses:
            self.loadaddrsub.append (wx.MenuItem( self.loadsubmenu, wx.ID_ANY, u"$" + adr, u"Set load addess for charset", wx.ITEM_NORMAL ))
            index = len(self.loadaddrsub)-1
            self.loadsubmenu.AppendItem( self.loadaddrsub[index])
            self.loadtable[index] = adr
            self.Bind(wx.EVT_MENU, self.setloadaddr, self.loadaddrsub[index] )

    def setloadaddr(self, event):
        for index in range(0,len(self.loadtable)):
            item = event.GetId()
            if item == self.loadaddrsub[index].GetId():
                displayaddr = self.loadtable[index]
                self.loadaddr = bytearray(binascii.unhexlify(self.loadtable[index]))
                self.status('Loadaddress set to: $' + displayaddr)
                self.loadaddrmenu.Check()
        event.Skip()

    def OnResize(self, event):
        self.drawpanel.Refresh()
        self.Refresh()
        event.Skip()

    def onabout(self, event):
        abouttext = 'CharEd version ' + version + """

by mikeri of SCC

http://github.com/mikeri/CharEd
http://mikeri.net
http://shish.org
"""
        wx.MessageBox( abouttext, "About CharEd", wx.OK )
            
    def OnClose(self, event):
        confirm = wx.MessageDialog(self, "Are you sure? Unsaved changes will be lost!")
        if self.changed is True: 
            if confirm.ShowModal() == wx.ID_CANCEL: 
                return
        self.Destroy()

    def flipy(self, event):
        global custchars
        char = custchars[charnum*8:charnum*8+8]
        flipped = char[::-1]
        custchars = custchars[:charnum * 8] + flipped + custchars[(charnum + 1) * 8:]
        self.Refresh()
        self.updatechars()
        self.changed = True
        event.Skip()
            
    def flipx(self, event):
        global custchars
        char = custchars[charnum*8:charnum*8+8]
        flipped = ''
        for byte in char:
            flipped = flipped + chr(int('{:08b}'.format(ord(byte))[::-1], 2))
        custchars = custchars[:charnum * 8] + flipped + custchars[(charnum + 1) * 8:]
        self.Refresh()
        self.updatechars()
        self.changed = True
        event.Skip()

    def shift(self, event):
        global custchars

        def up(char):
            return char[-7:] + char[0]

        def down(char):
            return char[7] + char[:7]

        def left(char):
            shifted = False
            for byte in char:
                byteint = ord(byte) << 1
                if byteint > 255: byteint = (byteint & 255) + 1
                if not shifted:
                    shifted = chr(byteint)
                else:
                    shifted = shifted + chr(byteint)
            return shifted

        def right(char):
            shifted = False
            carry = False
            for byte in char:
                if ord(byte) % 2 > 0 and ord(byte) > 0: carry = True
                byteint = ord(byte) >> 1
                if carry:
                    byteint += 128
                    carry = False
                shiftbyte = chr(byteint)
                if not shifted:
                    shifted = chr(byteint)
                else:
                    shifted = shifted + chr(byteint)
            return shifted

        char = custchars[charnum*8:charnum*8+8]
        item = event.GetId()
        if item == self.upmenu.GetId(): shifted = up(char)
        if item == self.downmenu.GetId(): shifted = down(char)
        if item == self.leftmenu.GetId(): shifted = left(char)
        if item == self.rightmenu.GetId(): shifted = right(char)
        custchars = custchars[:charnum * 8] + shifted + custchars[(charnum + 1) * 8:]
        self.Refresh()
        self.updatechars()
        self.changed = True
        event.Skip()

    def reversechar(self, event):
        global custchars
        char = custchars[charnum*8:charnum*8+8]
        reversedchar = ''
        for byte in char:
            byteval = ord(byte)
            reversedval = ~byteval & 255
            reversedbyte = chr(reversedval)
            reversedchar = reversedchar + reversedbyte
        custchars = custchars[:charnum * 8] + reversedchar + custchars[(charnum + 1) * 8:]
        self.drawpanel.Refresh()
        self.updatechars()
        self.changed = True
        event.Skip()

    def copychar(self, event):
        global custchars
        self.clipbuffer = custchars[charnum*8:charnum*8+8]
        self.pastemenu.Enable()
        event.Skip()

    def pastechar(self, event):
        global custchars
        custchars = custchars[:charnum * 8] + self.clipbuffer + custchars[(charnum + 1) * 8:]
        self.updatechars()
        self.Refresh()
        self.changed = True
        event.Skip()

    def savefont(self, event):
        global charfilename
        if charfilename: self.savechars()
        else: self.savecharsas()
        event.Skip

    def savefontas(self, event):
        self.savecharsas()
        event.Skip

    def openamiga(self, event):
        self.amigaload()
        event.Skip

    def openfont(self, event):
        self.loadchars()
        event.Skip

    def copylo(self,event):
        global custchars
        global upchars
        self.copychars(lochars)
        self.changed = True
        event.Skip()

    def copyup(self,event):
        global custchars
        global upchars
        self.copychars(upchars)
        self.changed = True
        event.Skip()

    def copychars(self, source):
        global custchars
        global upchars
        global lochars
        
        charnum = self.charchooser.GetFirstSelected()
        while True:
            if charnum is -1: break
            char = source[charnum*8:charnum*8+8]
            custchars = custchars[:charnum * 8] + char + custchars[(charnum + 1) * 8:]
            charnum = self.charchooser.GetNextSelected(charnum)

        self.updatechars()
        self.Refresh()

    def status(self, text):
        self.statusbar.SetStatusText(text)
        
    def makereverse(self, event):
        global custchars
        custchars = custchars[:1024]
        for byte in custchars[:1024]:
            byteval = ord(byte)
            reversedval = ~byteval & 255
            reversedbyte = chr(reversedval)
            custchars = custchars + reversedbyte
        self.drawpanel.Refresh()
        self.updatechars()
        self.changed = True
        event.Skip()

    def previewchars(self,event):
        global custchars
        global charfilename
        #TODO load previewprg
        try:
            prevprgfile = open(config.previewprg,'rb')
            previewprg = prevprgfile.read()
            prevprgfile.close()
            charfile = open(config.tempfile,'w')
            charfile.write(previewprg)
            charfile.write(custchars)
            charfile.close()
            subprocess.Popen([config.previewcommand, config.tempfile])

            self.status('Sent charset.')
        except ValueError:
            self.status('Error sending chars!')

    def savechars(self):
        global custchars
        global charfilename
        try:
            charfile = open(charfilename,'w')
            if self.loadaddrmenu.IsChecked():
                charfile.write(self.loadaddr[::-1])
            charfile.write(custchars)
            charfile.close()
            self.status('Saved charset ' + charfilename + '.')
            self.changed = False
        except:
            self.status('Error saving ' + charfilename + '!')

    def savecharsas(self):
        global custchars
        global charfilename
        global workdir
        global loadaddr
        filereq = wx.FileDialog(self,style=wx.FD_SAVE,defaultDir=workdir)
        if filereq.ShowModal() == wx.ID_OK:
            charfilename = filereq.GetPath()
            filename = filereq.GetFilename()
            workdir = filereq.GetDirectory()
            try:
                charfile = open(charfilename,'w')
                if self.loadaddrmenu.IsChecked():
                    charfile.write(self.loadaddr[::-1])
                charfile.write(custchars)
                charfile.close()
                self.status('Saved charset ' + filename + '.')
                self.changed = False
            except:
                self.status('Error saving ' + filename + '!')
        else: self.status('Save cancelled')
        filereq.Destroy()

    def amigaload(self):
        global charfilename
        global custchars
        filereq = wx.FileDialog(self,style=wx.FD_OPEN)
        if filereq.ShowModal() == wx.ID_OK:
            charfilename = filereq.GetPath()
            filename = filereq.GetFilename()
            try:
                charfile = open(charfilename,'r')
                amigafont = charfile.read()
                charfile.close()
            except:
                self.status('Error loading font file!')
            try:
                custbuffer = self.loadamiga(amigafont)
            except:
                self.status('Error importing Amiga font file! Wrong format?')
                return
            custchars = custbuffer
            if len(custchars)<4096:
                custchars = custchars.ljust(4096 - len(custchars), '\00')
            self.status('Imported Amiga font.')
            charfilename = ''
        else: self.status('Load cancelled')
        filereq.Destroy()
        self.updatechars()

    def loadchars(self):
        global charfilename
        global custchars
        global workdir
        filereq = wx.FileDialog(self,style=wx.FD_OPEN,defaultDir=workdir)
        if filereq.ShowModal() == wx.ID_OK:
            charfilename = filereq.GetPath()
            filename = filereq.GetFilename()
            workdir = filereq.GetDirectory()
            try:
                charfile = open(charfilename,'r')
                custchars = charfile.read()
                charfile.close()
                if len(custchars) < 2048:
                    custchars = custchars.ljust(2048, '\00')
                if len(custchars) == 2050:
                    self.loadaddr = bytearray(custchars[:2])[::-1]
                    custchars = custchars[2:]
                    self.status('Loaded charset ' + filename + ' with loaddaress $'
                                  + binascii.hexlify(self.loadaddr) + '.')
                    self.loadaddrmenu.Check(True)
                else:
                    self.status('Loaded charset ' + filename + '.')
                    self.loadaddrmenu.Check(False)
                self.changed = False
            except:
                self.status('Error loading ' + filename + '!')
        else: self.status('Load cancelled')
        filereq.Destroy()
        self.updatechars()

    def rendercharset(self, charset):
        self.charchooser.ClearAll()
        self.charchooser.InsertColumn(0,'Ch',width=25)
        self.charchooser.InsertColumn(1,'Hex',width=35)
        self.charchooser.InsertColumn(2,'Dec',width=35)
        self.imagelist = wx.ImageList(16,16,1)
        self.charchooser.SetImageList(self.imagelist,wx.IMAGE_LIST_SMALL)
        for charnum in range(0,256):
            wxbitmap = wx.BitmapFromBits(charset[charnum*8 : charnum*8+8],8,8,1)
            wximage = wx.ImageFromBitmap(wxbitmap).Scale(16,16).Mirror()
            wxbitmap = wx.BitmapFromImage(wximage,1)
            self.imagelist.Add(wxbitmap)
            pos = self.charchooser.InsertImageItem(charnum,charnum)
            self.charchooser.SetStringItem(pos,1,hex(charnum)[2:])
            self.charchooser.SetStringItem(pos,2,str(charnum))

    def updatechars(self):
        setnum = self.charset.GetSelection()
        if setnum == 2:
            global custchars
            #wxbitmap = wx.BitmapFromBits(chars[charnum*8 : charnum*8+8],8,8,1)
            #wximage = wx.ImageFromBitmap(wxbitmap).Scale(16,16).Mirror()
            #wxbitmap = wx.BitmapFromImage(wximage,1)
            #self.imagelist.Replace(charnum, wxbitmap)
            #self.charchooser.Refresh()

            self.imagelist = wx.ImageList(16,16,1)
            self.charchooser.SetImageList(self.imagelist,wx.IMAGE_LIST_SMALL)
            for charnum in range(0,256):
                wxbitmap = wx.BitmapFromBits(custchars[charnum*8 : charnum*8+8],8,8,1)
                wximage = wx.ImageFromBitmap(wxbitmap).Scale(16,16).Mirror()
                wxbitmap = wx.BitmapFromImage(wximage,1)
                self.imagelist.Add(wxbitmap)
        
    def colormotion(self, event):
        #self.bgcolor.ClearSelection()
        #self.fgcolor.ClearSelection()
        #pass
        event.Skip()

    def new(self,event):
        global custchars
        confirm = wx.MessageDialog(self, "Are you sure? Unsaved changes will be lost!")
        if self.changed is True: 
            if confirm.ShowModal() == wx.ID_CANCEL: 
                return
        custchars = str(bytearray(2048))
        self.drawpanel.Refresh()
        self.updatechars()
        self.changed = False
        charfilename = ''
        if event: event.Skip()

    def OnLeftUp(self, event):
        global charnum
        global charset
        self.updatechars()
        #self.drawpanel.ReleaseMouse()

    def OnLeftDown(self, event):
        global drawstate
        x, y = event.GetPositionTuple()
        x = x / blocksize
        y = y / blocksize
        if self.bitstate(x, y): 
            self.flipbit(x, y, False)
            drawstate = False
        else: 
            self.flipbit(x, y, True)
            drawstate = True
        #self.drawpanel.CaptureMouse()

    def drawmotion(self, event):
        global drawstate
        if event.Dragging() and event.LeftIsDown:
            x, y = event.GetPositionTuple()
            if x > 0 and x < blocksize * 8 and y > 0 and y < blocksize * 8:
                x = x / blocksize
                y = y / blocksize
                if drawstate: self.flipbit(x, y, True)
                else: self.flipbit(x, y, False)

    def bitstate(self, x, y):
        line = charnum * 8 + y
        bits = self.decodebyte(custchars[line])
        return bits[x]
        
    def flipbit(self, x, y, state):
        self.changed = True
        global charnum
        global custchars
        line = custchars[charnum * 8 + y]
        bits = self.decodebyte(line)
        bits[x] = state
        byte = self.encodebyte(bits)
        if y == 0 and charnum == 0:
            custchars = byte + custchars[1:]
        else:
            custchars = custchars[:charnum * 8 + y] + byte + custchars[charnum * 8 + y + 1:]
        #self.updatechar(charnum)
        #self.pixeldraw(x, y, state)
        self.drawpanel.Refresh()

    def encodebyte(self, bits):
        bitval = 1
        bitsum = 0
        for bitpos in reversed(bits):
            if bitpos: bitsum += bitval
            bitval = bitval * 2
        byte = chr(bitsum)
        return byte

    def setcharset(self,event):
        global chars
        global lochars
        global upchars
        setnum = self.charset.GetSelection()
        chardict = {0: upchars,
                    1: lochars,
                    2: custchars}
        self.rendercharset(chardict[setnum])
        chars = chardict[setnum]
        event.Skip()

    def setchar(self, event):
        global charnum
        charnum = event.Index
        if charnum < 0: charnum = 0
        self.extractchar(charnum)
        self.drawpanel.Refresh()
        event.Skip()

    def colorchooser_onpaint(self, event):
        global bgcolor
        global fgcolor

        # Setup
        chooser = event.GetEventObject()
        colorname = chooser.name
        if colorname == 'bg': color = bgcolor
        if colorname == 'fg': color = fgcolor
        chooser.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        dc = wx.AutoBufferedPaintDC(chooser)
        dc.Clear()
        x, y = chooser.GetClientSize()
        x = x / 8 * 8
        y = y / 2 * 2
        xblock = x / 8
        yblock = y / 2
        chooser.SetClientSize((x, y))
    
        for col in range(0,8):
            dc.SetBrush(wx.Brush(config.colors[col][1]))
            xpos = col * xblock
            if xpos == 0: xpos = 1
            dc.DrawRectangle(xpos, 0, xpos + xblock, yblock + 1)
            dc.SetBrush(wx.Brush(config.colors[col+8][1]))
            dc.DrawRectangle(xpos, yblock, xpos + xblock, y) 

        if color < 8:
            cursorxpos = xblock * color
            cursorypos = 1
        else:
            cursorxpos = xblock * (color - 8)
            cursorypos = yblock

        dc.SetPen(wx.Pen(wx.WHITE, 2))
        dc.SetBrush(wx.Brush(wx.WHITE, style=wx.TRANSPARENT))
        dc.DrawRectangle(cursorxpos, cursorypos,
                xblock, yblock) 
        

        #for line in range (0, x, x / 8):
        #    dc.DrawLine(line,0,line,y)
        #dc.DrawLine(0,y/2,x,y/2)

    def on_paint(self, event):
        global bgcolor
        global fgcolor
        global drawsize
        global blocksize
        global charnum

        def pixeldraw(x, y, state):
            if state: chardraw.SetBrush(wx.Brush(config.colors[fgcolor][1]))
            else: chardraw.SetBrush(wx.Brush(config.colors[bgcolor][1]))
            blocksize = drawsize / 8
            chardraw.DrawRectangle(x * blocksize, y * blocksize,
                                                         blocksize + 1,blocksize + 1)
        self.extractchar(charnum)
        #self.charbm = wx.EmptyBitmap(64, 64, 1)
        self.drawpanel.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        chardraw = wx.AutoBufferedPaintDC(self.drawpanel)
        #self.chargfx = wx.GraphicsContext.Create(self.chardraw)
        bgcolorrgb = config.colors[bgcolor][1]
        chardraw.SetBackground(wx.Brush(bgcolorrgb))
        chardraw.Clear()
        x, y = self.drawpanel.GetClientSize()
        x = x / 8 * 8
        self.drawpanel.SetClientSize((x, x))
        drawsize, dummy = self.drawpanel.GetClientSize()
    
        chardraw.SetPen(wx.Pen(wx.BLACK))
        for line in range (0, drawsize, drawsize / 8):
            chardraw.DrawLine(0,line,drawsize,line)
            chardraw.DrawLine(line,0,line,drawsize)

        blocksize = drawsize / 8

        for bit in range (0,8):
            for line in range (0,8):
                pixeldraw(bit,line,charbits[line][bit])

    def setcolor(self, event):
            global fgcolor
            global bgcolor
            xpos, ypos = event.GetPositionTuple()
            chooser = event.GetEventObject()
            colorname = chooser.name
            xsize, ysize = chooser.GetClientSize()
            xzonesize = xsize / 8
            yzonesize = ysize / 2
            colornum = xpos / xzonesize + 8 * (ypos / yzonesize)
            if colorname == 'fg':
                fgcolor = colornum
                self.status("Foreground color: " + config.colors[fgcolor][2])
            if colorname == 'bg': 
                bgcolor = colornum
                self.status("Background color: " + config.colors[bgcolor][2])
            self.Refresh()

    def extractchar(self,charnum):
        global charbits
        global custchars

        char = custchars[charnum * 8:charnum * 8 + 8]
        for linenum in range(0,8):
            line = char[linenum]
            bits = self.decodebyte(line)
            for bit in range(0,8):
                if bits[bit]: charbits[linenum][bit] = True
                else: charbits[linenum][bit] = False

    def decodebyte(self,byte):
        bits = []
        bit = 1
        for pos in range(0, 8):
            bitstate = ord(byte) & int(bit)
            if bitstate > 0: bitstate = True
            else: bitstate = False
            bits.append(bitstate)
            bit = bit << 1
        bits.reverse()
        return bits

    def loadamiga(self,font):
        fontsetting = self.readheader(font)
        if fontsetting['tf_XSize'] == 8 and fontsetting['tf_YSize'] == 8:
            bitmap = ''
            location = []
            charwidth = []
            # Strip header
            font = font[32:]
            lochar = fontsetting['tf_LoChar']
            hichar = fontsetting['tf_HiChar']
            length = fontsetting['tf_Modulo']
            fontpos = fontsetting['tf_CharData']
            charloc = fontsetting['tf_CharLoc']
            numchars = hichar - lochar
            count = 0
            for char in range(0, numchars*4+4, 4):
                data = struct.unpack('>HH',font[char+charloc:char+charloc+4])
                location.append(data[0])
                charwidth.append(data[1])
                count += 1

            fontbits = []
            count = 0
            for char in range(fontpos,fontpos + length * 8):
                count += 1
                bits = self.decodebyte(font[char])
                fontbits += bits


            for char in range(0, numchars):
                for row in range (0, 8):
                    #fetchbyte = location[char]/8 + (length * row)
                    #if char == 0: fetchbyte = 0
                    #dprint(fetchbyte)
                    bitlocation = location[char] + (length * 8 * row)
                    charbits = fontbits[bitlocation:bitlocation+8]
                    #bitmapbyte = font[fetchbyte]
                    bitmapbyte = self.encodebyte(charbits)
                    #bitmap.append(bitmapbyte)
                    bitmap += bitmapbyte
            petsciibitmap = self.asciitopetscii(bitmap, lochar, hichar)
            return petsciibitmap
        else:
            self.status("Font is not 8x8, operation cancelled.")

    def bitarray(data):
        bitarray = []
        for byte in data:
            bits = decodebyte(byte)
            bitarray.append(bits)
        return bitarray

    def readheader(self,font):
        header = font[36:][:106]
        fields = (['ln_Succ'    , 'L'],
                  ['ln_Pred'    , 'L'],
                  ['ln_Type'    , 'B'],
                  ['ln_Pri'     , 'B'],
                  ['ln_fontName', 'L'],
                  ['DFH_ID'     , 'H'],
                  ['Revision'   , 'H'],
                  ['Segment'    , 'L'],
                  ['Fontname'   , '32s'],
                  ['ln_Succ2'   , 'L'],
                  ['ln_Pred2'   , 'L'],
                  ['ln_Type2'   , 'B'],
                  ['ln_Pri2'    , 'B'],
                  ['ln_fontNam2', 'L'],
                  ['mn_ReplyPor', 'L'],
                  ['Reserved'   , 'H'],
                  ['tf_YSize'   , 'H'],
                  ['tf_Style'   , 'B'],
                  ['Flags'      , 'B'],
                  ['tf_XSize'   , 'H'],
                  ['tf_Baseline', 'H'],
                  ['tf_Boldsmea', 'H'],
                  ['tfAccessors', 'H'],
                  ['tf_LoChar'  , 'B'],
                  ['tf_HiChar'  , 'B'],
                  ['tf_CharData', 'L'],
                  ['tf_Modulo'  , 'H'],
                  ['tf_CharLoc' , 'L'],
                  ['tf_CharSpac', 'L'],
                  ['tf_CharKern', 'L'])
        fmtstring = '>'
        for field in fields:
            fmtstring = fmtstring + (field[1])
        values = struct.unpack(fmtstring,header)
        for field in range(0,len(fields)):
            fields[field][1]=values[field]
        return dict(fields)

    def asciitopetscii(self,bitmap,lochar,hichar):
        global outfile
        petsciiorder = '@abcdefghijklmnopqrstuvwxyz[£]^_ !"#$%&\'()*+,-./0123456789:;<=>?\\ABCDEFGHIJKLMNOPQRSTUVWXYZ'.decode('utf-8')
        asciiorder =   ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[£]^_\\abcdefghijklmnopqrstuvwxyz'.decode('utf-8')
        length = len(petsciiorder)
        outchars = []
        offset = 32 - lochar 

        for count in range(0, 255 * 8):
            outchars.append(0)

        count = 0
        for char in petsciiorder:
            asciipos = asciiorder.index(char)

            for line in range(0, 8):
                outchars[count*8+line] = bitmap[asciipos * 8 + line + offset * 8]
            count += 1

        petsciichars = ''.join(outchars[:length*8])
        return petsciichars

app = wx.App(None)
top = CharEditFrame(None)
top.Show()
app.MainLoop()
