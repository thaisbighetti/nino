import argparse
import requests

def requests_to_url(url, wordlist):
    arguments_found = []
    for line in wordlist:
        line = line.strip()
        response = requests.get(f'{url}/{line}', allow_redirects=True)
        if response.status_code == 200 and line not in arguments_found:
            print(f"Found: {url}/{line}")
            arguments_found.append(line)
            for argument in arguments_found:
                response = requests.get(f'{url}/{line}/{argument}', allow_redirects=True)
                if response.status_code == 200 and argument not in arguments_found:
                    print(f"Found: {url}/{line}/{argument}")
                    arguments_found.append(argument)
    return arguments_found

def main():
    parser = argparse.ArgumentParser(description='Send requests to a url with a list of words')
    parser.add_argument('--wordlist', type=str, required=True, help='a txt file containing a list of words')
    parser.add_argument('--url', type=str, required=True, help='a url to send requests')

    args = parser.parse_args()
    with open(args.wordlist, 'r') as file:
        requests_to_url(args.url, file)

if __name__ == "__main__":
    main()
