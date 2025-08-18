import threading
import requests

CHARS_COUNTER = 0

def downloader(mutex, thread_id, url, returns):
    global CHARS_COUNTER
    try:
        response = requests.get(url)
        chars_in_json = len(response.text)

        # Critical section
        with mutex:
            CHARS_COUNTER += chars_in_json

        returns.append((thread_id, chars_in_json, url))

    except Exception as e:
        print(f"Error with thread {thread_id}, url - {url}: {e}")

def main():
    mutex = threading.Lock()
    threads = []
    thread_returns = []
    urls = [
        'https://jsonplaceholder.typicode.com/posts',
        'https://jsonplaceholder.typicode.com/comments',
        'https://jsonplaceholder.typicode.com/albums',
        'https://jsonplaceholder.typicode.com/photos',
        'https://jsonplaceholder.typicode.com/todos',
        'https://jsonplaceholder.typicode.com/users'
    ]

    for i, url in enumerate(urls):
        thread = threading.Thread(target=downloader, args=(mutex, i, urls[i], thread_returns))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    for thread_id, chars, url in thread_returns:
        print(f"thread {thread_id} Downloaded {chars} chars from {url}")

    print(f"Total number of chars downloaded is: {CHARS_COUNTER}")

if __name__ == "__main__":
    main()