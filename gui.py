# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Sep  8 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx

ID_EXIT = 1000

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Char Edit", pos = wx.DefaultPosition, size = wx.Size( 600,500 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.Size( 450,450 ), wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.mainpanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer26 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.fgcolor = wx.Panel( self.mainpanel, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.SUNKEN_BORDER|wx.TAB_TRAVERSAL )
		bSizer2.Add( self.fgcolor, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.bgcolor = wx.Panel( self.mainpanel, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.SUNKEN_BORDER )
		bSizer2.Add( self.bgcolor, 1, wx.EXPAND |wx.ALL, 5 )
		
		bSizer26.Add( bSizer2, 1, wx.EXPAND|wx.LEFT, 5 )
		
		bSizerDraw = wx.BoxSizer( wx.VERTICAL )
		
		self.drawpanel = wx.Panel( self.mainpanel, wx.ID_ANY, wx.DefaultPosition, wx.Size( 128,128 ), wx.DOUBLE_BORDER )
		self.drawpanel.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVECAPTION ) )
		self.drawpanel.SetMinSize( wx.Size( 16,16 ) )
		self.drawpanel.SetMaxSize( wx.Size( 1024,1024 ) )
		
		bSizerDraw.Add( self.drawpanel, 1, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.SHAPED, 5 )
		
		bSizer26.Add( bSizerDraw, 6, wx.ALIGN_CENTER|wx.EXPAND, 5 )
		
		bSizer8.Add( bSizer26, 1, wx.EXPAND, 5 )
		
		bSizer25 = wx.BoxSizer( wx.VERTICAL )
		
		charsetChoices = [ u"Upper", u"Lower", u"Editing" ]
		self.charset = wx.Choice( self.mainpanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, charsetChoices, 0 )
		self.charset.SetSelection( 0 )
		bSizer25.Add( self.charset, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.charchooser = wx.ListCtrl( self.mainpanel, wx.ID_ANY, wx.DefaultPosition, wx.Size( 120,-1 ), wx.LC_REPORT )
		self.charchooser.SetMinSize( wx.Size( 120,-1 ) )
		self.charchooser.SetMaxSize( wx.Size( 120,-1 ) )
		
		bSizer7.Add( self.charchooser, 0, wx.ALIGN_RIGHT|wx.EXPAND, 5 )
		
		bSizer25.Add( bSizer7, 1, wx.ALIGN_RIGHT, 5 )
		
		bSizer8.Add( bSizer25, 0, wx.ALIGN_RIGHT|wx.EXPAND, 5 )
		
		self.mainpanel.SetSizer( bSizer8 )
		self.mainpanel.Layout()
		bSizer8.Fit( self.mainpanel )
		bSizer1.Add( self.mainpanel, 1, wx.EXPAND, 5 )
		
		self.SetSizer( bSizer1 )
		self.Layout()
		self.m_menubar1 = wx.MenuBar( 0 )
		self.file = wx.Menu()
		self.newmenu = wx.MenuItem( self.file, wx.ID_ANY, u"New", u"Starts a new charset by clearing all characters.", wx.ITEM_NORMAL )
		self.file.AppendItem( self.newmenu )
		
		self.menuopen = wx.MenuItem( self.file, wx.ID_ANY, u"Open", u"Load raw character bitmap.", wx.ITEM_NORMAL )
		self.file.AppendItem( self.menuopen )
		
		self.importamiga = wx.MenuItem( self.file, wx.ID_ANY, u"Import Amiga font", u"Import 8x8 bitmap font in Amiga format", wx.ITEM_NORMAL )
		self.file.AppendItem( self.importamiga )
		
		self.menusave = wx.MenuItem( self.file, wx.ID_ANY, u"Save", u"Save raw character bitmap.", wx.ITEM_NORMAL )
		self.file.AppendItem( self.menusave )
		
		self.saveasmenu = wx.MenuItem( self.file, wx.ID_ANY, u"Save as...", u"Save raw character bitmap to a chosen file.", wx.ITEM_NORMAL )
		self.file.AppendItem( self.saveasmenu )
		
		self.file.AppendSeparator()
		
		self.loadaddrmenu = wx.MenuItem( self.file, wx.ID_ANY, u"Include load address", u"Toggle if load address is prepended to the character data when saving.\n", wx.ITEM_CHECK )
		self.file.AppendItem( self.loadaddrmenu )
		
		self.loadsubmenu = wx.Menu()
		self.file.AppendSubMenu( self.loadsubmenu, u"Set load address" )
		
		self.file.AppendSeparator()
		
		self.menuexit = wx.MenuItem( self.file, ID_EXIT, u"Exit", u"Exit program.", wx.ITEM_NORMAL )
		self.file.AppendItem( self.menuexit )
		
		self.m_menubar1.Append( self.file, u"File" ) 
		
		self.edit = wx.Menu()
		self.copyupmenu = wx.MenuItem( self.edit, wx.ID_ANY, u"Fill with upper kernal", u"Fill selected characters with the upper case kernal chars.", wx.ITEM_NORMAL )
		self.edit.AppendItem( self.copyupmenu )
		
		self.copylomenu = wx.MenuItem( self.edit, wx.ID_ANY, u"Fill with lower kernal", u"Fill selected characters with the upper/lower case kernal chars.", wx.ITEM_NORMAL )
		self.edit.AppendItem( self.copylomenu )
		
		self.reversemenu = wx.MenuItem( self.edit, wx.ID_ANY, u"Make reversed character set", u"Copy characters 0-127 to 128-255 and reverse them.", wx.ITEM_NORMAL )
		self.edit.AppendItem( self.reversemenu )
		
		self.edit.AppendSeparator()
		
		self.copymenu = wx.MenuItem( self.edit, wx.ID_ANY, u"Copy character"+ u"\t" + u"CTRL-C", u"Copy current character to buffer.", wx.ITEM_NORMAL )
		self.edit.AppendItem( self.copymenu )
		
		self.pastemenu = wx.MenuItem( self.edit, wx.ID_ANY, u"Paste character"+ u"\t" + u"CTRL-V", u"Paste current character to buffer.", wx.ITEM_NORMAL )
		self.edit.AppendItem( self.pastemenu )
		self.pastemenu.Enable( False )
		
		self.edit.AppendSeparator()
		
		self.flipxmenu = wx.MenuItem( self.edit, wx.ID_ANY, u"Flip horizontally"+ u"\t" + u"ALT-X", u"Mirror character along the horizontal axis.", wx.ITEM_NORMAL )
		self.edit.AppendItem( self.flipxmenu )
		
		self.flipymenu = wx.MenuItem( self.edit, wx.ID_ANY, u"Flip vertically"+ u"\t" + u"ALT-Y", u"Mirror character along the vertical axis.", wx.ITEM_NORMAL )
		self.edit.AppendItem( self.flipymenu )
		
		self.reversechmenu = wx.MenuItem( self.edit, wx.ID_ANY, u"Reverse character"+ u"\t" + u"ALT-R", u"Reverse (invert) current character", wx.ITEM_NORMAL )
		self.edit.AppendItem( self.reversechmenu )
		
		self.edit.AppendSeparator()
		
		self.leftmenu = wx.MenuItem( self.edit, wx.ID_ANY, u"Shift left"+ u"\t" + u"ALT-H", u"Shift character one bit to the left", wx.ITEM_NORMAL )
		self.edit.AppendItem( self.leftmenu )
		
		self.rightmenu = wx.MenuItem( self.edit, wx.ID_ANY, u"Shift right"+ u"\t" + u"ALT-L", u"Shift character one bit to the right", wx.ITEM_NORMAL )
		self.edit.AppendItem( self.rightmenu )
		
		self.upmenu = wx.MenuItem( self.edit, wx.ID_ANY, u"Shift up"+ u"\t" + u"ALT-K", u"Shift character one bit up", wx.ITEM_NORMAL )
		self.edit.AppendItem( self.upmenu )
		
		self.downmenu = wx.MenuItem( self.edit, wx.ID_ANY, u"Shift down"+ u"\t" + u"ALT-J", u"Shift character one bit down", wx.ITEM_NORMAL )
		self.edit.AppendItem( self.downmenu )
		
		self.m_menubar1.Append( self.edit, u"Edit" ) 
		
		self.help = wx.Menu()
		self.aboutmenu = wx.MenuItem( self.help, wx.ID_ANY, u"About", wx.EmptyString, wx.ITEM_NORMAL )
		self.help.AppendItem( self.aboutmenu )
		
		self.m_menubar1.Append( self.help, u"Help" ) 
		
		self.SetMenuBar( self.m_menubar1 )
		
		self.statusbar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.fgcolor.Bind( wx.EVT_LEFT_UP, self.setfgcolor )
		self.fgcolor.Bind( wx.EVT_PAINT, self.colorchooser_onpaint )
		self.bgcolor.Bind( wx.EVT_LEFT_DOWN, self.setbgcolor )
		self.bgcolor.Bind( wx.EVT_PAINT, self.colorchooser_onpaint )
		self.drawpanel.Bind( wx.EVT_KEY_DOWN, self.OnLeftDown )
		self.drawpanel.Bind( wx.EVT_KEY_UP, self.OnLeftDown )
		self.drawpanel.Bind( wx.EVT_LEFT_DOWN, self.OnLeftDown )
		self.drawpanel.Bind( wx.EVT_LEFT_UP, self.OnLeftUp )
		self.drawpanel.Bind( wx.EVT_MOTION, self.drawmotion )
		self.charset.Bind( wx.EVT_CHOICE, self.setcharset )
		self.charchooser.Bind( wx.EVT_LIST_ITEM_FOCUSED, self.setchar )
		self.Bind( wx.EVT_MENU, self.new, id = self.newmenu.GetId() )
		self.Bind( wx.EVT_MENU, self.openfont, id = self.menuopen.GetId() )
		self.Bind( wx.EVT_MENU, self.openamiga, id = self.importamiga.GetId() )
		self.Bind( wx.EVT_MENU, self.savefont, id = self.menusave.GetId() )
		self.Bind( wx.EVT_MENU, self.savefontas, id = self.saveasmenu.GetId() )
		self.Bind( wx.EVT_MENU, self.copyup, id = self.copyupmenu.GetId() )
		self.Bind( wx.EVT_MENU, self.copylo, id = self.copylomenu.GetId() )
		self.Bind( wx.EVT_MENU, self.makereverse, id = self.reversemenu.GetId() )
		self.Bind( wx.EVT_MENU, self.copychar, id = self.copymenu.GetId() )
		self.Bind( wx.EVT_MENU, self.pastechar, id = self.pastemenu.GetId() )
		self.Bind( wx.EVT_MENU, self.flipx, id = self.flipxmenu.GetId() )
		self.Bind( wx.EVT_MENU, self.flipy, id = self.flipymenu.GetId() )
		self.Bind( wx.EVT_MENU, self.reversechar, id = self.reversechmenu.GetId() )
		self.Bind( wx.EVT_MENU, self.shift, id = self.leftmenu.GetId() )
		self.Bind( wx.EVT_MENU, self.shift, id = self.rightmenu.GetId() )
		self.Bind( wx.EVT_MENU, self.shift, id = self.upmenu.GetId() )
		self.Bind( wx.EVT_MENU, self.shift, id = self.downmenu.GetId() )
		self.Bind( wx.EVT_MENU, self.onabout, id = self.aboutmenu.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def setfgcolor( self, event ):
		event.Skip()
	
	def colorchooser_onpaint( self, event ):
		event.Skip()
	
	def setbgcolor( self, event ):
		event.Skip()
	
	
	def OnLeftDown( self, event ):
		event.Skip()
	
	
	
	def OnLeftUp( self, event ):
		event.Skip()
	
	def drawmotion( self, event ):
		event.Skip()
	
	def setcharset( self, event ):
		event.Skip()
	
	def setchar( self, event ):
		event.Skip()
	
	def new( self, event ):
		event.Skip()
	
	def openfont( self, event ):
		event.Skip()
	
	def openamiga( self, event ):
		event.Skip()
	
	def savefont( self, event ):
		event.Skip()
	
	def savefontas( self, event ):
		event.Skip()
	
	def copyup( self, event ):
		event.Skip()
	
	def copylo( self, event ):
		event.Skip()
	
	def makereverse( self, event ):
		event.Skip()
	
	def copychar( self, event ):
		event.Skip()
	
	def pastechar( self, event ):
		event.Skip()
	
	def flipx( self, event ):
		event.Skip()
	
	def flipy( self, event ):
		event.Skip()
	
	def reversechar( self, event ):
		event.Skip()
	
	def shift( self, event ):
		event.Skip()
	
	
	
	
	def onabout( self, event ):
		event.Skip()
	

