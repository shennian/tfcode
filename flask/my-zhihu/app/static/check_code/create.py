from PIL import Image, ImageDraw, ImageFont

fontsize = 12
image = Image.new("RGBA", (100, 50), (255, 255, 255))

draw = ImageDraw.Draw(image)

# use a bitmap font
font = ImageFont.truetype('simsun.ttc', 30)


draw.text((5, 10), "123456", font=font, fill='#ff0000')

image.save('image.png')