# import asyncio
# from aiohttp import ClientSession
# import time
#
#
# async def send_read_request(url):
#     print(f'Start_time: {time.time()}')
#     async with ClientSession() as session:
#         async with session.post(url) as response:
#             res = await response.text()
#             # res = res.result()
#             return res
#
#
# async def send_write_request(url, name, files):
#     print(f'Start_time: {time.time()}')
#     async with ClientSession() as session:
#         async with session.post(url, data=name, files=files) as response:
#             res = await response.text()
#             # res = res.result()
#             return res
#
# async def main():
#     writeurl = "http://localhost:5000/api/upload?key=hot&file"
#     readurl = "http://localhost:5000/api/key/cold"
#     # payload = {'key': 'hot'}
#     # files = [('file', ('hot.jpeg', open('/Users/lwh/Desktop/hot/hot.jpeg', 'rb'), 'image/jpeg'))]
#     payload = {'key': 'hot'}
#     files = ('hot.jpeg', open('/Users/lwh/Desktop/hot/hot.jpeg', 'rb'), 'image/jpeg')
#     task_list = []
#     readResponseTimes = []
#     for i in range(1,2):
#         for j in range(i):
#             # task_read = asyncio.create_task(send_read_request(readurl))
#             # task_list.append(task_read)
#             task_write = asyncio.create_task(send_write_request(writeurl, payload, files))
#             task_list.append(task_write)
#         done, pending = await asyncio.wait(task_list, timeout=None)
#
#         for done_task in done:
#             print(f"{time.time()} Get request result {done_task.result()}")
#
#         latency = time.time() - start_time
#         print(latency)
#         readResponseTimes.append(latency)
#     print(readResponseTimes)
#
#
# # asyncio.run(main())
# start_time = time.time()
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
# # print("Latency: ", time.time() - start_time)
#

import requests
import threading
import time


def send_read_req(count):
    url = "http://localhost:5000/api/key/cold"
    res = requests.request("POST", url, headers={}, data={})
    # print("Thread-" + str(count) + " " + str(res.status_code))
    print(res.text)


def send_write_req(count):
    writeurl = "http://localhost:5000/api/upload?key=hot&file"
    payload = {'key': 'hot'}
    files = [('file', ('hot.jpeg', open('/Users/lwh/Desktop/hot/hot.jpeg', 'rb'), 'image/jpeg'))]
    res = requests.request("POST", writeurl, headers={}, data=payload, files=files)
    # print("Thread-" + str(count) + " " + str(res.status_code))
    print(res.text)


def thread(count):
    read_threads = []
    write_threads = []

    for i in range(count):
        read_thread = threading.Thread(target=send_read_req, args=(i,))
        read_threads.append(read_thread)
        for j in range(4):
            write_thread = threading.Thread(target=send_write_req, args=(i,))
            write_threads.append(write_thread)
    print(read_threads)
    print(write_threads)

    for t in read_threads:
        t.start()
    for t in write_threads:
        t.start()
    for t in read_threads:
        t.join()
    for t in write_threads:
        t.join()


latency = []
for i in range(1, 21):
    start_time = time.time()
    thread(i)
    latency.append(time.time()-start_time)
    print("Time cost: ", time.time()-start_time)

