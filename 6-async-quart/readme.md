# Async Flask APIs with Quart

This project uses Quart to present information from the NASA APOD and The Solar System OpenDATA APIs
## Overview

### Screenshot

![](https://github.com/VadidEisrra/100daysofWeb/blob/main/images/6-flask-apis-1.png)
![](https://github.com/VadidEisrra/100daysofWeb/blob/main/images/6-flask-apis-2.png)

## My process

### Built with

- Quart
- aiohttp
- HTML markup
- CSS custom properties

### What I learned

#### Asynchronous programming with the `asyncio` library

Up until this point all python code I have written has been synchronous i.e. functions run sequentially; blocking execution of other tasks until they complete. 

Asynchronous programming is a paradigm which introduces the concept of concurrency or cooperative multitasking. An asyncio application can run async declared functions or coroutines in an event loop - when a coroutine needs to wait on some IO like responses from an API or database they can suspend execution and return control to the loop to run other coroutines.

##### Coroutines

Coroutines mainly refer to:
- coroutine function: an `async def` function
- coroutine object: an object returned by calling a coroutine function

For example, `main()` becomes a coroutine when we declare it with `async def`
```python
>>> import asyncio

>>> async def main():
...     print('hello')
...     await asyncio.sleep(1)
...     print('world')
```
Calling a coroutine does not execute it
```python
>>> main()
<coroutine object main at 0x1053bb7c8>
```
Coroutines can be executed in three ways:
1. `asyncio.run()`
```python
>>> asyncio.run(main())
hello
world
```
2. Awaiting on a coroutine: here the execution of the `say_after` coroutine occurs within `main()` using the `await` keyword
```python
import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    print(f"started at {time.strftime('%X')}")

    await say_after(1, 'hello')
    await say_after(2, 'world')

    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())
```
3. `asyncio.create_task()` function to run coroutines concurrently as asyncio Tasks in an event loop
- The above example is modified to run two `say_after` coroutines concurrently
```python
async def main():
    task1 = asyncio.create_task(
        say_after(1, 'hello'))

    task2 = asyncio.create_task(
        say_after(2, 'world'))

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    await task1
    await task2

    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())
```
- Note the `await` keyword can only be used in an expression with an awaitable object. Some examples of awaitable objects are coroutines and Tasks

#### Making asynchronous http requests using `aiohttp`

Our old synchronous code used requests to retrieve data from APIs, which does not support async. AIOHTTP is an asynchronous HTTP Client/Server library with support for asyncio. Here's how we make client requests to the nasa APOD with aiohttp

Import aiohttp module, and asyncio
```python
import aiohttp
import asyncio
```
The HTTP request is performed in three steps
```python
async def get_apod():
    url =  "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
    async with aiohttp.ClientSession() as session: #step one
        async with session.get(url) as resp: #step two
            data = await resp.json() #step three
    return data
```
- `async with aiohttp.CientSession()` does not perform I/O when entering the block - but ensures all remaining resources are closed correctly at the end. The session object manages a pool of connections you can reuse instead of opening and closing a new one at each request
- `async with session.get()` sends a GET request to the URL, which is asynchronous operation marked with an `async with` so it is non-blocking and cleanly finalized
- Loading the JSON response after the request is our second asynchronous operation noted by the `await` keyword


### Useful resources

- [asyncio docs](https://docs.python.org/3/library/asyncio.html)
- This [asyncio walkthrough](https://realpython.com/async-io-python/) by Brad Solomon
- [aiohttp docs](https://docs.aiohttp.org/en/stable/)
- [Quart docs](https://pgjones.gitlab.io/quart/)
