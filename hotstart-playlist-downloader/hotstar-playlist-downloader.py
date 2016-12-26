#!/usr/bin/env python
import sys
import re
import requests
import subprocess

re_link = re.compile(r'.*?hotstar\.com/tv/(?!/).*/[0-9]{4}/episodes/([0-9].*)/'
                     r'[0-9].*')


def get_hotstar_links(playlist_id):
    url = 'http://search.hotstar.com/AVS/besc?action=SearchContents&appVersi' \
          'on=5.0.37&channel=PCTV&maxResult=10000&moreFilters=series:'\
          + playlist_id \
          + '%3B&query=*&searchOrder=last_broadcast_date+desc,year+desc,titl' \
            'e+asc&startIndex=0&type=EPISODE'
    request = requests.get(url)
    request.raise_for_status()
    json_obj = request.json()
    if json_obj['resultCode'] != 'OK':
        print('Error fetching results. Aborting')
        sys.exit(1)
    return ['http://www.hotstar.com/%s' % x['contentId']
            for x in json_obj['resultObj']['response']['docs']]


def download(link):
    print('Downloading ' + link)
    command = 'youtube-dl ' + link
    subprocess.call(command, shell=True)


def download_many(links):
    for link in links:
        download(link)


def main():
    link = sys.argv[1]
    match = re_link.match(link)
    if not match:
        print('Invalid URL')
        sys.exit(1)
    playlist_id = match.groups()[0]
    links = get_hotstar_links(playlist_id)
    download_many(links)

if __name__ == '__main__':
    main()
