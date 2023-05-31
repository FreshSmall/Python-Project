"""
example06.py - 异步I/O版本爬虫
"""
import asyncio
import json
import os

import aiofile
import aiohttp


async def download_picture(session, url):
    filename = url[url.rfind('/') + 1:]
    async with session.get(url, ssl=False) as resp:
        if resp.status == 200:
            data = await resp.read()
            async with aiofile.async_open(f'images/beauty/{filename}', 'wb') as file:
                await file.write(data)


async def fetch_json():
    async with aiohttp.ClientSession() as session:
        for page in range(3):
            async with session.get(
                url=f'https://image.so.com/zjl?ch=beauty&sn={page * 30}',
                ssl=False
            ) as resp:
                if resp.status == 200:
                    json_str = await resp.text()
                    result = json.loads(json_str)
                    for pic_dict in result['list']:
                        await download_picture(session, pic_dict['qhimg_url'])


def main():
    if not os.path.exists('images/beauty'):
        os.makedirs('images/beauty')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_json())
    loop.close()


if __name__ == '__main__':
    main()