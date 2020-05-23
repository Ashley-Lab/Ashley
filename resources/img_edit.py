from PIL import Image, ImageDraw, ImageFont


def gift(key, time):

    # load image
    image = Image.open("images/dashboards/giftart.png").convert('RGBA')
    show = ImageDraw.Draw(image)

    # load fonts
    font_key = ImageFont.truetype("fonts/gift.otf", 18)
    font_time = ImageFont.truetype("fonts/bot.otf", 24)

    # retangulos dos textos
    rectangle_1 = [5, 46, 394, 83]
    rectangle_2 = [88, 191, 312, 156]
    x1, y1, x2, y2 = rectangle_1
    x3, y3, x4, y4 = rectangle_2

    # bordas dos retangulos
    show.rectangle([x1, y1, x2, y2])
    show.rectangle([x3, y3, x4, y4])

    # alinhamento do retangulo 1
    w, h = show.textsize(key, font=font_key)
    x = (x2 - x1 - w) / 2 + x1 + 3
    y = (y2 - y1 - h) / 2 + y1 + 3
    show.text(xy=(x + 2, y + 2), text=key, fill=(0, 0, 0), font=font_key)
    show.text(xy=(x, y), text=key, fill=(255, 255, 255), font=font_key)

    # alinhamento do retangulo 2
    w, h = show.textsize(time, font=font_time)
    x = (x4 - x3 - w) / 2 + x3
    y = (y4 - y3 - h) / 2 + y3 + 1
    show.text(xy=(x + 2, y + 2), text=time, fill=(0, 0, 0), font=font_time)
    show.text(xy=(x, y), text=time, fill=(255, 255, 255), font=font_time)

    image.save('giftcard.png')
