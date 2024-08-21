# Abyssinia AI - Wikipedia corpus fetcher
import os
import requests
from bs4 import BeautifulSoup
from code.logger import logger


def fetch_and_save_page(title, data_dir='data'):
    url = f'https://en.wikipedia.org/wiki/{title.replace(chr(32), chr(95))}'
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = '\n'.join([p.get_text() for p in soup.find_all('p')])
        if not text.strip():
            logger.warning(f'No content found for {title}')
            return None
        os.makedirs(data_dir, exist_ok=True)
        file_path = os.path.join(data_dir, f'{title}.txt')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        logger.info(f'Saved page {title} to {file_path}')
        return file_path
    except Exception as e:
        logger.error(f'Failed to fetch {title}: {e}')
        return None
