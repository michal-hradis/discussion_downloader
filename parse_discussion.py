import os
import argparse
from collections import defaultdict
from bs4 import BeautifulSoup


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input_path', required=True, help='File where each line is a link to idos discussion.')
    parser.add_argument('-o', '--output-path', required=True, help='Where downloaded files will be stored.', )

    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()

    files = [file for file in os.listdir(args.input_path) if 'html' in file]
    articles = defaultdict(list)
    for file in files:
        article = '.'.join(file.split('.')[:-2])
        articles[article].append(file)

    for article in articles:
        output_file = os.path.join(args.output_path, article + '.txt')
        with open(output_file, 'w', encoding='utf-8') as output_file:
            for file in articles[article]:
                with open(os.path.join(args.input_path, file), 'r', encoding='windows-1250') as input_file:
                    soup = BeautifulSoup(input_file.read(), 'html.parser')
                for div in soup.find_all('div', {"class": "user-text"}):
                    text = div.getText().strip()
                    text = text.encode('utf-8', 'replace').decode()
                    print(text, file=output_file)


if __name__ == '__main__':
    main()


