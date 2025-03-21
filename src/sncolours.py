import wx
import wx.grid
import os
import json
import pprint

class SaveFile:
  def __init__(self):
    self.filename = ""
    self.name = ""
    self.data = {}
    self.errmsg = "ERROR"
        
  def opensave(self, filename):

    rvalue = True
    
    # JSON file
    f = open(filename, 'r', encoding="utf-8", errors='ignore')
    rd = f.read()
    #print(rd[-1], rd[-10:])
    if rd[-1] == '\x00':
      data = json.loads(rd[:-1])
    else:
      data = json.loads(rd)
    f.close()

    for name in data:
      if name[:12] == "CompleteSave":
        self.name = name

    # Simple check for SnowRunner save
    if self.name == "":
      self.errmsg = "ERROR Invalid save file: " + filename
      rvalue = False
    else:
      self.filename = filename
      self.data = data
        
    return rvalue

  def writesave(self):
    f = open(self.filename, "w", encoding="utf-8")
    json.dump(self.data, f, separators=(',', ':'))
    f.write('\00')
    f.close()

class MainWindow(wx.Frame):
  def __init__(self, title):

    self.dirname = "."
    self.filename = ""
    self.source = SaveFile()
    self.colours = []
    self.grid = None
    
    wx.Frame.__init__(self, None, title=title, size=(1200,800))

    self.statusbar = self.CreateStatusBar() # A Statusbar in the bottom of the window
    self.statusbar.SetFieldsCount(2)
    self.statusbar.SetStatusWidths([-1,-4])

        # Setting up the menu.
    filemenu= wx.Menu()
    menuOpen = filemenu.Append(wx.ID_OPEN, "&Open"," Open a file to view")
    menuSave = filemenu.Append(wx.ID_SAVE, "S&ave"," Save the colours to Snowrunner save file.")
    menuAbout= filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
    menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")

    rowmenu = wx.Menu()
    menuAdd = rowmenu.Append(1001, "Add", "Append a row")
    menuDelete = rowmenu.Append(1002, "Delete", "Delete current selected row")
    menuSort = rowmenu.Append(1003, "Sort", "Sort Rows by ID")
    menuRenumber = rowmenu.Append(1004, "Renumber", "Renumber ID starting with 100")
    
    # Creating the menubar.
    menuBar = wx.MenuBar()
    menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
    menuBar.Append(rowmenu, "Row")
    self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

    self.grid = wx.grid.Grid(self)
    self.grid.CreateGrid(0, 7)
    for i in range(4):
      self.grid.SetColSize(0, 50)   
    for i in range(4,7):
      self.grid.SetColSize(i, 200)
    self.grid.SetColLabelValue(0, "ID")
    self.grid.SetColLabelValue(1, "Tint 1")
    self.grid.SetColLabelValue(2, "Tint 2")
    self.grid.SetColLabelValue(3, "Tint 3")
    self.grid.SetColLabelValue(4, "Tint 1 Text")
    self.grid.SetColLabelValue(5, "Tint 2 Text")
    self.grid.SetColLabelValue(6, "Tint 3 Text")
    
    self.grid.Bind(wx.grid.EVT_GRID_CELL_CHANGING, self.OnChanging)
    self.grid.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.OnChanged)
    self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnLeftClick)
    grid_sizer = wx.BoxSizer(wx.VERTICAL)
    grid_sizer.Add(self.grid, 0, wx.ALL|wx.EXPAND, 5)
    self.SetSizer(grid_sizer)

    # Events.
    self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
    self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
    self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
    self.Bind(wx.EVT_MENU, self.OnSave, menuSave)
    self.Bind(wx.EVT_MENU, self.OnSort, menuSort)
    self.Bind(wx.EVT_MENU, self.OnDelete, menuDelete)
    self.Bind(wx.EVT_MENU, self.OnRenumber, menuRenumber)
    self.Bind(wx.EVT_MENU, self.OnAdd, menuAdd)

    self.statusbar.SetStatusText("0", 0)
    self.statusbar.SetStatusText("None", 1)

    self.Show()

  def OnLeftClick(self, e):
    col = e.GetCol()
    if col < 1 or col > 3:
      e.Skip()
    else:
      row = e.GetRow()
      data = wx.ColourData()
      data.SetColour(self.colours[row]['tints'][col-1])
      dlg = wx.ColourDialog(self, data)
      if dlg.ShowModal() == wx.ID_OK:
        colour = dlg.GetColourData().GetColour()
        self.grid.SetCellValue(row, col+3, colour.GetAsString(wx.C2S_CSS_SYNTAX))
        self.grid.SetCellBackgroundColour(row, col, colour)
        self.grid.Refresh()
        self.colours[row]['tints'][col-1] = colour
    
  def OnAdd(self, e):
    row = self.grid.GetGridCursorRow()
    print(row)
    self.colours.append(self.colours[row])
    self.gridcolours()

  def OnDelete(self, e):
    row = self.grid.GetGridCursorRow()
    print("delete:", row)
    del self.colours[row]
    self.gridcolours()

  def OnRenumber(self, e):
    i = 100
    for c in self.colours:
      c['id'] = i
      i += 1
    self.gridcolours()

  def OnSort(self, e):
    self.colours = sorted(self.colours, key=lambda x: x['id'])
    self.gridcolours()
    
  def OnSave(self, e):
    self.savecolours()

  def OnAbout(self,e):
    # Create a message dialog box
    dlg = wx.MessageDialog(self,
                           " A simple custom colour editor for Snowrunnser save files.\n\n"\
                           "    by Byron Walton\n"\
                           "    bhwcan@netscape.net",
                           "About SnowRunner Colours", wx.OK)
    dlg.ShowModal() # Shows it
    dlg.Destroy() # finally destroy it when finished.

  def OnExit(self,e):
    self.Close(True)  # Close the frame.

  def savecolours(self):

    customColors = {}

    for c in self.colours:
      name = "color"+str(c['id'])

      tints = []
      for i in range(3):
        t = { 'a': 0.0, 'b': float(c['tints'][i].GetBlue()), 'g': float(c['tints'][i].GetGreen()), 'r': float(c['tints'][i].GetRed()) }
        tints.append(t)
        
      customColors[name] = {
        'id': c['id'],
        'gameDataXmlNode': None,
        'overrideMaterialName': 'skin_00',
        'tintsColors': tints,
        'uiName' : c['name'],
        'isSpecialSkin': True,
        'colorType': -10
        }

    #pprint.pprint(customColors)
    self.source.data[self.source.name]['SslValue']['persistentProfileData']['customColors'] = customColors    
    #pprint.pprint(self.source.data)

    self.source.writesave()
    
  def getcolours(self):

    self.colours = []

    if 'customColors' in self.source.data[self.source.name]['SslValue']['persistentProfileData']:
      custom = self.source.data[self.source.name]['SslValue']['persistentProfileData']['customColors']
    else:
      custom = {}

    pprint.pprint(custom)
    
    for c in custom:
      tints = []
      print(c)
      colour = {}
      colour['id'] = custom[c]['id']
      if custom[c]['uiName']:
        colour['name'] = custom[c]['uiName']
      else:
        colour['name'] = c
      i = 0
      for t in custom[c]['tintsColors']:
        uicolour = wx.Colour(int(custom[c]['tintsColors'][i]['r']), \
                             int(custom[c]['tintsColors'][i]['g']), \
                             int(custom[c]['tintsColors'][i]['b']))
                             #int(custom[c]['tintsColors'][i]['a']))
        print(uicolour, uicolour.GetAsString())
        tints.append(uicolour)
        i += 1
      colour['tints'] = tints
      self.colours.append(colour)
    #self.colours = sorted(self.colours, key=lambda x: x['id'])

    pprint.pprint(self.colours)
    self.gridcolours()

  def gridcolours(self):
    numcolours = len(self.colours)
    numrows = self.grid.GetNumberRows()

    print("colours:", numcolours, "rows:", numrows)
    
    if numcolours > numrows:
      self.grid.AppendRows(numcolours - numrows)
      
    if numrows > numcolours:
      self.grid.DeleteRows(0, numrows - numcolours)
      
    for row in range(numcolours):
      self.grid.SetCellValue(row, 0, str(self.colours[row]['id']))
      #self.grid.SetReadOnly(row, 0)
      for c in range(3):
        #print(self.colours[row]['tints'][c])
        self.grid.SetCellBackgroundColour(row, c+1, self.colours[row]['tints'][c])
        self.grid.SetReadOnly(row, c+1)
        #self.grid.SetCellBackgroundColour(row, c+1, wx.RED)
        #print(wx.RED)
      for t in range(3):
        self.grid.SetCellValue(row, t+4, self.colours[row]['tints'][t].GetAsString(wx.C2S_CSS_SYNTAX))
        
    self.statusbar.SetStatusText(str(numcolours), 0)
    self.Layout()

  def OnChanging(self, e):
    row = e.GetRow()
    col = e.GetCol()
    if col > 3:
      colour = e.GetString()
      print(row, col, colour)
      if self.colours[row]['tints'][col-4].Set(colour):
        print(self.colours[row]['tints'][col-4].GetAsString(wx.C2S_CSS_SYNTAX))
        #self.grid.SetCellBackgroundColour(row, col-3, self.colours[row]['tints'][col-4])
        #self.grid.SetCellValue(row, col, self.colours[row]['tints'][col-4].GetAsString())
      else:
        e.Veto()
    else:
      used = False
      try:
        id = int(e.GetString())
      except:
        id = 0
      for c in self.colours:
        if id == c['id']:
          used = True
          break
      if used or id < 100 or id > 999:
        e.Veto()
      else:
        self.colours[row]['id'] = id
    e.Skip()

  def OnChanged(self, e):
    row = e.GetRow()
    col = e.GetCol()
    #print(row, col, e.GetString)
    if col > 3:
      self.grid.SetCellValue(row, col, self.colours[row]['tints'][col-4].GetAsString(wx.C2S_CSS_SYNTAX))
      self.grid.SetCellBackgroundColour(row, col-3, self.colours[row]['tints'][col-4])
      self.grid.Refresh()
    else:
      self.grid.SetCellValue(row, 0, str(self.colours[row]['id']))
    #self.gridcolours()
      
  def OnOpen(self,e):
    """ Open a file"""
    filename = None
    dlg = wx.FileDialog(self, "Open Save file", self.dirname, "", "CompleteSave*", wx.FD_OPEN)
    if dlg.ShowModal() == wx.ID_OK:
      self.filename = dlg.GetFilename()
      self.dirname = dlg.GetDirectory()
      filename = os.path.join(self.dirname, self.filename)
      print(self.dirname, self.filename)
    dlg.Destroy()
    if filename:
      if self.source.opensave(filename):
        self.statusbar.SetStatusText(filename, 1)
        self.getcolours()
      else:
        self.statusbar.SetStatusText(self.source.errmsg)
 
# MAIN
# ----
app = wx.App(False)
frame = MainWindow("SnowRunner Colours")
app.MainLoop()
    
