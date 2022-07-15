# JavaScript Introduction

### How to run JS

JavaScript can be run in the JS console from web browser Developer Tools, or jsbin.com

Alternatively, install Node.js; a back-end runtime that can execute JS outside of the browser

- type `node` into terminal to activate REPL
- execute JS file `node hello.js`

### Print to console, variables and `let`

```javascript
> // print to console
> console.log('hello world');
hello world

> // use var to define a variable
> var name = 'bob';

> // best practice is to use 'let'
> let first_name = 'bob';

> // let variables cannot be redefined
> let first_name = 'richard'
Uncaught SyntaxError: Identifier 'first_name' has already been declared

> // define a constant
> const minAge = 18;
> 
> // constants cannot be assigned other values
> minAge = 23
Uncaught TypeError: Assignment to constant variable.

> // variables are global or local to a function
> if (true) {
    var x = 5;
    }
> console.log(x)
5

> // let allows you to declare variables that are limited to block, statement or expression on which it is used
> if (true) {
    let y = 5;
    }
> console.log(y);
Uncaught ReferenceError: y is not defined
```

## Data types

In JavaScript, a primitive (primitive value, primitive data type) is data that is not an object and has no methods or properties. There are 7 primitive data types: string, number, bigint, boolean, undefined, symbol, and null. All primitives are immutable.

JavaScript is a dynamically typed language - types are not defined at declaration of a var. The JavaScript engine allocates memory for variables on two memory locations: stack and heap.

### stack
- static memory allocation
- primitive values and references
- Size is known at compile time
- Allocates fixed amount of memory
### heap
- Dynamic memory allocation
- Size is known at run time
- No limit per object
### Primitives
- String
- Number
- Boolean
- Undefined
- Null
Primitive variables are stored in the stack, creating a copy of a variable creates a new instance with a copy of the value
```javascript
// new primitive var 'name' in stack
var name = 'Max';
console.log(name);

// copy value of 'name' to new var 'secondName' in stack
var secondName = name;
console.log(secondName);

// check if changing value of name will also change secondName
name = 'Chris';

// secondName is not changed because it's a different place in memory
console.log(secondName);
```
### Reference
- objects
- functions
```javascript
// first pointer on stack to object person
var person = {
  age: 38,
  name: 'Max',
  hobbies: ['Sports', 'Cooking']
};
console.log(person)

// manual copy of 'person' reference
var thirdPerson = {
  age: 28,
  name:'Max',
  hobbies: ['Sports','Cooking']
}

// second pointer on stack to object person
var secondPerson = person;
console.log(secondPerson);

// change name on any - all vars pointing to object change
person.name = 'Chris';
console.log(secondPerson)

// different place in memory; name remains Max
console.log(thirdPerson)
```
All variables first point to the stack. In case it's a non-primitive value, the stack contains a reference object in the heap
variables in the stack store addresses to objects in the heap
### Copy object data (sort of but not really)
The `Object.assign()` method can copy a reference object... but it is not truly a clone of the data
```javascript
// second pointer on stack to object person
var secondPerson = Object.assign({}, person);
console.log(secondPerson);

// secondPerson also gets hobbies - points to original
person.name = 'Chris';
person.hobbies.push('Reading');
console.log(secondPerson)

// different place in memory; name remains Max
console.log(thirdPerson)
```
### Actual copy (of some data)
Slice method can copy portions of an array, without any parameters it takes the entire thing
```javascript
// prints ["Sports", "Cooking", "Reading"]
var myHobbies = person.hobbies.slice();
console.log(myHobbies)
```

## Arrays

```javascript
// define array
> names = ['Julian', 'Bob']
[ 'Julian', 'Bob' ]

// copy names values to new var newNames
> newNames = names.slice()
[ 'Julian', 'Bob' ]

// select element from array
> names[0]
'Julian'

// slice
> names.slice(1,3)
[ 'Bob' ]

// reverse
> names.reverse()
[ 'Bob', 'Julian' ]

// sort
> names.sort()
[ 'Bob', 'Julian' ]

// get last element
> names.pop()
'Julian'

// add item
> > names.push('sara')
2
> names
[ 'Bob', 'sara' ]
> names.length

// for loop
> for (let i=0; i<names.length; i++){
    console.log(names[i])
    };
Bob
sara

// condensed for loop
> for (let name of names){
    console.log(name)
    };
Bob
sara
```
## Conditionals

