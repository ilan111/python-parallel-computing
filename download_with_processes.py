import multiprocessing
import requests

def downloader(process_id, url, queue):
    try:
        response = requests.get(url)
        chars_in_json = len(response.text)
        queue.put((process_id, chars_in_json, url))

    except Exception as e:
        print(f"Error with thread {process_id}, url - {url}: {e}")

def main():
    CHARS_COUNTER = 0
    queue = multiprocessing.Queue()
    processes = []
    urls = [
        'https://jsonplaceholder.typicode.com/posts',
        'https://jsonplaceholder.typicode.com/comments',
        'https://jsonplaceholder.typicode.com/albums',
        'https://jsonplaceholder.typicode.com/photos',
        'https://jsonplaceholder.typicode.com/todos',
        'https://jsonplaceholder.typicode.com/users'
    ]

    for i, url in enumerate(urls):
        process = multiprocessing.Process(target=downloader, args=(i, urls[i], queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    while not queue.empty():
        process_id, chars, url = queue.get()
        CHARS_COUNTER += chars
        print(f"Process {process_id} Downloaded {chars} chars from {url}")

    print(f"Total number of chars downloaded is: {CHARS_COUNTER}")

if __name__ == "__main__":
    main()