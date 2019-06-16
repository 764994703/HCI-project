# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version May 30 2019)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"驾驶员状态评估系统", pos = wx.DefaultPosition, size = wx.Size( 640,480 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.Size( 640,480 ), wx.Size( 640,480 ) )
		self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer1.SetMinSize( wx.Size( 640,480 ) )
		self.base_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 640,480 ), wx.TAB_TRAVERSAL )
		self.base_panel.SetMinSize( wx.Size( 640,480 ) )
		self.base_panel.SetMaxSize( wx.Size( 640,480 ) )

		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		bSizer3.SetMinSize( wx.Size( 640,480 ) )
		self.main_panel = wx.Panel( self.base_panel, wx.ID_ANY, wx.DefaultPosition, wx.Size( 640,320 ), wx.TAB_TRAVERSAL )
		self.main_panel.SetMinSize( wx.Size( 640,320 ) )
		self.main_panel.SetMaxSize( wx.Size( 640,320 ) )

		bSizer22 = wx.BoxSizer( wx.VERTICAL )

		bSizer22.SetMinSize( wx.Size( 640,320 ) )
		self.score_panel = wx.Panel( self.main_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer23 = wx.BoxSizer( wx.VERTICAL )

		bSizer23.SetMinSize( wx.Size( 640,320 ) )
		self.m_staticText17 = wx.StaticText( self.score_panel, wx.ID_ANY, u"您现在的驾驶状态评分是", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17.Wrap( -1 )

		self.m_staticText17.SetFont( wx.Font( 12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微软雅黑" ) )

		bSizer23.Add( self.m_staticText17, 0, wx.ALL, 5 )

		self.score_statictext = wx.StaticText( self.score_panel, wx.ID_ANY, u"无", wx.DefaultPosition, wx.Size( -1,-1 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE )
		self.score_statictext.Wrap( -1 )

		self.score_statictext.SetFont( wx.Font( 120, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微软雅黑" ) )
		self.score_statictext.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )

		bSizer23.Add( self.score_statictext, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

		self.score_text_statictext = wx.StaticText( self.score_panel, wx.ID_ANY, u"请先驾驶一段时间", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE )
		self.score_text_statictext.Wrap( -1 )

		self.score_text_statictext.SetFont( wx.Font( 12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微软雅黑" ) )
		self.score_text_statictext.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

		bSizer23.Add( self.score_text_statictext, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )


		self.score_panel.SetSizer( bSizer23 )
		self.score_panel.Layout()
		bSizer23.Fit( self.score_panel )
		bSizer22.Add( self.score_panel, 1, wx.EXPAND |wx.ALL, 5 )

		self.config_panel = wx.Panel( self.main_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.config_panel.Hide()

		gSizer4 = wx.GridSizer( 1, 2, 0, 0 )

		gSizer4.SetMinSize( wx.Size( 640,320 ) )
		bSizer27 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText11 = wx.StaticText( self.config_panel, wx.ID_ANY, u"路怒监测", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )

		self.m_staticText11.SetFont( wx.Font( 20, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "微软雅黑" ) )

		bSizer27.Add( self.m_staticText11, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.enable_angry_detect_checkbox = wx.CheckBox( self.config_panel, wx.ID_ANY, u"开启", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.enable_angry_detect_checkbox.SetValue(True)
		self.enable_angry_detect_checkbox.SetFont( wx.Font( 16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微软雅黑" ) )

		bSizer27.Add( self.enable_angry_detect_checkbox, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.m_staticText12 = wx.StaticText( self.config_panel, wx.ID_ANY, u"路怒提醒方式", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )

		self.m_staticText12.SetFont( wx.Font( 20, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "微软雅黑" ) )

		bSizer27.Add( self.m_staticText12, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.angry_ratiobutton1 = wx.RadioButton( self.config_panel, wx.ID_ANY, u"笑话", wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
		self.angry_ratiobutton1.SetValue( True )
		self.angry_ratiobutton1.SetFont( wx.Font( 16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微软雅黑" ) )

		bSizer27.Add( self.angry_ratiobutton1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.angry_ratiobutton2 = wx.RadioButton( self.config_panel, wx.ID_ANY, u"音乐", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.angry_ratiobutton2.SetFont( wx.Font( 16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微软雅黑" ) )

		bSizer27.Add( self.angry_ratiobutton2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		gSizer4.Add( bSizer27, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizer28 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText121 = wx.StaticText( self.config_panel, wx.ID_ANY, u"驾驶状态提醒间隔", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText121.Wrap( -1 )

		self.m_staticText121.SetFont( wx.Font( 20, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "微软雅黑" ) )

		bSizer28.Add( self.m_staticText121, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		bSizer29 = wx.BoxSizer( wx.VERTICAL )

		self.driver_status_inform_gap_ratiobutton1 = wx.RadioButton( self.config_panel, wx.ID_ANY, u"5分钟", wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
		self.driver_status_inform_gap_ratiobutton1.SetValue( True )
		self.driver_status_inform_gap_ratiobutton1.SetFont( wx.Font( 16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微软雅黑" ) )

		bSizer29.Add( self.driver_status_inform_gap_ratiobutton1, 0, wx.ALL, 5 )

		self.driver_status_inform_gap_ratiobutton2 = wx.RadioButton( self.config_panel, wx.ID_ANY, u"10分钟", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.driver_status_inform_gap_ratiobutton2.SetFont( wx.Font( 16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微软雅黑" ) )

		bSizer29.Add( self.driver_status_inform_gap_ratiobutton2, 0, wx.ALL, 5 )

		self.driver_status_inform_gap_ratiobutton3 = wx.RadioButton( self.config_panel, wx.ID_ANY, u"15分钟", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.driver_status_inform_gap_ratiobutton3.SetFont( wx.Font( 16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微软雅黑" ) )

		bSizer29.Add( self.driver_status_inform_gap_ratiobutton3, 0, wx.ALL, 5 )


		bSizer28.Add( bSizer29, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )


		gSizer4.Add( bSizer28, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )


		self.config_panel.SetSizer( gSizer4 )
		self.config_panel.Layout()
		gSizer4.Fit( self.config_panel )
		bSizer22.Add( self.config_panel, 1, wx.EXPAND|wx.ALL, 5 )


		self.main_panel.SetSizer( bSizer22 )
		self.main_panel.Layout()
		bSizer3.Add( self.main_panel, 1, wx.EXPAND |wx.ALL, 5 )

		self.menu_panel = wx.Panel( self.base_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.menu_panel.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		gSizer1 = wx.GridSizer( 1, 2, 0, 0 )

		self.estimate_icon_panel = wx.Panel( self.menu_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer6 = wx.BoxSizer( wx.VERTICAL )

		self.estimate_bitmap = wx.StaticBitmap( self.estimate_icon_panel, wx.ID_ANY, wx.Bitmap( u"resources/estimate_green_small.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.estimate_bitmap, 0, wx.ALL, 5 )

		self.estimate_icon_statictext = wx.StaticText( self.estimate_icon_panel, wx.ID_ANY, u"评估", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.estimate_icon_statictext.Wrap( -1 )

		self.estimate_icon_statictext.SetFont( wx.Font( 12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "微软雅黑" ) )
		self.estimate_icon_statictext.SetForegroundColour( wx.Colour( 0, 128, 0 ) )

		bSizer6.Add( self.estimate_icon_statictext, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		self.estimate_icon_panel.SetSizer( bSizer6 )
		self.estimate_icon_panel.Layout()
		bSizer6.Fit( self.estimate_icon_panel )
		gSizer1.Add( self.estimate_icon_panel, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.config_icon_panel = wx.Panel( self.menu_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer61 = wx.BoxSizer( wx.VERTICAL )

		self.config_bitmap = wx.StaticBitmap( self.config_icon_panel, wx.ID_ANY, wx.Bitmap( u"resources/config_small.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.config_bitmap.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		bSizer61.Add( self.config_bitmap, 0, wx.ALL, 5 )

		self.config_icon_statictext = wx.StaticText( self.config_icon_panel, wx.ID_ANY, u"设置", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.config_icon_statictext.Wrap( -1 )

		self.config_icon_statictext.SetFont( wx.Font( 12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "微软雅黑" ) )
		self.config_icon_statictext.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )

		bSizer61.Add( self.config_icon_statictext, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		self.config_icon_panel.SetSizer( bSizer61 )
		self.config_icon_panel.Layout()
		bSizer61.Fit( self.config_icon_panel )
		gSizer1.Add( self.config_icon_panel, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )


		self.menu_panel.SetSizer( gSizer1 )
		self.menu_panel.Layout()
		gSizer1.Fit( self.menu_panel )
		bSizer3.Add( self.menu_panel, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		self.base_panel.SetSizer( bSizer3 )
		self.base_panel.Layout()
		bSizer1.Add( self.base_panel, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.enable_angry_detect_checkbox.Bind( wx.EVT_CHECKBOX, self.changeEnableAngryDetect )
		self.angry_ratiobutton1.Bind( wx.EVT_RADIOBUTTON, self.changeAngryAlarmMode )
		self.angry_ratiobutton2.Bind( wx.EVT_RADIOBUTTON, self.changeAngryAlarmMode )
		self.driver_status_inform_gap_ratiobutton1.Bind( wx.EVT_RADIOBUTTON, self.changeDriverStatusInformGap )
		self.driver_status_inform_gap_ratiobutton2.Bind( wx.EVT_RADIOBUTTON, self.changeDriverStatusInformGap )
		self.driver_status_inform_gap_ratiobutton3.Bind( wx.EVT_RADIOBUTTON, self.changeDriverStatusInformGap )
		self.estimate_icon_panel.Bind( wx.EVT_LEFT_DOWN, self.switchToScorePanel )
		self.estimate_bitmap.Bind( wx.EVT_LEFT_DOWN, self.switchToScorePanel )
		self.estimate_icon_statictext.Bind( wx.EVT_LEFT_DOWN, self.switchToScorePanel )
		self.config_icon_panel.Bind( wx.EVT_LEFT_DOWN, self.switchToConfigPanel )
		self.config_bitmap.Bind( wx.EVT_LEFT_DOWN, self.switchToConfigPanel )
		self.config_icon_statictext.Bind( wx.EVT_LEFT_DOWN, self.switchToConfigPanel )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def changeEnableAngryDetect( self, event ):
		event.Skip()

	def changeAngryAlarmMode( self, event ):
		event.Skip()


	def changeDriverStatusInformGap( self, event ):
		event.Skip()



	def switchToScorePanel( self, event ):
		event.Skip()



	def switchToConfigPanel( self, event ):
		event.Skip()




