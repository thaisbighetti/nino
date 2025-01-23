import argparse
import aiohttp
import asyncio
from collections import defaultdict

async def fetch(session, url):
    """Faz uma requisição assíncrona e retorna o status HTTP sem seguir redirecionamentos."""
    try:
        async with session.get(url) as response:
            print(f'{url}')
            return response.status
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

async def requests_to_url(base_url, wordlist):
    """
    Faz requisições recursivas baseadas na lista de palavras.
    Para cada palavra encontrada, combina com outras palavras do wordlist,
    mas evita URLs repetitivas ou profundidade excessiva.
    """
    async with aiohttp.ClientSession() as session:
        # Limpar e organizar o wordlist
        wordlist = [line.strip() for line in wordlist]
        arguments_found = set()  # Conjunto para rastrear URLs já processadas
        stack = set(wordlist)
        new_url = set()  # Inicializa a pilha com todas as palavras do wordlist

        while stack:
            current_path = stack.pop()
            
            current_path = current_path.strip("/")
            current_url = f"{base_url.rstrip('/')}/{current_path}"

            status = await fetch(session, current_url)

            if status == 404:
                continue


            if status == 200:
                print(f"Found: {current_url}")
                arguments_found.add(current_path)

                for word in wordlist:
                    new_path = f"{current_path.strip('/')}/{word.strip('/')}"
                    if word not in arguments_found:
                        print(new_path)
                        stack.add(new_path)


    return arguments_found

async def main():
    """Ponto de entrada principal para o script."""
    parser = argparse.ArgumentParser(description='Send async requests to a URL with a list of words')
    parser.add_argument('--wordlist', type=argparse.FileType('r'), required=True, help='A txt file containing a list of words')
    parser.add_argument('--url', type=str, required=True, help='A URL to send requests to')

    args = parser.parse_args()
    wordlist = args.wordlist.readlines()

    await requests_to_url(args.url, wordlist)

if __name__ == "__main__":
    asyncio.run(main())
