import time
import threading
import multiprocessing
import asyncio
import aiohttp
import requests
import re
from collections import Counter


def count_words_in_chunk(text_chunk: str) -> Counter:
    """Finds all words in a text and counts their frequency."""
    words = re.findall(r'\b\w+\b', text_chunk.lower())
    return Counter(words)


class ConcurrencyService:
    """Service to demonstrate Threading, Multiprocessing, and Asyncio."""

    @staticmethod
    def run_task_a_threading() -> tuple:
        """Task A: 5 threads download 5 articles from different sources. Uses Lock."""
        urls = [
            "https://en.wikipedia.org/wiki/Concurrency_(computer_science)",
            "https://docs.python.org/3/tutorial/index.html",
            "https://docs.djangoproject.com/en/5.0/intro/tutorial01/",
            "https://peps.python.org/pep-0008/",
            "https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview"
        ]

        shared_texts = []
        lock = threading.Lock()

        def fetch_article(url):
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                response = requests.get(url, headers=headers, timeout=5)

                if response.status_code == 200:
                    text_data = response.text * 50
                    with lock:
                        shared_texts.append(text_data)
            except requests.RequestException:
                pass

        start_time = time.perf_counter()
        threads = []

        for url in urls:
            t = threading.Thread(target=fetch_article, args=(url,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        execution_time = time.perf_counter() - start_time
        return shared_texts, execution_time

    @staticmethod
    def run_task_b_multiprocessing(texts: list) -> tuple:
        """Task B: Count word frequency in massive texts using Process Pool."""
        start_time = time.perf_counter()

        if not texts:
            return [], time.perf_counter() - start_time

        cpu_cores = multiprocessing.cpu_count()
        with multiprocessing.Pool(processes=cpu_cores) as pool:
            counters = pool.map(count_words_in_chunk, texts)

        total_counter = sum(counters, Counter())
        top_words = total_counter.most_common(10)

        execution_time = time.perf_counter() - start_time
        return top_words, execution_time

    @staticmethod
    async def _check_url_async(session, url: str) -> tuple:
        """Async helper: Checks HTTP 200 status."""
        try:
            async with session.get(url, timeout=5) as response:
                return url, response.status == 200
        except Exception:
            return url, False

    @staticmethod
    async def _run_task_c_async() -> list:
        """Async helper: Gathers 20 concurrent requests."""
        urls = [
            "https://www.google.com", "https://www.github.com", "https://www.python.org",
            "https://www.djangoproject.com", "https://www.postgresql.org", "https://www.docker.com",
            "https://www.ubuntu.com", "https://www.linux.org", "https://www.microsoft.com",
            "https://www.apple.com", "https://www.amazon.com", "https://www.cloudflare.com",
            "https://www.nginx.com", "https://www.apache.org", "https://www.redis.io",
            "https://www.mongodb.com", "https://www.mysql.com", "https://www.sqlite.org",
            "https://www.debian.org", "https://www.centos.org"
        ]

        async with aiohttp.ClientSession() as session:
            tasks = [ConcurrencyService._check_url_async(session, url) for url in urls]
            return await asyncio.gather(*tasks)

    @staticmethod
    def run_task_c_asyncio() -> tuple:
        """Task C: Async check of 20 URLs triggered from synchronous Django."""
        start_time = time.perf_counter()
        results = asyncio.run(ConcurrencyService._run_task_c_async())
        execution_time = time.perf_counter() - start_time
        return results, execution_time