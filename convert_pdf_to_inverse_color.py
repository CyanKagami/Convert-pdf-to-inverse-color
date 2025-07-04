import os
import shutil
from pdf2image import convert_from_path
try:
    from PIL import Image
except ImportError:
    os.system("pip install pillow")

def main():
    week = input("Week : ")
    original_file = input("Original file name: ")
    if ".pdf" not in  original_file:
        original_file = original_file + ".pdf"
    new_name = input("Student ID: ")
    if ".pdf" not in new_name:
        new_name = new_name + ".pdf"

    # create directory name by week
    if not os.path.exists(week):
        os.makedirs(week)

    new_name = week + "/" + new_name
    convert_inverse_color_pdf(original_file, new_name)

def convert_inverse_color_pdf(filename, output_name):
    # Define the path to your PDF file
    pdf_path = filename

    # Define the output directory for images
    output_dir = pdf_path.split(".")[0]

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Convert PDF pages to images
    # Each page will be a PIL Image object in the 'images' list
    images = convert_from_path(pdf_path, dpi=200) # dpi can be adjusted for image quality

    image_paths = []
    # Save each image to the output directory
    for i, image in enumerate(images):
        image_filename = os.path.join(output_dir, f'page_{i+1}.png') # You can change format to .jpg
        image.save(image_filename, 'PNG') # Specify the desired image format
        change_pixel_color(image_filename)
        image_paths.append(image_filename)

    convert_to_pdf(image_paths, output_name)
    remove_picture_dir(output_dir)
    print(f"{output_name} Successfully convert to inverse color pdf")

def convert_to_pdf(image_paths, output_name):
    images = []
    for img_path in image_paths:
        try:
            img = Image.open(img_path)
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            images.append(img)
        except FileNotFoundError:
            print(f"Warning: Image file not found at '{img_path}'. Skipping.")
        except Exception as e:
            print(f"An error occurred while processing '{img_path}': {e}. Skipping.")

    if images:
        # Save the first image, then append the rest
        images[0].save(output_name, save_all=True, append_images=images[1:])
        print(f"Multiple images converted and combined into '{output_name}' successfully.")
    else:
        print("No valid images found to convert.")

def remove_picture_dir(picture_dir):
    try:
        if os.path.exists(picture_dir):
            shutil.rmtree(picture_dir)
            print(f"Folder '{picture_dir}' and its contents deleted successfully.")
        else:
            print(f"Folder '{picture_dir}' does not exist.")
    except OSError as e:
        print(f"Error: {e}")

def change_pixel_color(image_path):
    """
    Changes pixels of a specific RGB color to a new RGB color.
    """
    img = Image.open(image_path).convert("RGB")  # Ensure RGB mode
    pixels = img.load()  # Load pixel data

    width, height = img.size
    for x in range(width):
        for y in range(height):
            # if it's white color change to black
            if pixels[x, y] == (255 ,255 ,255):
                pixels[x, y] = (16, 16, 16)
            else:
                pixels[x, y] = (255 - pixels[x, y][0], 255 - pixels[x, y][1], 255 - pixels[x, y][2])

    img.save(image_path)


main()
