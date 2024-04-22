from httpx import AsyncClient
from bot.config import ATG_API


async def shorten_url(url: str) -> str:
    async with AsyncClient() as client:
        r = await client.get(f'https://atglinks.com/api?api={ATG_API}&url={url}')
        return r.json()['shortenedUrl']
