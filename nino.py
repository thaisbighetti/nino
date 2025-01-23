import argparse
import aiohttp
import asyncio

async def fetch(session, url):
    """Faz uma requisição assíncrona e retorna o status HTTP sem seguir redirecionamentos."""
    try:
        async with session.get(url) as response:
            return response.status
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

async def requests_to_url(base_url, wordlist, max_depth):
    """
    Faz requisições recursivas baseadas na lista de palavras.
    Para cada palavra encontrada, combina com outras palavras do wordlist,
    mas evita URLs repetitivas ou profundidade excessiva.
    """
    async with aiohttp.ClientSession() as session:
        wordlist = [line.strip() for line in wordlist]
        arguments_found = set()  
        stack = [(word, 1) for word in wordlist]  

        while stack:
            current_path, depth = stack.pop()
            
            if depth > max_depth:
                continue

            current_path = current_path.strip("/")
            current_url = f"{base_url.rstrip('/')}/{current_path}"

            status = await fetch(session, current_url)

            if status == 404:
                continue

            if status == 200:
                if current_path not in arguments_found:
                    print(f"Found: {current_url}")
                    arguments_found.add(current_path)

                for word in wordlist:
                    new_path = f"{current_path.strip('/')}/{word.strip('/')}"
                    if new_path not in arguments_found:
                        stack.append((new_path, depth + 1))

    return arguments_found

async def main():
    """Ponto de entrada principal para o script."""
    parser = argparse.ArgumentParser(description='Send async requests to a URL with a list of words')
    parser.add_argument('--wordlist', type=argparse.FileType('r'), required=True, help='A txt file containing a list of words')
    parser.add_argument('--url', type=str, required=True, help='A URL to send requests to')
    parser.add_argument('--max-depth', type=int, default=2, help='Maximum recursion depth')

    args = parser.parse_args()
    wordlist = args.wordlist.readlines()

    await requests_to_url(args.url, wordlist, args.max_depth)

if __name__ == "__main__":
    asyncio.run(main())
