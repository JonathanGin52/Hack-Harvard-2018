#!/usr/bin/env python

# Copyright 2015 Google, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os

# [START vision_face_detection_tutorial_imports]
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image
# [END vision_face_detection_tutorial_imports]


# [START vision_face_detection_tutorial_send_request]
def detect_face(face_file, max_results=100):
    """Uses the Vision API to detect faces in the given file.

    Args:
        face_file: A file-like object containing an image with faces.

    Returns:
        An array of Face objects with information about the picture.
    """
    # [START vision_face_detection_tutorial_client]
    client = vision.ImageAnnotatorClient()
    # [END vision_face_detection_tutorial_client]

    content = face_file.read()
    image = types.Image(content=content)

    return client.face_detection(image=image).face_annotations
# [END vision_face_detection_tutorial_send_request]


# [START vision_face_detection_tutorial_run_application]
def main(input_folder, output_filename, max_results):
    input_folder += '' if '/' in input_folder else '/'
    images = os.listdir(input_folder)
    for input_image in images:
        with open(input_folder + input_image, 'rb') as image:
            faces = detect_face(image, max_results)
            print('{}: Found {} face{}'.format(input_image, len(faces), '' if len(faces) == 1 else 's'))

            # Reset the file pointer, so we can read the file again
            image.seek(0)
# [END vision_face_detection_tutorial_run_application]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Detects faces in the given image.')
    parser.add_argument(
        'input_folder', help='the folder of images you\'d like to detect faces in.')
    parser.add_argument(
        '--out', dest='output', default='out.jpg',
        help='the name of the output file.')
    parser.add_argument(
        '--max-results', dest='max_results', default=100,
        help='the max results of face detection.')
    args = parser.parse_args()

    main(args.input_folder, args.output, args.max_results)
