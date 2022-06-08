import os
import sys
import shutil
import requests
import argparse
import time
import random
from bs4 import BeautifulSoup


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', required=True, help='File where each line is a link to idos discussion.')
    parser.add_argument('-o', '--output-path', required=True, help='Where downloaded files will be stored.', )

    args = parser.parse_args()
    return args


def download_discussion(session, output_path, url):
    for i in range(1, 500):
        full_url = f'{url}/diskuse/{i}'
        r = session.get(full_url, allow_redirects=False)
        if r.status_code != 200:
            print('Failed', full_url, r.status_code)
            break

        if 'Řadit diskuse' in r.text and 'podle data posledního příspěvku' in r.text and 'podle času založení komentáře' in r.text:
            print('No discussion', full_url, r.status_code)
            break

        soup = BeautifulSoup(r.text, 'html.parser')
        if len(soup.find_all('div', {"class": "user-text"})) == 0:
            print('No user-text', full_url, r.status_code)
            break

        print('DOWNLOADED', full_url)
        with open(f'{output_path}.{i:02d}.html', 'w', encoding=r.encoding) as f:
            f.write(r.text)
        time.sleep(random.uniform(1, 2))


def main():
    args = parse_arguments()
    with requests.Session() as session:
        for line in open(args.input, 'r'):
            line = line.strip()
            output_path = line.split('/')[-1]
            output_path = os.path.join(args.output_path, output_path)
            download_discussion(session, output_path, line)


if __name__ == '__main__':
    main()

