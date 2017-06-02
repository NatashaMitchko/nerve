"""
This script uses the Google Cloud Vision API's label detection capabilities to 
find a label or logo based on an image's content. It can also be used to 
determine if an image contains adult or violent content.

"""

import argparse
import base64
import googleapiclient.discovery

def get_tags_for_image(photo_file, maxResults=10):
    """Run a label request on a single image
       Takes an image and a result limit. Returns list of descriptors.
       If API call returns no descriptors, return False.

    >>> get_tags_for_image('static/images/snails.jpg', 10)
    [u'snails and slugs', u'snail', u'invertebrate', u'fauna', u'insect', u'macro photography', u'molluscs', u'slug']
    """

    service = googleapiclient.discovery.build('vision', 'v1')

    try:
        with open(photo_file, 'rb') as image:
            image_content = base64.b64encode(image.read())
            service_request = service.images().annotate(body={
                'requests': [{
                    'image': {
                        'content': image_content.decode('UTF-8')
                    },
                    'features': [{
                        'type': 'WEB_DETECTION',
                        'maxResults': maxResults
                    }]
                }]
            })
            response = service_request.execute()

            tags = {tag['description'] for tag in response['responses'][0]['webDetection']['webEntities']}
            return tags
    except:
        return False


# def get_logo_for_image(photo_file):
#     """Run a logo request on a single image

#     """

#     # [START authenticate]
#     service = googleapiclient.discovery.build('vision', 'v1')
#     # [END authenticate]

#     # [START construct_request]
#     with open(photo_file, 'rb') as image:
#         image_content = base64.b64encode(image.read())
#         service_request = service.images().annotate(body={
#             'requests': [{
#                 'image': {
#                     'content': image_content.decode('UTF-8')
#                 },
#                 'features': [{
#                     'type': 'LOGO_DETECTION',
#                     'maxResults': 2
#                 }]
#             }]
#         })
#         # [END construct_request]
#         # [START parse_response]
#         response = service_request.execute()
#         tags = []
#         for response in response['responses'][0]['logoAnnotations']:
#             tags.append(response['description'])
#         print tags
#         return tags
#         # [END parse_response]

def image_is_safe(photo_file):
    """Runs SafeSearch request on a single image.
       Returns False for unsafe images. Unsafe images are defined to be those
       that are LIKELY or VERY_LIKELY to contain adult or violent content.

       >>> image_is_safe('static/images/snails.jpg')
       True
       """

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








