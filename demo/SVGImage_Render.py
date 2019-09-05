
import os
import glob
import wx
from wx.svg import SVGimage

#----------------------------------------------------------------------

class SVGRenderPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.FULL_REPAINT_ON_RESIZE)

        self._renderer = None
        self._img = None

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)


    def SetRenderer(self, renderer):
        self._renderer = renderer
        self.Refresh()


    def SetSVGFile(self, svg_filename):
        self._img = SVGimage.CreateFromFile(svg_filename)
        self.Refresh()


    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.Clear()

        iw, ih = (self._img.width, self._img.height) if self._img else (100,100)
        dcdim = min(self.Size.width, self.Size.height)
        imgdim = min(iw, ih)
        scale = dcdim / imgdim
        width = int(iw * scale)
        height = int(ih * scale)

        dc.SetBrush(wx.Brush('white'))
        dc.DrawRectangle(0,0, width, height)

        if self._renderer and self._img:
            ctx = self._renderer.CreateContext(dc)
            self._img.RenderToGC(ctx, scale)



#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        self.listbox = wx.ListBox(self, style=wx.LB_SINGLE, size=(250, -1))
        self.listbox.AppendItems(glob.glob(os.path.join('data', '*.svg')))

        self.renderPanel = SVGRenderPanel(self)
        rightSizer = wx.BoxSizer(wx.VERTICAL)
        rightSizer.Add(self.renderPanel, wx.SizerFlags(1).Expand())

        self.Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.Sizer.Add(self.listbox, wx.SizerFlags(1).Border(wx.ALL, 10).Expand())
        self.Sizer.Add(rightSizer, wx.SizerFlags(2).Border(wx.RIGHT|wx.BOTTOM|wx.TOP, 10).Expand())

        self.Bind(wx.EVT_LISTBOX, self.OnSelectItem)
        self.listbox.SetSelection(0)

        # TODO: Add ability for the user to select the renderer
        if 'wxMSW' in wx.PlatformInfo:
            renderer = wx.GraphicsRenderer.GetDirect2DRenderer()
            # renderer = wx.GraphicsRenderer.GetCairoRenderer()
        else:
            renderer = wx.GraphicsRenderer.GetDefaultRenderer()
        self.renderPanel.SetRenderer(renderer)

        # Load the first SVG in the list into the static bitmaps
        self.renderPanel.SetSVGFile(self.listbox.GetString(0))


    def OnSelectItem(self, evt):
        filename = self.listbox.GetStringSelection()
        self.renderPanel.SetSVGFile(filename)


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>SVGImage</center></h2>

The wx.svg.SVGimage class provides the ability to load, parse and render
Scalable Vector Graphics (SVG) files. The advantage of SVG files is that
they can be used to create bitmaps of any size without loss of quality.

This sample demonstrates rendering an SVG image directly on to a
wx.GraphicsContext using the GC's daring capabilities.

</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

