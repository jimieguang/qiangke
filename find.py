#jpg格式是有损压缩，代码中引入的判定像素可能会变化导致一系列不确定后果，因此使用png格式保存匹配图片
from PIL import Image
import time
def find_pic(order):
    '''匹配缺口'''
    image2 = Image.open("./temp/target.jpg")
    w,h = image2.size
    if w==480:
        image1 = Image.open("./temp/480-240/new%d.jpg"%order)
    else:
        image1 = Image.open("./temp/320-160/new%d.jpg"%order)

    #转成灰度图提高匹配速度（像素值以array形式储存）
    array1 = image1.convert("L").load()
    array2 = image2.convert("L").load()

    image3 = Image.new("L",(w,h),255)
    #定义检测的最大像素值
    Maxnum = 6000*(w/320)
    num = 0
    for i in range(0,w):
        for j in range(0,h):
            mean1 = array1[i,j]
            mean2 = array2[i,j]
            if mean1 !=0:
                #检测该像素是否被透明块覆盖
                scale = mean2/mean1
                if scale < 0.9:
                    num += 1
                    image3.putpixel((i,j),0)
                if  scale>1.1:
                    num += 1
                    image3.putpixel((i,j),126)
            #及时终止不合理判定，提高效率
            if(num>=Maxnum):
                return 0
    if num < Maxnum:
        image3.save("./temp/result-%d.png"%order)
        return order
    else:
        return 0

def find_distance(fileorder):
    '''找到缺口离起点的距离（像素）'''
    if fileorder == 0:
        return 0
    image = Image.open("./temp/result-%d.png"%fileorder)
    w,h = image.size
    array = image.load()
    judgelist = [0,126]
    for i in range(0,w):
        num = 0
        for j in range(0,h):
            mean = array[i,j]
            if mean in judgelist:
                num += 1
        if num > 20*(w/320):
            return int(i*320/w)
    return 0

if __name__ == "__main__":
    start = time.time()
    for i in range(1,6):
        fileorder = find_pic(i)
        if fileorder != 0:
            break
    distance = find_distance(fileorder)
    print("distance=%d"%distance)
    end = time.time()
    print("time: %f"%(end-start))
