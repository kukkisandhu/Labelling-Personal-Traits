#!/usr/bin/python
import argparse
import os
import flickrapi
import flickr_utils

api_key ='762c532aa9bce16b072a502c7bb61311'
api_secret ='34a7f982b6eca927'


def flickr_init():
    flickr = flickrapi.FlickrAPI(api_key, api_secret)

    try:
        flickr.authenticate_via_browser(perms='write')
    except flickrapi.exceptions.FlickrError:
        (token, frob) = flickr.get_token_part_one(perms='write')
        if not token:
            raw_input("Press ENTER after you authorised this program")
        flickr.get_token_part_two((token, frob))

    return flickr


def flickr_search_downloadr(text, tags, user_id, sort, quantity, number, size,
                            title, noclobber, outdir):
    flickr = flickr_init()

    i = 0
    number = None

    filenames = []
    for photo in flickr.walk(
            tag_mode='all',
            user_id=user_id,
            text=text,
            tags=tags,
            sort=sort):

        i += 1
        if quantity and i > quantity:
            return filenames
        if number:
            number = str(i).zfill(6)

        photo_id = photo.attrib['id']
        #print photo_id
        photo_info = flickr.photos_getInfo(photo_id=photo_id)
        photo_info = photo_info[0]
        #print photo_info
        secret = photo_info.attrib['secret']
        if size == 'o':
            if'originalsecret' in photo_info.attrib:
                secret = photo_info.attrib['originalsecret']
            else:
                size = 'b'  # Next best

        if title:
            photo_title = photo.attrib['title']
        else:
            photo_title = None

        #text_file=open("info.txt","w")
        #text_file.write(photo_id)
        #text_file.write(photo_title)
        #text_file.write(photo_info)
        #text_file.close()    
        
        
        ftext = open('C:\Users\gursh\Desktop\API\\metaData.txt','a+')
        ftext.write('%s: ' % photo_title)
        ftext.write('%s: ' % photo_info)
        ftext.write('%s: ' % photo_id)
        ftext.write('%s: ' % user_id)
        ftext.write('%s: ' % text)
        ftext.write('%s: '%quantity)
        ftext.write('%s: ' %size )
        ftext.write('%s: ' % outdir)
        ftext.write('%s:  \r\n' % tags)
        ftext.close()
            





        filename = flickr_utils.download(
            "http://farm%s.static.flickr.com/%s/%s_%s_%s.jpg" %
            (photo.attrib['farm'], photo.attrib['server'],
                photo.attrib['id'], secret, size),
            photo_title, noclobber, number, directory=outdir)
        filenames.append(filename)


    return filenames


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Download from a Flickr search',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "--text",
        help="Search text")
    parser.add_argument(
        "--tags",
        help="Search tags")
    parser.add_argument(
        "-u", "--user_id",
        help="User to download from")
    sort_options = [
        'date-posted-asc', 'date-posted-desc', 'date-taken-asc',
        'date-taken-desc', 'interestingness-desc', 'interestingness-asc',
        'relevance']
    parser.add_argument(
        '--sort',
        default='relevance',
        choices=sort_options,
        help="The order in which to process photos.")
    parser.add_argument(
        "-q", "--quantity", type=int,
        help="Quantity to download")
    parser.add_argument(
        "-s", "--size", default="b",
        choices=("s", "q", "t", "m", "n", "z", "c", "b", "o"),
        help="The size of photo you want to download: "
        "s - 75x75, "
        "q - 150x150, "
        "t - 100 on the longest side, "
        "m - 240 on the longest side, "
        "n - 320 on the longest side, "
        "z - 640 on the longest side, "
        "c - 800 on the longest side, "
        "b - 1024 on the longest side (default), "
        "o - original")
    parser.add_argument(
        "-t", "--title", action="store_true",
        help="Use the title as the filename")
    parser.add_argument(
        "-o", "--outdir",
        help="Output directory")
    parser.add_argument(
        "-nc", "--noclobber", action="store_true",
        help="Don't clobber pre-exisiting files")
    parser.add_argument(
        "-n", "--number", action="store_true",
        help="Prefix filenames with a serial number")
    args = parser.parse_args()

    # Optional, http://stackoverflow.com/a/1557906/724176
    try:
        import timing
        assert timing  
    except ImportError:
        pass

    flickr_search_downloadr(args.text, 'grand pa', args.user_id, args.sort,
                            args.quantity, args.number, args.size, args.title,
                            args.noclobber, args.outdir)


