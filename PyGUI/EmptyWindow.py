import wx

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title="Empty Window")
        self.Bind(wx.EVT_CLOSE, self.OnClose)
    
    def OnClose(self, event):
        if wx.MessageBox("Close Window?", "OK", wx.YES_NO) \
            != wx.YES:
            event.Skip(False)
        else:
            self.Destroy()

if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame()
    frame.Show()

    app.MainLoop()