# -*- coding: utf-8 -*-
"""
Created on Fri May 22 09:58:08 2020

@author: Dell
"""

from PIL import Image   

# Use the wxPython backend of matplotlib
import matplotlib       
matplotlib.use('WXAgg')

# Matplotlib elements used to draw the bounding rectangle
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.patches import Rectangle
from matplotlib.patches import Arrow
from matplotlib.patches import Circle
from matplotlib.lines import Line2D
import matplotlib.lines as lines
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

# Wxpython
import wx
import os

# OpenCV
import cv2
import numpy as np

image = None
fig =None
type = 0
#rect = Rectangle((0,0), 0, 0, facecolor='None', edgecolor='red')
class MyDialog(wx.Panel):
    def __init__(self, parent, pathToImage=None):
        
        # Use English dialog
        self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
        
        # Initialise the parent
        wx.Panel.__init__(self, parent)

        # Intitialise the matplotlib figure
        #self.figure = plt.figure(facecolor='gray',figsize = (9,8))
        self.figure = Figure(facecolor='gray',figsize = (9,8))

        # Create an axes, turn off the labels and add them to the figure
        self.axes = plt.Axes(self.figure,[0,0,1,1])      
        self.axes.set_axis_off() 
        self.figure.add_axes(self.axes)
        

        
        # Add the figure to the wxFigureCanvas
        self.canvas = FigureCanvas(self, -1, self.figure)
        


        # Add Button and Progress Bar
        self.openBtn=wx.Button(self,-1,"Open",pos=(680,50),size=(70,40))
        self.saveBtn=wx.Button(self,-1,"save",pos=(680,150),size=(70,40))
        self.cirBtn=wx.Button(self,-1,"circle",pos=(680,200),size=(70,40))
        self.rectBtn=wx.Button(self,-1,"rectangle",pos=(790,200),size=(70,40))
        self.lineBtn=wx.Button(self,-1,"line",pos=(790,250),size=(70,40))
        self.arrowlineBtn=wx.Button(self,-1,"arrowline",pos=(680,250),size=(70,40))
        #self.gauge=wx.Gauge(self,-1,100,(00,520),(640,50))


        


        # Attach button with function
        self.Bind(wx.EVT_BUTTON,self.load,self.openBtn)
        self.Bind(wx.EVT_BUTTON,self.save,self.saveBtn)
        self.Bind(wx.EVT_BUTTON,self.line,self.lineBtn)
        self.Bind(wx.EVT_BUTTON,self.rectangle,self.rectBtn)
        self.Bind(wx.EVT_BUTTON,self.arrow,self.arrowlineBtn)
        self.Bind(wx.EVT_BUTTON,self.circle,self.cirBtn)

        # Show dialog path
        self.pathText=wx.TextCtrl(self,-1,"",pos=(680,100),size=(175,30),)

        # Check box
        self.check=wx.CheckBox(self,-1,"Check",pos=(790,50),size=(70,20))
        self.check.Bind(wx.EVT_CHECKBOX,self.onCheck)


        #self.area_text.SetInsertionPoint(0) 

        # Initialise the rectangle
        #self.rect = Rectangle((0,0), 0, 0, facecolor='None', edgecolor='red')
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        #self.axes.add_patch(self.rect)


        # The list of the picture(absolute path)
        self.fileList=[]

        # Picture name
        self.picNameList=[]

        # Picture index in list
        self.count=0 
    
        # Cut from the picture of the rectangle
        self.cut_img=None

        
        # Connect the mouse events to their relevant callbacks
        self.canvas.mpl_connect('button_press_event', self._onPress)
        self.canvas.mpl_connect('button_release_event', self._onRelease)
        self.canvas.mpl_connect('motion_notify_event', self._onMotion)
        
        
        # Lock to stop the motion event from behaving badly when the mouse isn't pressed
        self.pressed = False

        # If there is an initial image, display it on the figure
        if pathToImage is not None:
            self.setImage(pathToImage)



        
        
    # GetFilesPath with the end with .jpg or .png
    def getFilesPath(self,path):
        filesname=[]
        dirs = os.listdir(path)
        for i in dirs:
            if os.path.splitext(i)[1] == ".jpg" or os.path.splitext(i)[1] == ".png":
                filesname+=[path+"/"+i]
                self.picNameList+=[i[:-4]]
        return filesname


    # Load Picture button function
    def load(self,event):
        #dlg = wx.DirDialog(self,"Choose File",style=wx.DD_DEFAULT_STYLE)  
        dlg = wx.FileDialog(None,'select',os.getcwd(),'','All files(*.*)|*.*',wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.count=0       
            print(dlg.GetPath())
            self.setImage(dlg.GetPath())
           # self.gauge.SetValue((self.count+1)/len(self.fileList)*100)
            self.pathText.Clear()
            self.pathText.AppendText(dlg.GetPath())
            #self.fileList=self.getFilesPath(dlg.GetPath())
            #if self.fileList:
            #    self.setImage(self.fileList[0])
            #    self.gauge.SetValue((self.count+1)/len(self.fileList)*100)
            #    self.pathText.Clear()
            #    self.pathText.AppendText(dlg.GetPath())
           #else:
                #print("List Null")
        dlg.Destroy()


    # Save Picture button function
    def save(self,event):
        global fig
        self.dir_name = ''
        fd = wx.FileDialog(self, '把文件保存到何处', self.dir_name, 
                '.jpg', '*.jpg', wx.FD_SAVE)
        if fd.ShowModal() == wx.ID_OK:
            file_name = fd.GetFilename()
            dir_name = fd.GetDirectory()
            desFilename = dir_name+'\\'+file_name
            self.figure.savefig(desFilename,dpi=600)#不能使用plt.savefig保存 会出现空白 

    def circle(self,event):
        global type 
        type = 1
    # CheckBox
    def line(self,event):
        global type
        type = 2
    def arrow(self,event):
        global type
        type = 3
    def rectangle(self,event):
        global type
        type = 0
    def onCheck(self,event):
        wx.MessageBox(str(self.check.GetValue()),"Check?",wx.YES_NO|wx.ICON_QUESTION)

        
    

    def _onPress(self, event):
        ''' Callback to handle the mouse being clicked and held over the canvas'''
        # Check the mouse press was actually on the canvas
        if event.xdata is not None and event.ydata is not None:
                    
            # Upon initial press of the mouse record the origin and record the mouse as pressed
            self.pressed = True
            #rect.set_linestyle('dashed')
            self.x0 = event.xdata
            self.y0 = event.ydata
            #self.axes.add_patch(rect)


    def _onRelease(self, event):
        global type
        rect = Rectangle((0,0), 0, 0, facecolor='None', edgecolor='red')
        '''Callback to handle the mouse being released over the canvas'''
        # Check that the mouse was actually pressed on the canvas to begin with and this isn't a rouge mouse 
        # release event that started somewhere else
        if self.pressed:
            
            # Upon release draw the rectangle as a solid rectangle
            self.pressed = False
            rect.set_linestyle('solid')

            # Check the mouse was released on the canvas, and if it wasn't then just leave the width and 
            # height as the last values set by the motion event
            if event.xdata is not None and event.ydata is not None:
                self.x1 = event.xdata
                self.y1 = event.ydata
                if type == 0:#0画矩形
                        
                        
                # Set the width and height and origin of the bounding rectangle
                        self.boundingRectWidth =  self.x1 - self.x0
                        self.boundingRectHeight =  self.y1 - self.y0
                        self.bouningRectOrigin = (self.x0, self.y0)
            
                        # Draw the bounding rectangle
                        rect.set_width(self.boundingRectWidth)
                        rect.set_height(self.boundingRectHeight)
                        rect.set_xy((self.x0, self.y0))
                        self.axes.add_patch(rect)
                        self.canvas.draw()
                elif type == 1:#1画圆
                        #print (1)
                        r = ((self.x1-self.x0)**2+(self.y1-self.y0)**2)**0.5
                        #x = np.arange(self.x0+r,self.x0-r,0.01)
                        #y = self.y0+np.sqrt(r**2-(x-self.x0)**2)
                        cir = Circle((self.x0, self.y0),r, color='r', alpha=0.1,facecolor = None)
                        self.axes.add_patch(cir)
                        #self.axes.plot(x,-y)
                        #self.axes.plot(x,y)
                        self.canvas.draw()
                        #print(1)
                elif type ==2:
                        #print(self.x0)
                        #print(self.y0)
                        #print(self.x1)
                        #print(self.y1)
                        #self.axes.plot([self.x0,self.imageSize[1]-self.y0],[self.x1,self.imageSize[1]-self.y1])
                        #self.axes.add_line(Line2D((self.x0,self.y0) , (self.x0,self.y0),linewidth=2, color='r'))
                        self.axes.add_artist(lines.Line2D([self.x0,self.x1],[self.y0,self.y1],color = 'r'))
                        self.canvas.draw()
                        #print (2)
                elif type ==3:
                        arr = Arrow(self.x0,self.y0,self.x1-self.x0,self.y1-self.y0,width = 40,color = 'r')
                        self.axes.add_patch(arr)
                        self.canvas.draw()
                        #print(3)

            

    def _onMotion(self, event):
        '''Callback to handle the motion event created by the mouse moving over the canvas'''
        # If the mouse has been pressed draw an updated rectangle when the mouse is moved so 
        # the user can see what the current selection is
        
        if self.pressed:
            # Check the mouse was released on the canvas, and if it wasn't then just leave the width and 
            # height as the last values set by the motion event
            #if event.xdata is not None and event.ydata is not None:
               # self.x1 = event.xdata
                #self.y1 = event.ydata
            
            # Set the width and height and draw the rectangle
            #rect.set_width(self.x1 - self.x0)
            #rect.set_height(self.y1 - self.y0)
            #rect.set_xy((self.x0, self.y0))
            #canvas.draw_polygon([[150, 150], [250, 150], [250, 250], [150, 250]], 2, "Blue", "Aqua")
            self.canvas.draw()

        # Show Picture
    def setImage(self, pathToImage):
        '''Sets the background image of the canvas'''
        # Clear the rectangle in front picture
        self.axes.text(200,200,'',None)
        #rect.set_width(0)
        #rect.set_height(0)
        #rect.set_xy((0, 0))
        self.canvas.draw()
        #plt.cla()
        #self.initCanvas()
      
        

        
        # Load pic by OpenCV
        #image=cv2.imread(pathToImage,1)
        
        # Load the image into matplotlib and PIL
        img = cv2.imread(pathToImage)
        
        image = matplotlib.image.imread(pathToImage)
        
        imPIL = Image.open(pathToImage) 
        
        # Save the image's dimensions from PIL
        self.imageSize = imPIL.size

        '''
        self.imageSize = image.shape
        print(pathToImage)
        print("It's width and height:")
        print(self.imageSize)
        
        print("------------------------")

        # OpenCV add text on pic
        str1='(%s,%s)' % (str(self.imageSize[0]),str(self.imageSize[1]))
        rev=wx.StaticText(self,-1,str1,(670,400))
        #rev.SetForegroundColour('white')
        #rev.SetBackgroundColour('black')
        #rev.SetFont(wx.Font(15,wx.DECORATIVE,wx.ITALIC,wx.NORMAL))
        cv2.putText(image,str1,(10,200), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2)
        '''

        str1='%s,%s' % (str(self.imageSize[0]),str(self.imageSize[1]))
        rev=wx.StaticText(self,-1,str1,(680,550))
        
        # Add the image to the figure and redraw the canvas. Also ensure the aspect ratio of the image is retained.
        self.axes.imshow(image,aspect='equal')

        self.canvas.draw()

       

if __name__ == "__main__":

    # Create an demo application
    app = wx.App()
    # Create a frame and a RectangleSelectorPanel
    frame = wx.Frame(None, -1,"Show",size=(900,650))
    panel = MyDialog(frame)
    

    # Start the demo app
    frame.Show()
    app.MainLoop()
    app.OnExit()
