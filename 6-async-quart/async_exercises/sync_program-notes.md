## Inspecting sync_program.py

This script illustrates the idea of synchronous execution, mainly through the primary functions of `generate_data()` and `process_data()` in a producer / consumer pattern. We'll go over these in detail within the context of the lesson.

### Main

- Establish timestamp at start
- Declare an empty list 'data'
- Generate 20 units of data, append them to list 'data'
- Process 20 units of data, read from list 'data'
- Establish timestamp, output delta from start

```python
def main():
    t0 = datetime.datetime.now()
    print(colorama.Fore.WHITE + "App started.", flush=True)
    data = []
    generate_data(20, data)
    process_data(20, data)

    dt = datetime.datetime.now() - t0
    print(colorama.Fore.WHITE + "App exiting, total time: {:,.2f} sec.".format(dt.total_seconds()), flush=True)
```

### Generate data

- Given a number x and a list, generate x units of data and store them in the list
- A unit of data will be defined as a tuple containing an integer squared and timestamp of the operation
- Use time.sleep() to simulate waiting for some process (web request, db call etc)

pseudocode:
```
generate_data(input_a_number, and_a_list):
	for number in the range of 1 to (input_a_number + 1):
    	item = number * number
        append to list "data" a tuple containing item and current datetime
        
        print ack of the generated item, flush sys.stdout buffer for next call
        pause execution for half to one half second
```
Python
```python
def generate_data(num: int, data: list):
    for idx in range(1, num + 1):
        item = idx*idx
        data.append((item, datetime.datetime.now()))

        print(colorama.Fore.YELLOW + f" -- generated item {idx}", flush=True)
        time.sleep(random.random() + .5)
```

### Process data

- Given a number x and list containing generated data
- Iterate over list x times calculating delta between generation and processing of a data unit
- Use time.sleep() to simulate waiting for some process (web request, db call etc)
pseudocode:
```
process_data(input_a_number, and_a_list):
    counter = 0
    while counter is less than input_a_number:
        item = remove the tuple at index 0 from and_a_list and store it
        if item is equal to None
            pause execution of this function for .01 seconds
            return to the start of the while loop
    
    increment counter by 1
    value = item index 0 (squared number generated from the previous function)
    t = item index 1 (timestamp generated from previous function)
    dt = calculate time difference between now and when item data was generated
    
    print ack of data unit, include time delta of generation and processing, flush stdout buffer
    pause execution for a half second
```
Python
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
        dt = datetime.datetime.now() -t
        
        print(colorama.Fore.CYAN +
              " +++ Processed value {} after {:,.2f} sec".format(value, dt.total_seconds()), flush=True)
        time.sleep(.5)
```
### Output
```python
App started.
 -- generated item 1
 -- generated item 2
 -- generated item 3
 -- generated item 4
 -- generated item 5
 -- generated item 6
 -- generated item 7
 -- generated item 8
 -- generated item 9
 -- generated item 10
 -- generated item 11
 -- generated item 12
 -- generated item 13
 -- generated item 14
 -- generated item 15
 -- generated item 16
 -- generated item 17
 -- generated item 18
 -- generated item 19
 -- generated item 20
 +++ Processed value 1 after 18.69 sec.
 +++ Processed value 4 after 18.65 sec.
 +++ Processed value 9 after 18.16 sec.
 +++ Processed value 16 after 17.82 sec.
 +++ Processed value 25 after 17.19 sec.
 +++ Processed value 36 after 16.82 sec.
 +++ Processed value 49 after 16.44 sec.
 +++ Processed value 64 after 15.82 sec.
 +++ Processed value 81 after 15.71 sec.
 +++ Processed value 100 after 15.62 sec.
 +++ Processed value 121 after 15.06 sec.
 +++ Processed value 144 after 14.62 sec.
 +++ Processed value 169 after 14.49 sec.
 +++ Processed value 196 after 14.31 sec.
 +++ Processed value 225 after 14.10 sec.
 +++ Processed value 256 after 13.83 sec.
 +++ Processed value 289 after 13.12 sec.
 +++ Processed value 324 after 12.63 sec.
 +++ Processed value 361 after 11.70 sec.
 +++ Processed value 400 after 10.89 sec.
App exiting, total time: 28.75 sec.
```
## Notes

### Print() and the flush parameter

The print function prints *objects* to the text stream *file*, separated by *sep* and followed by *end*

The *file* argument must be an object with a write(string) method; if it is not present or None, `sys.stdout` will be used.

`stdout` is used for the output of print() and expression statements and for the prompts of input(); `stdout` is used to display output directly to the screen console

The stream `stdout` is line-buffered when it points to a terminal. Partial lines will not appear until flush(3) or exit(3) is called, or a newline is printed.

The flush argument of the print() function can be set to True to stop the function from buffering the output data and forcibly flush it. If the flush argument is set to True, the print() function will not buffer the data and partial lines will be printed

Flush does not change output, what changes is how the output is printed

- flush=False (default) will wait for the line to complete before printing it
- flush=True will force the terminal to print partial line
- flush does not matter if end=\n

Default: `end=\n` and `flush=False`. Partials are printed sequentially due to newline
```python
>>> for i in range(10):
...     print(i)
...     sleep(0.5)
... 
0
1
2
3
4
5
6
7
8
9
>>>
```
`end=","` and `flush=False`. Stream is line-buffered and output appears all at once
```python
>>> for i in range(10):
...     print(i, end=",")
...     sleep(0.5)
... 
0,1,2,3,4,5,6,7,8,9,>>> 
>>>
```
`end=","` and `flush=True`. Buffer is flushed after each call resulting in sequential output of partial lines
```python
>>> for i in range(10):
...     print(i, end=",", flush=True)
...     sleep(0.5)
... 
0,1,2,3,4,5,6,7,8,9,>>> 
>>> 
```
### String formatting

The format() method allows us to format strings

```python
>>> "The {0} goes to the {1}".format("dog", "park")
'The dog goes to the park'
```

`{0}` is replaced by the first argument of format() i.e. `dog` while `{1}` is replaced by the second argument `park`

Syntax `{[argument_index_or_keyword]:[width][.precision][type}`
```python
>>> "Floating point {:.2f}".format(38.754892)
'Floating point 38.75'
```

Here 2 digits of precision (max # of characters after decimal) are specified and `f` is used for a floating-point representation of the number

### List pop() method

list_name.pop(index)

Parameters:

index: The Python pop() function accepts only a single parameter which is the item’s index to be popped out of the list. It is an optional parameter.

The list pop in Python returns the popped value

```python
>>> fruits = ['apple', 'banana', 'cherry', 'grape', 'mango']
>>> for i in fruits:
...     processed = 0 
...     while processed < len(fruits):
...         item = fruits.pop(0)
...         print(colorama.Fore.MAGENTA + item)
...         time.sleep(.5)
... 
apple
banana
cherry
grape
mango
>>> fruits
[]
```