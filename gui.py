# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Sep  8 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.grid

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Char Edit", pos = wx.DefaultPosition, size = wx.Size( 955,606 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.Size( 450,450 ), wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer26 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.bgcolor = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SUNKEN_BORDER )
		
		# Grid
		self.bgcolor.CreateGrid( 2, 8 )
		self.bgcolor.EnableEditing( False )
		self.bgcolor.EnableGridLines( True )
		self.bgcolor.SetGridLineColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DDKSHADOW ) )
		self.bgcolor.EnableDragGridSize( False )
		self.bgcolor.SetMargins( 0, 0 )
		
		# Columns
		self.bgcolor.AutoSizeColumns()
		self.bgcolor.EnableDragColMove( False )
		self.bgcolor.EnableDragColSize( False )
		self.bgcolor.SetColLabelSize( 0 )
		self.bgcolor.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.bgcolor.EnableDragRowSize( False )
		self.bgcolor.SetRowLabelSize( 0 )
		self.bgcolor.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.bgcolor.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		self.bgcolor.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVEBORDER ) )
		self.bgcolor.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVECAPTION ) )
		
		bSizer2.Add( self.bgcolor, 1, wx.ALL, 5 )
		
		self.fgcolor = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SUNKEN_BORDER )
		
		# Grid
		self.fgcolor.CreateGrid( 2, 8 )
		self.fgcolor.EnableEditing( False )
		self.fgcolor.EnableGridLines( True )
		self.fgcolor.SetGridLineColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DDKSHADOW ) )
		self.fgcolor.EnableDragGridSize( False )
		self.fgcolor.SetMargins( 0, 0 )
		
		# Columns
		self.fgcolor.AutoSizeColumns()
		self.fgcolor.EnableDragColMove( False )
		self.fgcolor.EnableDragColSize( False )
		self.fgcolor.SetColLabelSize( 0 )
		self.fgcolor.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.fgcolor.EnableDragRowSize( False )
		self.fgcolor.SetRowLabelSize( 0 )
		self.fgcolor.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.fgcolor.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		self.fgcolor.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVEBORDER ) )
		self.fgcolor.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVECAPTION ) )
		
		bSizer2.Add( self.fgcolor, 1, wx.ALL, 5 )
		
		bSizer26.Add( bSizer2, 0, 0, 5 )
		
		bSizerDraw = wx.BoxSizer( wx.VERTICAL )
		
		self.drawpanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 128,128 ), wx.DOUBLE_BORDER )
		self.drawpanel.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVECAPTION ) )
		self.drawpanel.SetMinSize( wx.Size( 16,16 ) )
		self.drawpanel.SetMaxSize( wx.Size( 1024,1024 ) )
		
		bSizerDraw.Add( self.drawpanel, 1, wx.ALIGN_LEFT|wx.ALIGN_TOP|wx.LEFT|wx.SHAPED, 5 )
		
		bSizer26.Add( bSizerDraw, 1, wx.ALIGN_CENTER|wx.EXPAND, 5 )
		
		bSizer1.Add( bSizer26, 1, wx.EXPAND, 5 )
		
		bSizer25 = wx.BoxSizer( wx.VERTICAL )
		
		charsetChoices = [ u"Upper", u"Lower", u"Custom" ]
		self.charset = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, charsetChoices, 0 )
		self.charset.SetSelection( 0 )
		bSizer25.Add( self.charset, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.charchooser = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 120,-1 ), wx.LC_REPORT )
		self.charchooser.SetMinSize( wx.Size( 120,-1 ) )
		self.charchooser.SetMaxSize( wx.Size( 120,-1 ) )
		
		bSizer7.Add( self.charchooser, 0, wx.ALIGN_RIGHT|wx.EXPAND, 5 )
		
		bSizer25.Add( bSizer7, 1, wx.ALIGN_RIGHT, 5 )
		
		bSizer1.Add( bSizer25, 0, wx.ALIGN_RIGHT|wx.EXPAND, 5 )
		
		self.SetSizer( bSizer1 )
		self.Layout()
		self.m_menubar1 = wx.MenuBar( 0 )
		self.file = wx.Menu()
		self.menuopen = wx.MenuItem( self.file, wx.ID_ANY, u"Open", wx.EmptyString, wx.ITEM_NORMAL )
		self.file.AppendItem( self.menuopen )
		
		self.menusave = wx.MenuItem( self.file, wx.ID_ANY, u"Save", wx.EmptyString, wx.ITEM_NORMAL )
		self.file.AppendItem( self.menusave )
		
		self.saveasmenu = wx.MenuItem( self.file, wx.ID_ANY, u"Save as...", wx.EmptyString, wx.ITEM_NORMAL )
		self.file.AppendItem( self.saveasmenu )
		
		self.menuexit = wx.MenuItem( self.file, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL )
		self.file.AppendItem( self.menuexit )
		
		self.m_menubar1.Append( self.file, u"File" ) 
		
		self.edit = wx.Menu()
		self.copyupmenu = wx.MenuItem( self.edit, wx.ID_ANY, u"Copy all from upper", wx.EmptyString, wx.ITEM_NORMAL )
		self.edit.AppendItem( self.copyupmenu )
		
		self.copylomenu = wx.MenuItem( self.edit, wx.ID_ANY, u"Copy all from lower", wx.EmptyString, wx.ITEM_NORMAL )
		self.edit.AppendItem( self.copylomenu )
		
		self.reversemenu = wx.MenuItem( self.edit, wx.ID_ANY, u"Make reversed chars", wx.EmptyString, wx.ITEM_NORMAL )
		self.edit.AppendItem( self.reversemenu )
		
		self.clearallmenu = wx.MenuItem( self.edit, wx.ID_ANY, u"Clear all chars", wx.EmptyString, wx.ITEM_NORMAL )
		self.edit.AppendItem( self.clearallmenu )
		
		self.m_menubar1.Append( self.edit, u"Edit" ) 
		
		self.SetMenuBar( self.m_menubar1 )
		
		self.statusbar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.bgcolor.Bind( wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.setbgcolor )
		self.bgcolor.Bind( wx.EVT_MOTION, self.colormotion )
		self.fgcolor.Bind( wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.setfgcolor )
		self.fgcolor.Bind( wx.grid.EVT_GRID_RANGE_SELECT, self.colormotion )
		self.drawpanel.Bind( wx.EVT_KEY_DOWN, self.OnLeftDown )
		self.drawpanel.Bind( wx.EVT_KEY_UP, self.OnLeftDown )
		self.drawpanel.Bind( wx.EVT_LEFT_DOWN, self.OnLeftDown )
		self.drawpanel.Bind( wx.EVT_LEFT_UP, self.OnLeftUp )
		self.drawpanel.Bind( wx.EVT_MOTION, self.drawmotion )
		self.charset.Bind( wx.EVT_CHOICE, self.setcharset )
		self.charchooser.Bind( wx.EVT_LIST_ITEM_FOCUSED, self.setchar )
		self.Bind( wx.EVT_MENU, self.openfont, id = self.menuopen.GetId() )
		self.Bind( wx.EVT_MENU, self.savefont, id = self.menusave.GetId() )
		self.Bind( wx.EVT_MENU, self.savefontas, id = self.saveasmenu.GetId() )
		self.Bind( wx.EVT_MENU, self.copyup, id = self.copyupmenu.GetId() )
		self.Bind( wx.EVT_MENU, self.copylo, id = self.copylomenu.GetId() )
		self.Bind( wx.EVT_MENU, self.makereverse, id = self.reversemenu.GetId() )
		self.Bind( wx.EVT_MENU, self.clearall, id = self.clearallmenu.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def setbgcolor( self, event ):
		event.Skip()
	
	def colormotion( self, event ):
		event.Skip()
	
	def setfgcolor( self, event ):
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
	
	def openfont( self, event ):
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
	
	def clearall( self, event ):
		event.Skip()
	