```javascript
> const minAge = 18
> let myAge = 17;

// check if myAge greater than or equal to minAge
> if(myAge >= minAge){
    console.log('can drive');
    }

// add else statement
> if(myAge >= minAge){
    console.log('can drive');
    } else {
    console.log('cannot drive');
    }
cannot drive

// condensed
> (myAge >= minAge)? 'can drive' : 'cannot drive'
'cannot drive'

> names = ['bob', 'julian', 'mike', 'berta', 'quinton', 'tim', 'oliver']
[
  'bob',     'julian',
  'mike',    'berta',
  'quinton', 'tim',
  'oliver'
]

// ternary way
> for(let name of names){
    console.log(name);
    }
bob
julian
mike
berta
quinton
tim
oliver

// log names that start with 'b'
> for(let name of names){
    if (name.startsWith('b')){
      console.log(name);
      }
    }
bob
berta

// if name starts with 'b' continue loop
// if names starts with 'q' break look
> for(let name of names){
    if(name.startsWith('b')){
      continue;
      } else if (name.startsWith('q')){
      break;
      }
    console.log(name)
    }
julian
mike

> names
[
  'bob',     'julian',
  'mike',    'berta',
  'quinton', 'tim',
  'oliver'
]
```

 ## Functions

```java
// declare simple function
> function hello(name){
    console.log('Hello ' + name);
    }

// call function and pass name
> hello('Mike')
Hello Mike

// calling function with no parameters
> hello()
Hello undefined

// declare function to convert farenheit to celsius
> function toCelsius(farenheit){
    return (5/9) * (farenheit - 32);
    }

> toCelsius(100)
37.77777777777778

// print argument passed to function
> function print_arguments(){
    for(let arg of arguments){
      console.log(arg);
      }
    }

> print_arguments()
undefined
> print_arguments(1, 2, 3, 'a')
1
2
3
a

// default argument 'stranger'
> function hello(name){
    if (name == undefined) name = 'stranger';
    console.log('Hello ' + name);
    }

> hello()
Hello stranger

> hello('julian')
Hello julian

// another way to declare default arg similiar to python
> function hello(name='stranger'){
    console.log(`Hello ${name}`);
    }

> hello()
Hello stranger

> hello('mike')
Hello mike

// arrow functions - new in ES6
> hello = (name='stranger') => {return 'hello ' + name}

> hello('bob')
'hello bob'
```

## Objects

```javascript
// almost 'everything' is an object
> let person = 'bob'
> person.length
3
> person.toUpperCase()
'BOB'
> person.endsWith('b')
true

// object literal aka dictionary
> let bite = {number: 1, title: 'Sum of numbers', points: 2}
> bite.number
1
> bite["title"]
'Sum of numbers'
> bite.points
2

// using anonymous function to add a method
> bite.repr = function(){
    console.log(`Bite ${this.number} - ${this.title}
                (${this.points} points)`);
    }

> bite.repr()
Bite 1 - Sum of numbers (2 points)

// inspecting objects
> console.log(bite)
{
  number: 1,
  title: 'Sum of numbers',
  points: 2,
  repr: [Function (anonymous)]
}

> JSON.stringify(bite)
'{"number":1,"title":"Sum of numbers","points":2}'
```

## Debugging
You may debug in the browser. For instance - from chrome open dev tools (right click > inspect). Instead of console, select `sources`. Here you may access the source file of the page and set breakpoints. Then refresh the page and open the console drawer to access the program at the breakpoint. 

Fun online IDE's

- [JS Bin](https://jsbin.com/?html,output)  
- [JSitor](https://jsitor.com/)


## Common gotchas

- Global variables make code less isolated and your program less reliable. Example: omit the var keyword and a variable is created in the global scope. Use let and const

- End of line semicolons are optional and misuse is "passed silently" masking errors. Use semicolons!

- Two equality operators: == (value equality) vs === (value + type equality)

- Two ways to express undefined or empty variables: null and undefined

## Further study

- [JavaScript in 15 minutes](https://jgthms.com/javascript-in-14-minutes/)
- [W3 Schools JS](https://www.w3schools.com/js/)  
- [MDN Learn JavaScript](https://developer.mozilla.org/en-US/docs/Learn/JavaScript) - These are great, go through guides then use reference
- [The Birth and Death of JavaScript](https://www.destroyallsoftware.com/talks/the-birth-and-death-of-javascript)
- [Execute program - Modern JS](https://www.executeprogram.com/courses/modern-javascript)
- Books: You Don't Know JavaScript, JavaScript: The Good Parts, Eloquent JavaScript
- Specializations: 
1. Server-side: Node, TypeScript
2. Frameworks: jQuery, Angular, React, Vue.js

Checking browser support for JS features [CanIUse](https://caniuse.com/)