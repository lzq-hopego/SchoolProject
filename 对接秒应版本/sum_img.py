'''
作者: 李展旗
Date: 2023-05-18 21:54:41
文件最后编辑者: 李展旗
LastEditTime: 2023-05-21 12:06:15
'''
from PIL import Image
import sys


def sum_img(img1,img2,out_img):
    im = Image.open(img1)
    img=Image.open(img2)


    x, y = im.size
    x1,y1=img.size

    height=y==y1
    width=x==x1
    print(im.size,img.size)

    if width:
        print("height")
        image = Image.new('RGB', (x, y+y1), (255,0,0))
        image.paste(im,(0,0))
        image.paste(img,(0,y))
        image.save(out_img)
        return
    if height:
        print("width")
        image = Image.new('RGB', (x+x1, y), (255,0,0))
        image.paste(im,(0,0))
        image.paste(img,(x,0))
        image.save(out_img)
        return
    print('不同宽高，正在计算..')
    y=y + y1
    x=x if x>x1 else x1
    image = Image.new('RGB', (x, y), (0,0,0))
    image.paste(im,(0,0))
    image.paste(img,(0,im.size[1]))
    image.save(out_img)

if __name__=='__main__':
    ls=sys.argv[1:]
    sum_img(ls[0],ls[1],ls[2])

