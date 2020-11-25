
import argparse
import functools
import json
import sys

import requests
import semver


def get_image_meta(image):
    """Retrieve meta data from docker hub for tags of an image.

    :param image: image name.
    """
    tags = list()
    addr = 'https://hub.docker.com/v2/repositories/{}/tags'.format(image)
    while True:
        response = requests.get(addr)
        tags_data = json.loads(response.content.decode())
        tags.extend(tags_data['results'])
        if tags_data['next'] is not None:
            addr = tags_data['next']
        else:
            break
    return tags


def get_image_tags(image, prefix='v'):
    """Retrieve tags from dockerhub of an image.

    :param image: image name, organisation/repository.
    :param prefix: prefix by which to filter images.

    :returns: sorted list of tags, newest first, ordered by semver.
    """
    tags_data = get_image_meta(image)
    tags = list()
    for t in tags_data:
        name = t['name']
        if prefix is not None:
            if name.startswith(prefix):
                name = name[len(prefix):]
            else:
                continue

        try:
            semver.parse(name)
        except ValueError:
            continue
        else:
            tags.append(name)
    ordered_tags = sorted(
        tags, reverse=True,
        key=functools.cmp_to_key(semver.compare))
    if prefix is not None:
        ordered_tags = ['{}{}'.format(prefix, x) for x in ordered_tags]
    return ordered_tags


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch image tags from dockerhub')
    parser.add_argument('imagename', help='Image name: namespace/image.')
    parser.add_argument('--prefix', help='Filter image tags by matching prefix.')
    parser.add_argument('--list', action='store_true', help='List all tags, not just latest')
    args = parser.parse_args()
    tags = get_image_tags(args.imagename, prefix=args.prefix)
    if len(tags) == 0:
        print("No tags found.")
        sys.exit(1)
    if args.list:
        for tag in tags:
            print(tag)
    else:
        print(tags[0])
