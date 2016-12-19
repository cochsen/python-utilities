import argparse
import asyncio
import hashlib
from urllib.parse import urlsplit

import aiohttp

chunk_size = 1024

async def download_url(url, destination):
    # download a resource from a url and get the sha256 checksum
    print('Downloading {}'.format(url))
    file_hash = hashlib.sha256()
    with open(destination, 'wb') as file:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                while True:
                    chunk = await response.content.read(chunk_size)
                    if not chunk:
                        break
                    file_hash.update(chunk)
                    file.write(chunk)

    print('Downloaded {}, sha256: {}'.format(destination, file_hash.hexdigest()))

def main():
    # get the URL from the command-line args
    parser = argparse.ArgumentParser()
    parser.add_argument('url', metavar='URL', help='The URL to download')
    arguments = parser.parse_args()

    # get the filename from the URL
    url_parts = urlsplit(arguments.url)
    file_name = url_parts.path[url_parts.path.rfind('/')+1:]

    # start the download asynchronously
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download_url(arguments.url, file_name))

if __name__ == '__main__':
    main()
