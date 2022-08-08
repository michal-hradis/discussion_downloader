import os
import time
import random
import requests
import argparse
import datetime
from bs4 import BeautifulSoup
from download_specific_discussions import download_discussion

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output-path', required=True, help='Where downloaded files will be stored.', )
    parser.add_argument('-d', '--day', required=True, type=int,  help='Start day.', )
    parser.add_argument('-m', '--month', required=True, type=int,  help='Start day.', )
    parser.add_argument('-y', '--year', required=True, type=int, help='Start day.', )

    args = parser.parse_args()
    return args


def get_all_articles(session, date):
    links = []
    for i in range(1, 30):
        if i == 1:
            full_url = f"https://www.idnes.cz/zpravy/archiv?datum={date.day}.+{date.month}.+{date.year}&idostrova=idnes"
        else:
            full_url = f"https://www.idnes.cz/zpravy/archiv/{i}?datum={date.day}.+{date.month}.+{date.year}&idostrova=idnes"

        r = session.get(full_url, allow_redirects=False)
        if r.status_code != 200:
            print('Failed', full_url, r.status_code)
            break

        print('PAGE', full_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        articles = soup.find('div', {'id': 'list-art-count'})
        for link in articles.find_all('a', {"class": "art-link"}):
            links.append(link['href'])

        time.sleep(random.uniform(1, 2))

    print(f'HAVE {len(links)} links')
    return links


def main():
    args = parse_arguments()
    date = datetime.date(args.year, args.month, args.day)
    with requests.Session() as session:
        while True:
            time.sleep(random.uniform(1, 2))
            links = get_all_articles(session, date)
            for link in links:
                output_path = date.strftime('%Y-%m-%d') + '_' +link.split('/')[-1]
                output_path = os.path.join(args.output_path, output_path)
                download_discussion(session, output_path, link)
            date -= datetime.timedelta(days=1)


if __name__ == '__main__':
    main()
