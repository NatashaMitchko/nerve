#!/usr/bin/env python
# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.g

"""
This script uses the Vision API's label detection capabilities to find a label
based on an image's content.

"""

import argparse
import base64
import googleapiclient.discovery

def get_labels_for_image(photo_file, maxResults):
    """Run a label request on a single image
       Takes an image and a result limit. Returns list of descriptors."""

    # [START authenticate]
    service = googleapiclient.discovery.build('vision', 'v1')
    # [END authenticate]

    # [START construct_request]
    with open(photo_file, 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'LABEL_DETECTION',
                    'maxResults': maxResults
                }]
            }]
        })
        # [END construct_request]
        # [START parse_response]
        response = service_request.execute()
        annotation = []
        for response in response['responses'][0]['labelAnnotations']:
            annotation.append(response['description'])
        print annotation
        return annotation
        # [END parse_response]


def get_logo_for_image(photo_file):
    """Run a label request on a single image"""

    # [START authenticate]
    service = googleapiclient.discovery.build('vision', 'v1')
    # [END authenticate]

    # [START construct_request]
    with open(photo_file, 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'LOGO_DETECTION',
                    'maxResults': 2
                }]
            }]
        })
        # [END construct_request]
        # [START parse_response]
        response = service_request.execute()
        annotation = []
        for response in response['responses'][0]['logoAnnotations']:
            annotation.append(response['description'])
        print annotation
        return annotation
        # [END parse_response]

def image_is_safe(photo_file):
    """Runs SafeSearch request on a single image.
       Returns False for unsafe images. Unsafe images are defined to be those
       that are LIKELY or VERY_LIKELY to contain adult or violent content."""

    # [START authenticate]
    service = googleapiclient.discovery.build('vision', 'v1')
    # [END authenticate]

    # [START construct_request]
    with open(photo_file, 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'SAFE_SEARCH_DETECTION',
                }]
            }]
        })
        # [END construct_request]
        # [START parse_response]
        response = service_request.execute()
        adult = response['responses'][0]['safeSearchAnnotation']['adult']
        violent = response['responses'][0]['safeSearchAnnotation']['violence']
        # [END parse_response]
        return adult in ['UNLIKELY', 'VERY_UNLIKELY'] or violence in ['UNLIKELY', 'VERY_UNLIKELY']








