# -*- coding: UTF-8 -*-

import wx
import MainFrame
import _thread
import threading

RESOURCES_PATH = "resources/"
SCORE_TEXTS = ["请先驾驶一段时间",
               "建议休息",
               "请小心驾驶",
               "状况良好"]
SCORE_COLORS = [wx.Colour(0, 0, 0),
                wx.Colour(255, 0, 0),
                wx.Colour(255, 128, 0),
                wx.Colour(0, 128, 0)]
ANGRY_ALARM_MODE_LABELS = [u"笑话",
                           u"音乐"]
DRIVER_STATUS_INFORM_GAPS = [5, 10, 15]
DRIVER_STATUS_INFORM_GAP_LABELS = [u"5分钟",
                                   u"10分钟",
                                   u"15分钟"]


# GUI Wrapper class
class GUI(MainFrame.MainFrame):
    def __init__(self, parent):
        MainFrame.MainFrame.__init__(self, parent)
        self.param_config = None

    def switchToScorePanel(self, event):
        if self.config_panel.IsShown():
            # Change icons' color
            self.estimate_bitmap.SetBitmap(wx.Bitmap(RESOURCES_PATH + u"estimate_green_small.png", wx.BITMAP_TYPE_ANY))
            self.estimate_icon_statictext.SetForegroundColour(wx.Colour(0, 128, 0))
            self.estimate_icon_statictext.Refresh()
            self.config_bitmap.SetBitmap(wx.Bitmap(RESOURCES_PATH + u"config_small.png", wx.BITMAP_TYPE_ANY))
            self.config_icon_statictext.SetForegroundColour(wx.Colour(0, 0, 0))
            self.config_icon_statictext.Refresh()

            self.config_panel.Hide()
            self.score_panel.Show()

    def switchToConfigPanel(self, event):
        if self.score_panel.IsShown():
            # Change icons' color
            self.config_bitmap.SetBitmap(wx.Bitmap(RESOURCES_PATH + u"config_green_small.png", wx.BITMAP_TYPE_ANY))
            self.config_icon_statictext.SetForegroundColour(wx.Colour(0, 128, 0))
            self.config_icon_statictext.Refresh()
            self.estimate_bitmap.SetBitmap(wx.Bitmap(RESOURCES_PATH + u"estimate_small.png", wx.BITMAP_TYPE_ANY))
            self.estimate_icon_statictext.SetForegroundColour(wx.Colour(0, 0, 0))
            self.estimate_icon_statictext.Refresh()

            self.score_panel.Hide()
            self.config_panel.Show()

    def changeEnableAngryDetect(self, event):
        self.param_config.setEnableAngryDetect(self.enable_angry_detect_checkbox.GetValue())

    def changeAngryAlarmMode(self, event):
        for i in range(len(ANGRY_ALARM_MODE_LABELS)):
            if event.GetEventObject().GetLabelText() == ANGRY_ALARM_MODE_LABELS[i]:
                self.param_config.setAngryAlarmMode(i)

    def changeDriverStatusInformGap(self, event):
        for i in range(len(DRIVER_STATUS_INFORM_GAP_LABELS)):
            if event.GetEventObject().GetLabelText() == DRIVER_STATUS_INFORM_GAP_LABELS[i]:
                self.param_config.setDriverStatusInformGap(DRIVER_STATUS_INFORM_GAPS[i])

    def setParamConfig(self, param_config):
        self.param_config = param_config

    def setDriverScore(self, score):
        index = 0
        if score < 0:
            pass
        elif score < 60:
            index = 1
        elif score < 80:
            index = 2
        else:
            index = 3
        # Update score
        self.score_statictext.SetLabelText(str(score))
        self.score_statictext.SetForegroundColour(SCORE_COLORS[index])
        self.score_statictext.Refresh()
        # Update score text
        self.score_text_statictext.SetLabelText(SCORE_TEXTS[index])
        self.score_text_statictext.SetForegroundColour(SCORE_COLORS[index])
        self.score_text_statictext.Refresh()
