from PIL import Image, ImageDraw, ImageFont
import piexif
import os


def add_border_and_watermark(image_path, output_path, brand_logo_path):
    # 打开图片
    image = Image.open(image_path)

    # 获取图片元数据
    exif_data = piexif.load(image.info['exif'])
    make = exif_data['0th'][piexif.ImageIFD.Make].decode('utf-8') if piexif.ImageIFD.Make in exif_data[
        '0th'] else 'Unknown'
    model = exif_data['0th'][piexif.ImageIFD.Model].decode('utf-8') if piexif.ImageIFD.Model in exif_data[
        '0th'] else 'Unknown'

    # 添加边框
    border_width = 50
    new_width = image.width + 2 * border_width
    new_height = image.height + 2 * border_width
    bordered_image = Image.new('RGB', (new_width, new_height), (255, 255, 255))
    bordered_image.paste(image, (border_width, border_width))

    # 添加水印
    watermark_text = f"Camera: {make} {model}"
    font = ImageFont.truetype("arial.ttf", 30)
    draw = ImageDraw.Draw(bordered_image)
    text_width, text_height = draw.textsize(watermark_text, font=font)
    text_position = (bordered_image.width - text_width - border_width,
                     bordered_image.height - text_height - border_width)
    draw.text(text_position, watermark_text, font=font, fill=(0, 0, 0))

    # 添加品牌 logo
    if brand_logo_path:
        logo = Image.open(brand_logo_path)
        logo = logo.resize((100, 100))
        logo_position = (border_width, bordered_image.height - logo.height - border_width)
        bordered_image.paste(logo, logo_position, logo)

    # 保存图片
    bordered_image.save(output_path)


# 示例用法
if __name__ == '__main__':
    image_path = '../imgs/input/YKW_1066.jpg'  # 输入图片路径
    output_path = '../imgs/output'  # 输出图片路径
    brand_logo_path = '../core/logo/nikon_1.png'  # 品牌 logo 路径
    add_border_and_watermark(image_path, output_path, brand_logo_path)


