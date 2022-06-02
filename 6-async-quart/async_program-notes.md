## Inspecting async_program.py

This script adds asynchronous functionality to sync_program.py

### Import the asyncio library
```
import asyncio
```

### Convert data list to async queue
Within the main function `data` is converted from a `list` to `asyncio.Queue()`, an instance of a FIFO queue. This asynchronous queue will allow flexible `await` operations with `get()` and `put()` methods for data that is generated and processed
```python
def main():
	...
    data = asyncio.Queue()
    ...
```
### Converting functions to async coroutines

#### generate_data()

Here is our original `generate_data()` function
```python
def generate_data(num: int, data: list):
    for idx in range(1, num + 1): 
        item = idx*idx
        data.append((item, datetime.datetime.now()))

        print(colorama.Fore.YELLOW + f" -- generated item {idx}", flush=True)
        time.sleep(random.random() + .5)
```

Here is the async implementation
```python
async def generate_data(num: int, data: asyncio.Queue):
    for idx in range(1, num + 1): 
        item = idx*idx
        await data.put((item, datetime.datetime.now()))

        print(colorama.Fore.YELLOW + f" -- generated item {idx}", flush=True)
        await asyncio.sleep(random.random() + .5)
```

1. Functions that are going to participate in async event loop, must be introduced with `async def` - these become coroutine objects (similar to generators)

2. Data is published to the queue using `put()` async queue method

3. async `await` keyword signals to the event loop where this coroutine can be suspended to pass control to another coroutine (similiar to generator `yield`):

- When generated data is `put()` into the queue
- While `asyncio.sleep` is called (sleep is used to simulate time waiting on IO)

4. `time.sleep` is changed to the async version since only awaitable objects can be called with the `await` keyword

#### process_data()

Original function

```python
def process_data(num: int, data: list):
    processed = 0
    while processed < num:
        item = data.pop(0)
        if not item:
            time.sleep(.01)
            continue
    
        processed += 1
        value = item[0]
        t = item[1]
        dt = datetime.datetime.now() - t
        
        print(colorama.Fore.CYAN +
              " +++ Processed value {} after {:,.2f} sec.".format(value, dt.total_seconds()), flush=True)
        time.sleep(.5)
````
async implementation

```python
async def process_data(num: int, data: asyncio.Queue):
    processed = 0
    while processed < num:
        item = await data.get()
        
        processed += 1
        value = item[0]
        t = item[1]
        dt = datetime.datetime.now() - t

        print(colorama.Fore.CYAN +
              " +++ Processed value {} after {:,.2f} sec.".format(value, dt.total_seconds()), flush=True)
        await asyncio.sleep(.5)
```
Again we introduce the function with `async def` and add the `await` keyword to the `get()` method for the async queue. Then convert the sleep function to the awaitable async version.

### Onto the main function

Some work needs to be done on main to complete the async functionality
```python
def main():
    t0 = datetime.datetime.now()
    print(colorama.Fore.WHITE + "App started.", flush=True)
    data = asyncio.Queue()
    generate_data(20, data)
    process_data(20, data)

    dt = datetime.datetime.now() - t0
    print(colorama.Fore.WHITE + "App exiting, total time: {:,.2f} sec.".format(dt.total_seconds()), flush=True)
```
1. Create an async loop, functions within loop will share execution time  
`loop = asyncio.get_event_loop()`

2. Create tasks for each of primary coroutines within the async loop  
`task1 = loop.create_task(generate_data(20, data))`  
`task2 = loop.create_task(process_data(20, data))`  

3. Create third task from first two   
`final_task = asyncio.gather(task1, task2)  

4. Execute loop  
`loop.run_until_complete(final_task)  

Final:

```python
def main():
    t0 = datetime.datetime.now()
    print(colorama.Fore.WHITE + "App started.", flush=True)
    
    loop = asyncio.get_event_loop()
    data = asyncio.Queue()

    task1 = loop.create_task(generate_data(20, data))
    task2 = loop.create_task(process_data(20, data))

    final_task = asyncio.gather(task1, task2)
    loop.run_until_complete(final_task)

    dt = datetime.datetime.now() - t0
    print(colorama.Fore.WHITE + "App exiting, total time: {:,.2f} sec.".format(dt.total_seconds()), flush=True)
```

### Output
```python
App started.
 -- generated item 1
 +++ Processed value 1 after 0.00 sec.
 -- generated item 2
 +++ Processed value 4 after 0.00 sec.
 -- generated item 3
 +++ Processed value 9 after 0.00 sec.
 -- generated item 4
 +++ Processed value 16 after 0.00 sec.
 -- generated item 5
 +++ Processed value 25 after 0.00 sec.
 -- generated item 6
 +++ Processed value 36 after 0.00 sec.
 -- generated item 7
 +++ Processed value 49 after 0.00 sec.
 -- generated item 8
 +++ Processed value 64 after 0.00 sec.
 -- generated item 9
 +++ Processed value 81 after 0.00 sec.
 -- generated item 10
 +++ Processed value 100 after 0.00 sec.
 -- generated item 11
 +++ Processed value 121 after 0.00 sec.
 -- generated item 12
 +++ Processed value 144 after 0.00 sec.
 -- generated item 13
 +++ Processed value 169 after 0.00 sec.
 -- generated item 14
 +++ Processed value 196 after 0.00 sec.
 -- generated item 15
 +++ Processed value 225 after 0.00 sec.
 -- generated item 16
 +++ Processed value 256 after 0.00 sec.
 -- generated item 17
 +++ Processed value 289 after 0.00 sec.
 -- generated item 18
 +++ Processed value 324 after 0.00 sec.
 -- generated item 19
 +++ Processed value 361 after 0.00 sec.
 -- generated item 20
 +++ Processed value 400 after 0.00 sec.
App exiting, total time: 19.39 sec.
```

## Notes

Taken from real python's [Async IO in Python: A complete Walkthrough](https://realpython.com/async-io-python/) :

Async IO takes long waiting periods in which functions would otherwise be blocking and allows other functions to run during that downtime. (A function that blocks effectively forbids others from running from the time that it starts until the time that it returns.)

At the heart of async IO are coroutines. A coroutine is a specialized version of a Python generator function... A coroutine is a function that can suspend its execution before reaching return, and it can indirectly pass control to another coroutine for some time.

The use of `await` is a signal that marks a break point. It lets a coroutine temporarily suspend execution and permits the program to come back to it later. `await` must be used with awaitable objects (for example, coroutines)

A key feature of coroutines is that they can be chained together. (Remember, a coroutine object is awaitable, so another coroutine can await it.) This allows you to break programs into smaller, manageable, recyclable coroutines
