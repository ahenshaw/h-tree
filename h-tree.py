import wx
import sys

class HTree(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnErase)

        self.max_level = 12

    def OnErase(self, event):
        pass

    def OnSize(self, event):
        self.Refresh(False)
        self.Update()

    def OnPaint(self, event):
        w, h = self.GetClientSize()
        cx = w // 2
        cy = h // 2
        dc = wx.BufferedPaintDC(self)

        dc.SetBackground(wx.WHITE_BRUSH)
        dc.SetBrush(wx.RED_BRUSH)
        dc.Clear()
        dc.SetPen(wx.BLACK_PEN)
        self.DrawNode(dc, 0, cx, cy, w, h)

    def DrawNode(self, dc, level, x, y, w, h):
        dc.DrawRectangle(x-2, y-2, 5, 5)
        if level == self.max_level:
            return

        if level % 2:
            length = h // 4
            h //= 2
            np0 = (x, y - length)
            np1 = (x, y + length)
            dx = 0
            dy = 2

        else:
            length = w // 4
            w //= 2
            np0 = (x - length, y)
            np1 = (x + length, y)
            dx = 2
            dy = 0
        dc.DrawLine(x-dx, y-dy, *np0)
        dc.DrawLine(x+dx, y+dy, *np1)

        self.DrawNode(dc, level+1, *np0, w, h)
        self.DrawNode(dc, level+1, *np1, w, h)

        
class Frame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title, size=(1000, 700))
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        menuBar = wx.MenuBar()
        menu = wx.Menu()
        m_exit = menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Close window and exit program.")
        self.Bind(wx.EVT_MENU, self.OnClose, m_exit)
        menuBar.Append(menu, "&File")
        # menu = wx.Menu()
        # m_about = menu.Append(wx.ID_ABOUT, "&About", "Information about this program")
        # self.Bind(wx.EVT_MENU, self.OnAbout, m_about)
        # menuBar.Append(menu, "&Help")
        self.SetMenuBar(menuBar)
        
        self.statusbar = self.CreateStatusBar()
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.panel = HTree(self)
        sizer.Add(self.panel, 1, flag=wx.EXPAND)
        self.SetSizer(sizer)


    def OnClose(self, event):
        self.Destroy()

    # def OnAbout(self, event):
    #     dlg = AboutBox()
    #     dlg.ShowModal()
    #     dlg.Destroy()  


app = wx.App(redirect=False)   # Error messages go to popup window
top = Frame("H-Tree")
top.Show()
app.MainLoop()