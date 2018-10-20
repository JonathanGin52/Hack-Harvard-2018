import argparse
import os
from shutil import rmtree
from analyze import detect_faces, get_average_hsv
from scraper import scrape

def main(input_folder):
    # Append '/' to folder location if not present
    total_faces = 0.0
    image_count = 0
    input_folder += '' if '/' in input_folder else '/'
    images = [img for img in os.listdir(input_folder) if img.endswith('.jpg')]
    for input_image in images:
        image_count += 1
        with open(input_folder + input_image, 'rb') as image:
            faces = detect_faces(image)
            total_faces += len(faces)
            print('{}: Found {} face{}'.format(input_image, len(faces), '' if len(faces) == 1 else 's'))

            get_average_hsv(input_folder + input_image)
            print()
            # Reset the file pointer, so we can read the file again
            image.seek(0)
    print("There is an average of {} faces in each photo.".format(total_faces / image_count))            

if __name__ == '__main__':
    #parser = argparse.ArgumentParser(
    #    description='Detects faces in the given image.')
    #parser.add_argument(
    #    'input_folder', help='the folder of images you\'d like to detect faces in.')
    #parser.add_argument(
    #    '--out', dest='output', default='out.jpg',
    #    help='the name of the output file.')
    #args = parser.parse_args()

    folder = 'temp/'
    username = input("Enter an Instagram username: ")
    scrape(username)
    main(folder)
    try:
        rmtree(folder)
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))
