from PIL import Image

# 载入图像
img_path = 'image.jpg'
img = Image.open(img_path)

# 将图像转换为RGBA，以便我们可以处理透明度
img = img.convert('RGBA')

# 准备一个新图像以存放污点，使用相同的大小和RGBA模式
spots_img = Image.new('RGBA', img.size)

# 定义污点的RGB阈值，这里我们假设污点为黑色或接近黑色
# RGB的值都比较低，这里我们设定一个阈值，低于这个值的认为是污点
threshold = 134

# 遍历原图中的每个像素
for y in range(img.height):
    for x in range(img.width):
        current_pixel = img.getpixel((x, y))
        # 检查像素的RGB值是否低于阈值
        if current_pixel[0] < threshold and current_pixel[1] < threshold and current_pixel[2] < threshold:
            # 将污点像素设置为黑色，其余为透明
            spots_img.putpixel((x, y), (0, 0, 0, 255))
        else:
            # 其余像素设置为完全透明
            spots_img.putpixel((x, y), (0, 0, 0, 0))

# 保存新的污点图层
spots_img_path = 'spots_layer.png'
spots_img.save(spots_img_path)

# 使用相同的阈值清除污点
clean_img = img.copy()

# 初始化一个数组用于存放污点位置
dirty_pixels = []

for y in range(clean_img.height):
    for x in range(clean_img.width):
        current_pixel = clean_img.getpixel((x, y))
        # 如果当前像素是污点，我们将其替换为白色，这里假设图片背景是白色的
        if current_pixel[0] < threshold and current_pixel[1] < threshold and current_pixel[2] < threshold:
            clean_img.putpixel((x, y), (255, 255, 255, 255))
            dirty_pixels.append((x, y))

# 保存清洁的图像
clean_img_path = 'clean_image.png'
clean_img.save(clean_img_path)

# 打印出污点位置
print(dirty_pixels)


# 将污点位置存储到文本文件
dirty_pixels_path = 'dirty_pixels.txt'
with open(dirty_pixels_path, 'w') as file:
    for pixel in dirty_pixels:
        file.write(f'{pixel[0]},{pixel[1]}\n')