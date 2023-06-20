from PIL import Image

for i in range(6):
    image_l = Image.open(f"{i+1}l.jpg")
    image_r = Image.open(f"{i+1}r.jpg")
    new_image = Image.new("RGB",(480,240))
    for j in range(0,480):
        if j <= 240:
            image = image_r
        else:
            image = image_l
        for k in range(0,240):
            pixel = image.getpixel((j,k))
            new_image.putpixel((j,k),pixel)
    new_image.save(f"new_{i+1}.jpg")
