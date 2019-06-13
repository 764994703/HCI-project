# -*- coding: UTF-8 -*-

import wx
import DriverGUI

RESOURCES_PATH = "resources/"
SCORE_TEXTS = ["请先驾驶一段时间",
               "建议休息",
               "请小心驾驶",
               "状况良好"]
driver_score = -1


# Wrapper class
class MainFrame(DriverGUI.main_frame):
    def __init__(self, parent):
        DriverGUI.main_frame.__init__(self, parent)

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


def main():
    app = wx.App(False)
    frame = MainFrame(None)
    frame.Show(True)
    # Start the applications
    app.MainLoop()


if __name__ == "__main__":
    main()
