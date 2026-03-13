from PIL import Image, ImageDraw

def fill_beaker(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")

    # Create a mask for the liquid
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)

    # Coordinates for Beaker A
    left_x = 151
    right_x = 282
    bottom_y = 414
    top_y = 300

    draw.rectangle((left_x, top_y, right_x, bottom_y - 10), fill=255)
    draw.ellipse((left_x, bottom_y - 20, right_x, bottom_y), fill=255)
    draw.ellipse((left_x, top_y - 8, right_x, top_y + 8), fill=255)

    pixels = img.load()
    mask_pixels = mask.load()

    for y in range(img.height):
        for x in range(img.width):
            if mask_pixels[x, y] > 0:
                r, g, b, a = pixels[x, y]
                # Dark pixels (lines) stay mostly dark
                if r < 120 and g < 120 and b < 120:
                    pass
                else:
                    alpha = 0.5
                    new_r = int(r * (1 - alpha) + 0 * alpha)
                    new_g = int(g * (1 - alpha) + 120 * alpha)
                    new_b = int(b * (1 - alpha) + 255 * alpha)
                    pixels[x, y] = (new_r, new_g, new_b, a)

    # Draw a darker/slightly different meniscus line
    meniscus_mask = Image.new('L', img.size, 0)
    draw_m = ImageDraw.Draw(meniscus_mask)
    draw_m.ellipse((left_x, top_y - 8, right_x, top_y + 8), fill=255)
    m_pixels = meniscus_mask.load()

    for y in range(img.height):
        for x in range(img.width):
            if m_pixels[x, y] > 0:
                r, g, b, a = pixels[x, y]
                if r >= 120 or g >= 120 or b >= 120:
                    alpha = 0.3
                    new_r = int(r * (1 - alpha) + 0 * alpha)
                    new_g = int(g * (1 - alpha) + 80 * alpha)
                    new_b = int(b * (1 - alpha) + 200 * alpha)
                    pixels[x, y] = (new_r, new_g, new_b, a)

    img = img.convert("RGB")
    img.save(output_path)
    print(f"Saved filled beaker to {output_path}")

if __name__ == "__main__":
    fill_beaker("/tmp/file_attachments/image.png", "image.png")
