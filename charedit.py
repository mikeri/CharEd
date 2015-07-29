#!/usr/bin/python
import wx
import gui

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
        [10,(154, 103, 89),'light red'],
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

for line in range (0,8):
    charbits.append([0,0,0,0,0,0,0,0])
    
class CharEditFrame(gui.MainFrame):
    def __init__(self,parent):
        global chars
        global upchars
        global custchars
        global lochars
        global charbits
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
        self.Bind(wx.EVT_PAINT, self.on_paint)
        
        self.rendercharset(upchars)
#        self.fgcolor.Bind(wx.EVT_GRID_RANGE_SELECT, self.colormotion) 
#        self.bgcolor.Bind(wx.EVT_GRID_RANGE_SELECT, self.colormotion) 

    def OnClose(self, event):
        self.Destroy()

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

    def updatechar(self, charnum):
        setnum = self.charset.GetSelection()
        if setnum == 2:
            global custchars
            wxbitmap = wx.BitmapFromBits(chars[charnum*8 : charnum*8+8],8,8,1)
            wximage = wx.ImageFromBitmap(wxbitmap).Scale(16,16).Mirror()
            wxbitmap = wx.BitmapFromImage(wximage,1)
            self.imagelist.Replace(charnum, wxbitmap)
            self.charchooser.RefreshItem(charnum)
        
    def colormotion(self, event):
        #self.bgcolor.ClearSelection()
        #self.fgcolor.ClearSelection()
        #pass
        event.Skip()

    def OnLeftDown(self, event):
        x, y = event.GetPositionTuple()
        x = x / blocksize
        y = y / blocksize
        if self.bitstate(x, y): self.flipbit(x, y, False)
        else: self.flipbit(x, y, True)
        #self.CaptureMouse()
        #event.skip()

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
        self.updatechar(charnum)
        self.pixeldraw(x, y, state)

    def pixeldraw(self, x, y, state):
        chardraw = wx.AutoBufferedPaintDC(self.drawpanel)
        if state: chardraw.SetBrush(wx.Brush(colors[fgcolor][1]))
        else: chardraw.SetBrush(wx.Brush(colors[bgcolor][1]))
        blocksize = drawsize / 8
        chardraw.DrawRectangle(x * blocksize, y * blocksize,
                               blocksize + 1,blocksize + 1)

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
        self.Refresh()
        event.Skip()

    def setchar(self, event):
        global charnum
        charnum = event.Index
        if charnum < 0: charnum = 0
        self.extractchar(charnum)
        self.Refresh()
        event.Skip()

    def on_paint(self, event):
        global bgcolor
        global fgcolor
        global drawsize
        global blocksize
        global charnum
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
    
        for line in range (0, drawsize, drawsize / 8):
            chardraw.SetPen(wx.Pen(wx.BLACK))
            chardraw.DrawLine(0,line,drawsize,line)
            chardraw.DrawLine(line,0,line,drawsize)

        chardraw.SetBrush(wx.Brush(colors[fgcolor][1]))
        blocksize = drawsize / 8

        for bit in range (0,8):
            for line in range (0,8):
                if charbits[line][bit]:
                    chardraw.DrawRectangle(bit * blocksize, line * blocksize,
                                           blocksize + 1,blocksize + 1)

    def setfgcolor( self, event ):
            global fgcolor
            fgcolor = event.GetCol() + 8 * event.GetRow()
            self.Refresh()
            event.Skip()

    def setbgcolor( self, event ):
            global bgcolor
            bgcolor = event.GetCol() + 8 * event.GetRow()
            self.Refresh()
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

app = wx.App()# Error messages go to popup window
top = CharEditFrame(None)
top.Show()
app.MainLoop()
