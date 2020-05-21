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

import cv2
drawing=False
type = 0#图案类型  
def draw_picture(event,x,y,flags,param):
    global x1,y1 #初始坐标
    if event==cv2.EVENT_LBUTTONDOWN:
        drawing = True
        x1,y1 = x,y #初始点赋值
    elif event==cv2.EVENT_MOUSEMOVE and flags==cv2.EVENT_FLAG_LBUTTON:
        if drawing==True:
            if type == 1:
                #cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),3)
                cv2.line(img, (x1,y1), (x,y), (0,0,255),1,4)
            elif type == 2:
                cv2.rectangle(img,(x1,y1),(x,y),(0,0,255),3)  
            elif type == 3:
                cv2.circle(img,(x,y),100,(0,0,255),1)
    elif event == event==cv2.EVENT_LBUTTONUP:
        drawing = False
        if type == 1:
                #cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),3)
                cv2.line(img, (x1,y1), (x,y), (0,0,255),1,4)
        elif type == 2:
                cv2.rectangle(img,(x1,y1),(x,y),(0,0,255),3)  
        elif type == 3:
                cv2.circle(img,(x,y),100,(0,0,255),5)
        elif type == 4:
                cv2.arrowedLine(img, (x1,y1), (x,y), (0,0,255),5,8,0,0.1)
    
    
    
img=cv2.imread('test.jpg',cv2.IMREAD_COLOR)#读取图片
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_picture)#调取鼠标响应函数
while(1):#键盘输入
    cv2.imshow('image',img)
    k=cv2.waitKey(20)&0xFF#获取键盘输入
    if k==ord('1'):
        type = 1 #直线
    elif k== ord('2'):
        type = 2 #矩形
    elif k == ord('3'):
        type = 3 #圆形
    elif k == ord('4'):
        type = 4 #箭头
    elif k==27:  #"Esc"退出
        break
cv2.imwrite('fsf.png',img)
cv2.destroyAllWindows()
