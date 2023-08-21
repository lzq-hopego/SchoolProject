from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox
import os
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
'''
使用该脚本需要安装图像处理库opencv(opencv-python)和PIL(Pillow)
创建时间:‎2022‎年‎11‎月‎21‎日，‏‎13:59:34——李展旗
使用：选择一个路径用来存放学生的作业截图，同时通过这个路径目录里的文件判断是否未交作业
选择文件，是为了方便每一个学生发来的截图需要改名的复杂和姓名学号(后续可搭配opencv实现)的复杂操作
提交,自动命名图片的名称，操作不可逆
下拉列表框用来选择学生
保存记录，生成一个.csv用来可视化统计交作业的信息

'''



name_list=[]
id_list=[]
opencv=False

txt='''
学号	姓名
123456789 李四
123456789 张三

'''.split("\n")#在上面的内容输入学号和名字，用空格隔开


for i in txt[2:-2]:
    name_id=i.split("\t")[0]
    name=i.split("\t")[-1].split(",")[0]
    name_list.append(name)
    id_list.append(name_id)

def selectPath():
    selected_file_path = filedialog.askopenfilename()  # 使用askopenfilename函数选择单个文件
    path_in.set(selected_file_path)  
def selectPath_out():
    path_ = filedialog.askdirectory()
    path.set(path_)
def baocun():
    file_name=entry.get()
    file_path_in=entry_path.get()
    if entry.get()=='' or entry_path.get()=="":
        tkinter.messagebox._show('警告信息','输入文件名')
        return

    index=comboExample.current()
    kuozhan='.'+file_name.split('.')[-1]
    name=file_path_in+"\\"+name_list[index]+"_"+id_list[index]+kuozhan


    if opencv==True:
        image =cv2.imdecode(np.fromfile(file_name,dtype=np.uint8),-1)
        name_id=name_list[index]+id_list[index][-2:]
        image=print_text(image,(image.shape[1]/2-(len(name_id)*28),image.shape[0]/2-60),name_id)

        cv2.imencode('.jpg', image)[1].tofile(name)

        text.insert(END, "已提交>>>\t" +name_list[index]+"_"+id_list[index]+kuozhan)
        text.see(END)
        text.update()
        return
    with open(file_name,'rb') as f:
        data=f.read()
    with open(name,"wb") as f:
        f.write(data)
    text.insert(END, "已提交>>>\t" +name_list[index]+"_"+id_list[index]+kuozhan)
    text.see(END)
    text.update()
    data=''

def print_text(img,position,word):
    img_c = Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_c)
    font = ImageFont.truetype(r"C:\Windows\Fonts\SIMYOU.ttf", 120)  #设置字体 （参数字体，文字大小）
    draw.text(position,word,(255,0,0),font=font)  #添加文字  参数（字的位置，字的内容，颜色，字体）
    img = cv2.cvtColor(np.array(img_c), cv2.COLOR_RGB2BGR)
    return img

def cleartxt():
    text.delete(0,END)
def dirlist():
    list=os.listdir(entry_path.get())
    name=[]
    id=[]
    for i in list:
        if ".py" in i:
            continue
        elif '.csv' in i:
            continue
        name.append(i.split("_")[0])
        id.append(i.split("_")[-1].split(".")[0])
    return name,id

def success():
    name,id=dirlist()
    cleartxt()
    for i in range(len(name)):
        text.insert(END, "已提交>>>" +name[i]+",\t学号>>>"+ id[i])
    text.see(END)
    text.update()
    return
def un_success():
    name,id=dirlist()
    cleartxt()
    
    for i in range(len(name_list)):
        if name_list[i] in name:
            continue
        else:
            text.insert(END, "未提交>>>" +name_list[i]+",\t学号>>>"+ id_list[i])
            text.see(END)
            text.update()
    return
def log():
    name,id=dirlist()
    file_path_in=entry_path.get()
    success_num=0
    un_success_num=0
    txt=''
    fo=open("作业提交信息统计.csv",'w')
    for i in range(len(name_list)):
        if name_list[i] in name:
            txt+=(name_list[i]+","+id_list[i]+","+"已提交,,,"+name_list[i]+"\n")
            success_num+=1
        else:
            txt+=(name_list[i]+","+id_list[i]+","+"未提交,,,,"+name_list[i]+"\n")
            un_success_num+=1
    fo.write('姓名,学号,作业状态,,,已提交:'+str(success_num)+",未提交:"+str(un_success_num)+",退学:1"+"\n")
    fo.write(txt)
    fo.write("刘亚迪,222603003934,已退学,,,,,刘亚迪\n")
    fo.close()
def set_opencv():
    global opencv
    if opencv==False:
        opencv=True
    else:
        opencv=False

    
    

root = Tk()
##禁止拉伸窗体
# root.resizable(False,False)
##调整窗口的透明度
root.attributes('-alpha', 0.9)
path = StringVar()
path_in = StringVar()

path.set(os.getcwd())

##初始化窗口至屏幕中央
sw=root.winfo_screenwidth()
sh=root.winfo_screenheight()
root.geometry('770x460+{}+{}'.format(int((sw-770)/2),int((sh-460)/2)))

root.title("作业统计")




##下拉列表控件
comboExample = ttk.Combobox(root, 
                            values=name_list,font=("Consolas", 15),state="readonly")
comboExample.grid(row=0, column=0)
comboExample.current(0)

 

Button(root, text="选择文件", relief = 'ridge',font=("Consolas", 15), command=selectPath).grid(row=0, column=2)
 
entry = Entry(root,textvariable = path_in, font=('Consolas', 15))
entry.grid(row=0, column=1)

 
Label(root, text="文件存放路径", font=('Consolas', 15)).grid(row=2, column=0)
#存放路径的输入栏
entry_path = Entry(root, textvariable = path,font=('Consolas', 15))
entry_path.grid(row=2, column=1)
 
Button(root, text="选择路径", relief = 'ridge',font=("Consolas", 15),command=selectPath_out).grid(row=2, column=2)#,sticky=E)
 
text = Listbox(root,selectmode = BROWSE,font=("Consolas", 15), width=45, height=10)
text.grid(row=3, columnspan=2)



Button(root, text="清空列表", relief = 'ridge',font=("Consolas", 15),command=cleartxt).grid(row=3, column=2,sticky=S)

##radioBtnA = Radiobutton(root, text="Python", variable=IntVar(), value=1).grid(row=4, column=1,sticky=W)
checkBtnA = Checkbutton(root, text="P学号",font=("Consolas", 13),command=set_opencv).grid(row=4, column=0)

#下载和退出按钮

Button(root, text="已提交",font=("Consolas", 15),command=success).grid(row=4, column=1)
Button(root, text="未提交",font=("Consolas", 15),command=un_success).grid(row=4, column=1,sticky=W)

btn_down=Button(root, text="提交",relief = 'ridge',font=("Consolas", 15),command=baocun).grid(row=4, column=0, sticky=W)

Button(root, text="退出", relief = 'ridge',font=("Consolas", 15),command=root.destroy).grid(row=4, column=1, sticky=E)
Button(root, text="保存记录", relief = 'ridge',font=("Consolas", 15),command=log).grid(row=4, column=2, sticky=E)
root.mainloop()


