#!/usr/bin/python
#coding=latin
import wx
import gui
import struct

version = '1.0'
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
bgcolor = 6
fgcolor = 14
drawsize = 0
chars = 0
upchars = 0
lochars = 0
custchars = 0
charbits = []
charnum = 0
blocksize = 0
charfilename = ''
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
        gui.MainFrame.__init__(self,parent)
        col=0
        row=0
        charfile = open("chars.raw",'r')
        orgchars = charfile.read()
        upchars = orgchars[0:2049]
        lochars = orgchars[2048:4096]
        chars = lochars
        custchars = lochars
        self.charbitmaps = []
        for color in colors:
            self.bgcolor.SetCellBackgroundColour(row,col,(colors[color[0]][1]))
            self.fgcolor.SetCellBackgroundColour(row,col,(colors[color[0]][1]))
            col += 1
            if col==8:
                row += 1
                col = 0

        self.Bind(wx.EVT_MENU, self.OnClose, self.menuexit )
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_SIZE, self.OnResize)
        self.drawpanel.Bind(wx.EVT_PAINT, self.on_paint)
        
        self.rendercharset(upchars)
#        self.fgcolor.Bind(wx.EVT_GRID_RANGE_SELECT, self.colormotion) 
#        self.bgcolor.Bind(wx.EVT_GRID_RANGE_SELECT, self.colormotion) 

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
        print('close')
        self.Destroy()

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

    def copyup(self,event):
        global custchars
        global upchars
        custchars = upchars
        self.updatechars()
        self.drawpanel.Refresh()
        event.Skip()

    def copylo(self,event):
        global custchars
        global lochars
        custchars = lochars
        self.updatechars()
        self.drawpanel.Refresh()
        event.Skip()

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
        event.Skip()

    def savechars(self):
        global custchars
        global charfilename
        try:
            charfile = open(charfilename,'w')
            charfile.write(custchars)
            charfile.close()
            self.status('Saved charset ' + charfilename + '.')
        except:
            self.status('Error saving ' + charfilename + '!')

    def savecharsas(self):
        global custchars
        global charfilename
        filereq = wx.FileDialog(self,style=wx.FD_SAVE)
        if filereq.ShowModal() == wx.ID_OK:
            charfilename = filereq.GetPath()
            filename = filereq.GetFilename()
            try:
                charfile = open(charfilename,'w')
                charfile.write(custchars)
                charfile.close()
                self.status('Saved charset ' + filename + '.')
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
        filereq = wx.FileDialog(self,style=wx.FD_OPEN)
        if filereq.ShowModal() == wx.ID_OK:
            charfilename = filereq.GetPath()
            filename = filereq.GetFilename()
            try:
                charfile = open(charfilename,'r')
                custchars = charfile.read()
                charfile.close()
                if len(custchars)<4096:
                    custchars = custchars.ljust(4096 - len(custchars), '\00')
                self.status('Loaded charset ' + filename + '.')
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

    def clearall(self,event):
        global custchars
        clear = '{0:' + chr(0) + '<2048}'
        custchars = clear.format('')
        self.drawpanel.Refresh()
        self.updatechars()
        event.Skip()

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

    def on_paint(self, event):
        global bgcolor
        global fgcolor
        global drawsize
        global blocksize
        global charnum
        def pixeldraw(x, y, state):
            if state: chardraw.SetBrush(wx.Brush(colors[fgcolor][1]))
            else: chardraw.SetBrush(wx.Brush(colors[bgcolor][1]))
            blocksize = drawsize / 8
            chardraw.DrawRectangle(x * blocksize, y * blocksize,
                                                         blocksize + 1,blocksize + 1)
        self.extractchar(charnum)
        #self.charbm = wx.EmptyBitmap(64, 64, 1)
        self.drawpanel.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        chardraw = wx.AutoBufferedPaintDC(self.drawpanel)
        #self.chargfx = wx.GraphicsContext.Create(self.chardraw)
        bgcolorrgb = colors[bgcolor][1]
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

    def setfgcolor( self, event ):
            global fgcolor
            fgcolor = event.GetCol() + 8 * event.GetRow()
            self.Refresh()
            self.status("Foreground color: " + colors[fgcolor][2])
            event.Skip()

    def setbgcolor( self, event ):
            global bgcolor
            bgcolor = event.GetCol() + 8 * event.GetRow()
            self.Refresh()
            self.status("Background color: " + colors[bgcolor][2])
            event.Skip()

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
