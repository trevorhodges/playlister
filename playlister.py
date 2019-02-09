from bs4 import BeautifulSoup
import requests
import pdb
import lxml
from lxml import etree
import argparse

def get_title(vid):
    url = "http://www.youtube.com/watch?v={0}".format(vid)
    youtube = etree.HTML(requests.get(url).text)
    video_title = youtube.xpath("//span[@id='eow-title']/@title")
    return video_title[0]

def get_all_pages(url, count):
    pages = []
    for i in range(1, count):
        sourceCode = requests.get(url.format(i)).text
        soup = BeautifulSoup(sourceCode, 'html.parser')
        pages.append(soup)
    return pages

def get_all_links(pages, tag, prop):
    links = []
    for page in pages:
        for link in page.find_all(tag):
            src = link.get(prop)
            if 'youtube' in src:
                links.append(src)
    return links

def get_all_ids(links):
    yt_url = 'https://youtube.com/embed/'
    id_length = 11
    ids = []
    for link in links:
        ids.append(link.split(yt_url)[1][0:id_length])
    return ids

def filter_existing(ids):
    thumbnail = 'https://img.youtube.com/vi/{0}/0.jpg'
    existing = []
    for ytid in ids:
        exists = requests.get(thumbnail.format(ytid)).status_code == 200
        if exists:
            existing.append(ytid)
    return existing

def get_playlist_ids(url, pages):
    tag = "iframe"
    prop = "src"
    
    print("Getting %s pages..." % pages)
    pages = get_all_pages(url, pages)
    print("Done getting pages, processing links...")
    links = get_all_links(pages, tag, prop)
    print("Found %s YouTube links" % len(links))
    print("Filtering by existing...")
    ids = filter_existing(get_all_ids(links))
    print("IDs found: %s" % ids)
    return ids

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Collect all YouTube links from forum pages and create a YouTube playlist from them')
    parser.add_argument(
            'url',
            help='URL for forum post, replace page number with {}',
            default='https://forum.watmm.com/topic/75217-italo-disco/page-{}')
    parser.add_argument('count', help='Page count', type=int)
    args = parser.parse_args()

    # get youtube ideo ids from forum pages
    ids = list(set(get_playlist_ids(args.url, args.count)))

    # break list into chunks of 49 (max auto generated playlist length)
    chunks = [ids[x:x+49] for x in range(0, len(ids), 49)]

    # with a little manual assistance, process each chunk
    for chunk in chunks:
        print("Visit the following page to create an auto playlist:")
        print('https://www.youtube.com/watch_videos?video_ids=' + ','.join(chunk))
        playlist_id = input("Enter playlist id (found in URL 'list' parameter):")
        print("Visit the following page to show the play list, from where you can add contents to another managed playlist:")
        print("https://www.youtube.com/playlist?list=%s&disable_polymer=true" % playlist_id)
        input("Ready to continue? Hit enter")
