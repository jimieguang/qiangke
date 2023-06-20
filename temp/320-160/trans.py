from PIL import Image

for num in range(1,6):
    image = Image.open("new%d.jpg" % num)
    image1=Image.new("RGB",(320,160),(255,255,255))
    image2 = Image.new("RGB",(320,160),(255,255,255))
    image3 = Image.new("RGB",(320,160),(255,255,255))
    for i in range(0,320):
        for j in range(0,160):
            r,g,b = image.getpixel((i,j))
            image1.putpixel((i,j),(r,r,r))
            image2.putpixel((i,j),(g,g,g))
            image3.putpixel((i,j),(b,b,b))

    image1.save("%d-1.jpg" %(num))
    image2.save("%d-2.jpg" %(num))
    image3.save("%d-3.jpg" %(num))

