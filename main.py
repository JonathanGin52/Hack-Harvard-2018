import argparse
import os
from shutil import rmtree
from analyze import detect_faces, get_average_hsv
from scraper import scrape

def results(average_hsv):
    pass


def main(input_folder, args):
    # Append '/' to folder location if not present
    total_faces = total_h = total_s = total_v = 0.0
    image_count = 0

    input_folder += '' if '/' in input_folder else '/'
    images = [img for img in os.listdir(input_folder) if img.endswith('.jpg')]

    for input_image in images:
        image_count += 1
        with open(input_folder + input_image, 'rb') as image:
            faces = detect_faces(image)
            total_faces += len(faces)

            h, s, v = get_average_hsv(input_folder + input_image)
            total_h += h
            total_s += s
            total_v += v

            if args.verbose:
                print('{}: Found {} face{}\n'.format(input_image, len(faces), '' if len(faces) == 1 else 's'))
                print("Average hue: {}\nAverage saturation: {}\nAverage value: {}".format(h, s, v))          

            # Reset the file pointer, so we can read the file again
            image.seek(0)

    if args.verbose: print("\nThere is an average of {} faces in each photo.".format(total_faces / image_count))            

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyses an IG feed for signs and of depression')
    parser.add_argument('-d', '--debug', help="Flag to keep temp files upon completion.", action="store_true", default=False)
    parser.add_argument('-v', '--verbose', help="Enable verbose output.", action="store_true", default=False)
    args = parser.parse_args()

    folder = 'temp/'
    username = input("Enter an Instagram username: ")
    scrape(username)
    main(folder, args)
    try:
        if not args.debug: rmtree(folder)
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))
