'''
作者: 李先生
Date: 2023-05-19 13:24:08
文件最后编辑者: 李先生
LastEditTime: 2023-05-22 12:18:27
'''
import sys
#PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.QtWidgets import QApplication, QMainWindow
#导入designer工具生成的login模块
from PyQt5.QtWidgets import QApplication,QPushButton,QFileDialog,QFileDialog
import os
from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from sum_img import sum_img as sumimg
import numpy as np
from PIL import Image, ImageDraw, ImageFont
# import numpy as np
import cv2
import time
import xlwt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from get_music.download import download

from Ui_down_img import Ui_Form as down_img
from Ui_main import Ui_MainWindow as mainwindow
from Ui_sum_img_ui import Ui_Form as sum_img
from Ui_put import Ui_Form as putui


class Main(QMainWindow, mainwindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        self.setContextMenuPolicy(3)
        self.customContextMenuRequested[QPoint].connect(self.right)
    def right(self):
        global is_or_ps
        menu=QMenu()
        menu.setStyleSheet("font: 12pt \"幼圆\";\n"
    "color: rgb(255, 128, 128);")
        menu.addAction(QAction(u'设置保存文件夹', self, triggered=self.path))  #下载当前选中的条目 
        if is_or_ps:
            menu.addAction(QAction(u'是否P学号:是', self,triggered=self.change_ps))
        else:
            menu.addAction(QAction(u'是否P学号:否', self,triggered=self.change_ps))
        menu.exec_(QCursor.pos())
    
    def change_ps(self):
        global is_or_ps
        daan = QMessageBox.question(self, '水印', '你需要自动添加水印？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if daan==QMessageBox.Yes:
            is_or_ps=True
        else:
            is_or_ps=False

    def path(self):
        global worker_path
        dirname=wenjianjia()
        if dirname=="未打开文件夹":
            worker_path=""
        else:
            worker_path=dirname
         

    def mousePressEvent(self, evt):
        if evt.button() == Qt.LeftButton:
            self.switch = True
        else:
            self.switch = False
        self.mouse_x = evt.globalX()
        self.mouse_y = evt.globalY()
        self.window_x = self.x()
        self.window_y = self.y()
    def mouseMoveEvent(self, evt):
        if self.switch:
            move_x = evt.globalX() - self.mouse_x
            move_y = evt.globalY() - self.mouse_y

            vector_x = self.window_x + move_x
            vector_y = self.window_y + move_y
            self.move(vector_x, vector_y)

class down_img(QMainWindow, down_img):
    def __init__(self, parent=None):
        super(down_img, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.downimg)
        self.pushButton_2.clicked.connect(self.sou_page)
        self.graphicsScene = QGraphicsScene()
        self.name_ls=[]
        self.sid_ls=[]
        self.imgurl_ls=[]
        
    def downimg(self):
        options=Options()
        options.add_argument("headless")
        #在此填写谷歌驱动或各个浏览器的驱动
        self.guge=webdriver.Chrome(r"D:\chrome\chromedriver.exe",options=options)
        global worker_path
        if worker_path=='':
            path=wenjianjia()
            worker_path=path
        url=self.lineEdit.text()
        if url == '' or 'http' not in url:
            print('链接为空,或链接不合法')
            return
        self.textBrowser.insertPlainText(url+"\n")
        # url='http://miaoying.hui51.cn/tongji/result/64533be1e5465e000b467d24'
        self.guge.get(url)
        filename='login_test.png'
        time.sleep(3)
        
        img=self.guge.find_element_by_xpath("/html/body/div/div/div/div[2]/img")
        self.textBrowser.insertPlainText(filename+"\n")
        img.screenshot(filename)
        # time.sleep(3)
        self.file_name1=filename
        self.pixmap = QPixmap(filename)
        self.pixmap=self.pixmap.scaled(256,192,Qt.KeepAspectRatio)
        self.pixmapItem = QGraphicsPixmapItem(self.pixmap)
        self.graphicsScene.addItem(self.pixmapItem)
        self.graphicsView.setScene(self.graphicsScene)
        # time.sleep(20)
        # try:
        #     guge.find_element_by_xpath("/html/body/div/section/section/section/main/div[1]/div/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div/div[1]")
        # except:
        #     self.textBrowser.insertPlainText("登录成功!\n正在收集信息中...!\n")
        # self.sou()
        # guge.quit()
        # self.textBrowser.insertPlainText("一共收集到了:"+str(len(self.name_ls))+"份作业\n")
    def sou_page(self):
        self.sou()
        self.guge.quit()
        self.textBrowser.insertPlainText("完成!\n")
        self.textBrowser.insertPlainText("一共收集到了:"+str(len(self.name_ls))+"份作业\n")
        self.download_img()

    def sou(self):
        for i in range(1,29):
            try:
                self.name_ls.append(self.guge.find_element_by_xpath("/html/body/div/section/section/section/main/div[1]/div/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[{}]/div[1]/div[1]/div/div[1]".format(i)).text)
                self.sid_ls.append(self.guge.find_element_by_xpath("/html/body/div/section/section/section/main/div[1]/div/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[{}]/div[2]/div/div/div[1]/div/div/div/div[2]/block".format(i)).text)
                self.imgurl_ls.append(self.guge.find_element_by_xpath("/html/body/div/section/section/section/main/div[1]/div/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[{}]/div[2]/div/div/div[2]/div/div/div/div[2]/div/block/div/div/div/img".format(i)).get_attribute("src"))
            except:
                self.textBrowser.insertPlainText("无法匹配信息!\n")
                break
            self.textBrowser.insertPlainText("进度:{}\n".format(i))
        try:
            pagedown=self.guge.find_element_by_class_name('ant-pagination-next')  
            if pagedown.get_attribute("aria-disabled")=='false':
                pagedown.click()
                time.sleep(1)
                return self.sou()
        except:
            return
        
    def download_img(self):
        global worker_path
        self.textBrowser.insertPlainText("正在下载图片...\n")
        self.img_name=[]
        self.img_name_id=[]
        for i in self.imgurl_ls:
            num=self.imgurl_ls.index(i)
            self.img_name_id.append(self.name_ls[num]+self.sid_ls[num])
            filename=worker_path+"\\"+self.name_ls[num]+"_"+self.sid_ls[num]+".jpg"
            self.img_name.append(filename)
            print(i)
            download(i,filename,or_re=False)
            self.textBrowser.insertPlainText("下载进度:{}/{}\n".format(num+1,len(self.imgurl_ls)))
        self.img_ps()
    def img_ps(self):
            for i in self.img_name:
                index=self.img_name.index(i)
                alter_img(i,self.img_name_id[index])
                self.textBrowser.insertPlainText("正在处理水印:{} / {}\n".format(self.img_name.index(i)+1,len(self.img_name)))



class sum_img(QMainWindow, sum_img):
    def __init__(self, parent=None):
        super(sum_img, self).__init__(parent)
        self.setupUi(self)

        self.graphicsScene = QGraphicsScene()
        self.graphicsScene_2 = QGraphicsScene()
        self.graphicsScene_3 = QGraphicsScene()
        
        self.pushButton_3.clicked.connect(self.img_1)
        self.pushButton_4.clicked.connect(self.img_2)
        self.pushButton_2.clicked.connect(self.img_3)

        self.file_name1=''
        self.file_name2=''
        global worker_path
        if worker_path=='':
            path=wenjianjia()
            worker_path=path

    def img_1(self):
        filename=self.wenjian()
        if filename=="未打开文件":
            return
        self.file_name1=filename
        self.pixmap = QPixmap(filename)
        self.pixmap=self.pixmap.scaled(256,192,Qt.KeepAspectRatio)
        self.pixmapItem = QGraphicsPixmapItem(self.pixmap)
        self.graphicsScene.addItem(self.pixmapItem)
        self.graphicsView.setScene(self.graphicsScene)
        
    def img_2(self):
        filename=self.wenjian()
        if filename=="未打开文件":
            return
        self.file_name2=filename
        self.pixmap_2 = QPixmap(filename)
        self.pixmap_2=self.pixmap_2.scaled(256,192,Qt.KeepAspectRatio)
        self.pixmapItem = QGraphicsPixmapItem(self.pixmap_2)
        self.graphicsScene_2.addItem(self.pixmapItem)
        self.graphicsView_2.setScene(self.graphicsScene_2)
    def img_3(self):
        global name_list
        global id_list
        global worker_path
        index=name_list.index(self.comboBox.currentText())
        if self.file_name2 !='' and self.file_name1 !='':
            name=worker_path+"//"+name_list[index]+"_"+id_list[index]+".jpg"
            try:
                sumimg(self.file_name1,self.file_name2,name)
            except:
                print("转换失败")
            try:
                # print(name,worker_path)
                alter_img(name,name_list[index]+id_list[index])
            except:
                print("处理水印失败")
            self.pixmap_3 = QPixmap(name)
            self.pixmap_3=self.pixmap_3.scaled(256,192,Qt.KeepAspectRatio)
            self.pixmapItem = QGraphicsPixmapItem(self.pixmap_3)
            self.graphicsScene_3.addItem(self.pixmapItem)
            self.graphicsView_3.setScene(self.graphicsScene_3)
        else:
            print("缺少图片")
        

    def wenjian(self):
        file,_ = QFileDialog().getOpenFileName(self,"选择一张图片","C:\\Users\\李展旗\\Desktop\\",'Image files (*.jpg *png)')
        if file:
            filename = file
            return filename
        else:
            return "未打开文件"

class putui(QMainWindow, putui):
    def __init__(self, parent=None):
        super(putui, self).__init__(parent)
        self.setupUi(self)
        self.graphicsScene = QGraphicsScene()
        self.graphicsScene_2 = QGraphicsScene()
        self.pushButton.clicked.connect(self.tijiao)
        self.pushButton_2.clicked.connect(self.img_1)

        self.setContextMenuPolicy(3)
        self.customContextMenuRequested[QPoint].connect(self.right)
    def right(self):
        menu=QMenu()
        menu.setStyleSheet("font: 12pt \"幼圆\";\n"
    "color: rgb(255, 128, 128);")
        menu.addAction(QAction(u'保存记录', self, triggered=self.message))  #下载当前选中的条目 
        menu.exec_(QCursor.pos())
    
    def message(self):
        global worker_path
        global name_list
        global id_list
        list=os.listdir(worker_path)
        unput_name=[]
        self.name_list=[]
        for i in list:
            if ('.jpg' in i) or ('.png' in i):
                self.name_list.append(i[0:i.index('_')])
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('作业统计表')
        style = xlwt.easyxf('pattern:pattern solid, fore_colour red;')
        sheet.write(0,0,"姓名")
        sheet.write(0,1,"学号")
        put_sum=0
        for i in range(len(name_list)):
            sheet.write(i+1,0,name_list[i])
            sheet.write(i+1,1,id_list[i])
            if name_list[i] in self.name_list:
                sheet.write(i+1,3,name_list[i])
                put_sum+=1
                self.listWidget.addItem(name_list[i]+"\t"+"已提交")
            else:
                sheet.write(i+1,4,name_list[i],style)
                unput_name.append(name_list[i]+"\t"+"未提交")
        self.listWidget.addItems(unput_name)
        sheet.write(0,3,"已提交: {}".format(put_sum))
        sheet.write(0,4,"未提交: {}".format(len(name_list)-put_sum))
        workbook.save(worker_path+'//作业统计表.xls')

    
    def wenjian(self):
        file,_ = QFileDialog().getOpenFileName(self,"选择一张图片","C:\\Users\\李展旗\\Desktop\\",'Image files (*.jpg *png)')
        if file:
            filename = file
            return filename
        else:
            return "未打开文件"
        
    def img_1(self):
        filename=self.wenjian()
        if filename=="未打开文件":
            return
        self.file_name1=filename
        self.pixmap = QPixmap(filename)
        self.pixmap=self.pixmap.scaled(256,192,Qt.KeepAspectRatio)
        self.pixmapItem = QGraphicsPixmapItem(self.pixmap)
        self.graphicsScene.addItem(self.pixmapItem)
        self.graphicsView.setScene(self.graphicsScene)
        
    def tijiao(self):
        global worker_path
        global name_list
        global id_list
        index=name_list.index(self.comboBox.currentText())
        path=worker_path+"//"+name_list[index]+"_"+id_list[index]+".jpg"
        alter_img(self.file_name1,name_list[index]+id_list[index],path_to=path)
        self.listWidget.addItem(name_list[index]+"\t"+"已提交")
        
    #     filename=self.wenjian()
    #     if filename=="未打开文件":
    #         return
    #     self.file_name2=filename
        self.pixmap_2 = QPixmap(path)
        self.pixmap_2=self.pixmap_2.scaled(256,192,Qt.KeepAspectRatio)
        self.pixmapItem = QGraphicsPixmapItem(self.pixmap_2)
        self.graphicsScene_2.addItem(self.pixmapItem)
        self.graphicsView_2.setScene(self.graphicsScene_2)


def print_text(img,position,word):
    img_c = Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_c)
    font = ImageFont.truetype(r"C:\Windows\Fonts\SIMYOU.ttf", 120)  #设置字体 （参数字体，文字大小）
    draw.text(position,word,(255,0,0),font=font)  #添加文字  参数（字的位置，字的内容，颜色，字体）
    img = cv2.cvtColor(np.array(img_c), cv2.COLOR_RGB2BGR)
    return img

def alter_img(img_name,name_and_id,path_to=''):
    global is_or_ps
    image =cv2.imdecode(np.fromfile(img_name,dtype=np.uint8),-1)
    if is_or_ps:
        image=print_text(image,(image.shape[1]/2-(len(name_and_id)*28),image.shape[0]/2-60),name_and_id)
    img_type="."+img_name.split('.')[-1]
    if path_to !='':
        img_name=path_to
    cv2.imencode(img_type, image)[1].tofile(img_name)

def wenjianjia():
    file = QFileDialog.getExistingDirectory()
    if file:
        return file
    else:
        return "未打开文件夹"

worker_path=""
is_or_ps=True
name_list=[]
id_list=[]
txt='''
学号	姓名
123456789 李四
123456789 张三

'''.split("\n")  #在此填写姓名和学号，用空格隔开


for i in txt[2:-2]:
    name_id=i.split("\t")[0]
    name=i.split("\t")[-1].split(",")[0]
    name_list.append(name)
    id_list.append(name_id)





if __name__ =="__main__":
    app = QApplication(sys.argv)
    main=Main()
    Down_img=down_img()
    Sum_img=sum_img()
    Put_ui=putui()
    main.show()

    if worker_path=='':
        path=wenjianjia()
        worker_path=path

    main.pushButton_2.clicked.connect(Sum_img.show)
    main.pushButton_3.clicked.connect(Down_img.show)
    main.pushButton_4.clicked.connect(Put_ui.show)
##    main.pushButton.clicked.connect(app.quit)
    
    Sum_img.comboBox.addItems(name_list)
    Put_ui.comboBox.addItems(name_list)
    sys.exit(app.exec_())
