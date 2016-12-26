#!/usr/bin/env python
import sys
import re
import requests
import subprocess

re_link_pl = re.compile(r'.*?hotstar\.com/tv/(?!/).*/[0-9].*/episodes/([0-9].*)/[0-9].*')
re_link_se = re.compile(r'.*?hotstar.com/tv/(?!/).*?/([0-9].*)/seasons/season-([0-9])')


def get_playlist_links(playlist_id):
    url = 'http://search.hotstar.com/AVS/besc?action=SearchContents&appVersi' \
          'on=5.0.37&channel=PCTV&maxResult=10000&moreFilters=series:'\
          + playlist_id \
          + '%3B&query=*&searchOrder=last_broadcast_date+desc,year+desc,titl' \
            'e+asc&startIndex=0&type=EPISODE'
    request = requests.get(url)
    request.raise_for_status()
    json_obj = request.json()
    if json_obj['resultCode'] != 'OK':
        return []
    return ['http://www.hotstar.com/%s' % x['contentId']
            for x in json_obj['resultObj']['response']['docs']]


def get_season_links(season):
    url = 'http://account.hotstar.com/AVS/besc?action=GetArrayContentList&a' \
          'ppVersion=5.0.37&categoryId=' + str(season) + '&channel=PCTV'
    request = requests.get(url)
    request.raise_for_status()
    json_obj = request.json()
    return ['http://www.hotstar.com/%s' % x['contentId']
            for x in json_obj['resultObj']['contentList']]


def download(link):
    print('Downloading ' + link)
    command = 'youtube-dl ' + link
    subprocess.call(command, shell=True)


def download_many(links):
    for link in links:
        download(link)


def main():
    link = sys.argv[1]
    links = []
    match_se = re_link_se.match(link)
    if match_se:
        season, offset = map(int, match_se.groups())
        final_season = season + offset - 1
        links += get_season_links(final_season)
    match_pl = re_link_pl.match(link)
    if match_pl:
        playlist_id = match_pl.groups()[0]
        links += get_playlist_links(playlist_id)
    if len(links) == 0:
        print('No links fetched')
        sys.exit(1)
    download_many(links)

if __name__ == '__main__':
    main()
