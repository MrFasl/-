# -*- coding: utf-8 -*-
"""
Created on Thu May 21 10:13:05 2020
键盘输入 ‘1’：直线  ‘2’：矩形 ‘3’：圆形 ‘4’：箭头 ‘Esc’：退出
部分函数解释：
直线函数cv2.line (
    img:输入图像，直线画在该图像上
    pt1:直线的起点
    pt2:直线的终点
    color:直线的颜色
    thickness:直线的大小
    lineType：直线类型
    shift:直线的偏移量)
箭头函数cv2.arrwedLine(
    img:输入图像，直线画在该图像上
    pt1:直线的起点
    pt2:直线的终点
    color:直线的颜色
    thickness:直线的大小
    lineType：直线类型
    shift:直线的偏移量
    tipLength:箭头占线段的比例)
矩形函数cv2.retangle(
    img:输入图像，矩形画在该图像上
    rec:矩形
    color:矩形的颜色
    thickness:矩形边的大小
    lineType：矩形类型
    shift:直线的偏移量)
圆形函数cv2.circle()
    img:输入图像，圆形画在该图像上
    center:圆心
    radius:半径
    color:圆形的颜色
    thickness:圆形边的厚度
    lineType：圆形类型
    shift:圆形的偏移量)
@author: zihao
"""
import wx
import os
import cv2
drawing=False
itype = 0
curfilename = ''
k = 0
img = None
class SiteLog(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,title='选择图片',size=(520,80))
        self.SelBtn = wx.Button(self,label='open',pos=(305,5),size=(80,25))
        self.SelBtn.Bind(wx.EVT_BUTTON,self.OnOpenFile)
        self.OkBtn = wx.Button(self,label='save as',pos=(405,5),size=(80,25))
        self.OkBtn.Bind(wx.EVT_BUTTON,self.ReadFile)
        self.FileName = wx.TextCtrl(self,pos=(5,5),size=(230,25))
        #self.FileContent = wx.TextCtrl(self,pos=(5,35),size=(620,480),style=(wx.TE_MULTILINE))
        
    def OnOpenFile(self,event):
        global curfilename
        global itype
        global img,k
        wildcard = 'All files(*.*)|*.*'
        dialog = wx.FileDialog(None,'select',os.getcwd(),'',wildcard,wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.FileName.SetValue(dialog.GetPath())
            curfilename = dialog.GetPath()
            img=cv2.imread(curfilename,cv2.IMREAD_COLOR)#读取图片
            cv2.namedWindow('image')
            cv2.setMouseCallback('image',draw_picture)
            dlg = wx.MessageDialog(None, u"键盘输入1为直线，输入2为矩形，输入3为圆形，输入4为箭头，按下“Esc”为退出", u"操作指南",  wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                self.Close(True)
                dlg.Destroy()
            while(1):#键盘输入
                cv2.imshow('image',img)
                k=cv2.waitKey(20)&0xFF#获取键盘输入
                if k==ord('1'):
                    itype = 1 #直线
                elif k== ord('2'):
                    itype = 2 #矩形
                elif k == ord('3'):
                    itype = 3 #圆形
                elif k == ord('4'):
                    itype = 4 #箭头
                elif k==27:  #"Esc"退出
                    break
            #cv2.imwrite('fsf.png',img)
            cv2.destroyAllWindows()
            dialog.Destroy
            
    def ReadFile(self,event):
        global img,k
        self.dir_name = ''
        fd = wx.FileDialog(self, '把文件保存到何处', self.dir_name, 
                '.jpg', '*.jpg', wx.FD_SAVE)
        if fd.ShowModal() == wx.ID_OK:
            self.file_name = fd.GetFilename()
            self.dir_name = fd.GetDirectory()
            desFilename = fd.GetDirectory()+'\\'+fd.GetFilename()
            print(desFilename)
            cv2.imwrite(desFilename,img)
            k = ord('27')
            cv2.destroyAllWindows()
def draw_picture(event,x,y,flags,param):
        global x1,y1 #初始坐标
        if event==cv2.EVENT_LBUTTONDOWN:
            #drawing = True
            x1,y1 = x,y #初始点赋值
        elif event == event==cv2.EVENT_LBUTTONUP:
            #drawing = False
            if itype == 1:
                    #cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),3)
                    cv2.line(img, (x1,y1), (x,y), (0,0,255),1,4)
            elif itype == 2:
                    cv2.rectangle(img,(x1,y1),(x,y),(0,0,255),3)  
            elif itype == 3:
                    cv2.circle(img,(x,y),100,(0,0,255),5)
            elif itype == 4:
                    cv2.arrowedLine(img, (x1,y1), (x,y), (0,0,255),5,8,0,0.1)



if __name__=='__main__':

    app = wx.App()
    SiteFrame = SiteLog()
    SiteFrame.Show()
    app.MainLoop()
    
    
