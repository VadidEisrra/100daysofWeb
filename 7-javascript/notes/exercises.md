# exercises

### control flow
```html
<!DOCTYPE html>
<html>
<head>
  <title>Can you guess the number?</title>
</head>
<body>
  <script type="text/javascript">
  /* write a simple number guessing game:
     - use 'prompt' to ask for a number, covert it to int (parseInt)
     - if guess === null or 'q', exit (user escapes / cancels)
     - if not a number continue
     - if number == secretNumber, print 'You guessed it!' (use console.log)
     - if number < secretNumber, print 'Too low'
     - if number > secretNumber, print 'Too high'
     - bonus: count the number of attempts, and exit upon the 5th guess
  */
    
    function getRandomInt(min, max) {
      min = Math.ceil(min)
      max = Math.floor(max)
      return Math.floor(Math.random() * (max - min +1)) + min
    }
    
    const secretNumber = getRandomInt(1, 15)
    
    // I code
    
    let i = 0
    
    while(i < 10) {
      let guessLeft = 9 - i
      let guess = prompt('Guess the number')
      if(guess === null || guess == 'q'){
        break
      } else if(isNaN(guess)){
        alert('not a number')
        continue
      } else if(guess == secretNumber){
        alert('You guessed it, ' + secretNumber + '!')
        break
      } else if(guess > secretNumber){
        alert('Too high! Guesses left: ' + guessLeft)
        i++
        continue
      } else if(guess < secretNumber){
        alert('Too low! Guesses left: ' + guessLeft)
        i++
        continue
      }
    }
  </script>
</body>
</html>
```

### functions
```html
<!DOCTYPE html>
<html>
<head>
  <title>JS is Fun!</title>
</head>
<body>
  <script type="text/javascript">
  /* write a function to sum numbers, if no argument is provided
    default summing a range of 1..100 - write a second function
    called range to return that range of integers */

  function sum(numbers){
    // you code
    if (numbers == undefined) numbers = range(1, 100)
    let result = 0
    for (let i=0; i < numbers.length; i++){
      result += numbers[i]
    }
    return result
  }

  function range(min, max){
    let result = []
    for (let i=0; i < 4; i++){
      let newNum = getRandomInt(min, max)
      result.push(newNum)
    }
    console.log(result)
    return result
  }
    
  function getRandomInt(min, max){
    min = Math.ceil(min)
    max = Math.floor(max)
    return Math.floor(Math.random() * (max - min +1)) + min
  }
    

  // test code
  // with argument
  let ages = [11, 18, 25, 17, 33];
  console.log(sum(ages)); // 104


  // without argument
  console.log(sum()); // 5050 default
  </script>
</body>
</html>
```
### looping

```html
<!DOCTYPE html>
<html>
<head>
  <title>Who can drive?</title>
</head>
<body>
  <script type="text/javascript">
  /* write a small program to loop over a list of names and ages,
     printing if each person is allowed to drive based on minAge,
     output should look like:
     tim (14) is not allowed to drive
     sara (33) is allowed to drive
     mike (17) is not allowed to drive
     julian (18) is allowed to drive
     eva (25) is allowed to drive
     amy (7) is not allowed to drive    
  */

  let minAge = 18;

  // names and ages are equal length lists (we will make objects (dicts) soon)
  let names = ["tim", "sara", "mike", "julian", "eva", "amy"];
  let ages = [14, 33, 17, 18, 25, 7];

  // you code
  function mergeArrays(names, ages){
    data = {}
    for(let i =0; i < names.length; i++){
      data[names[i]] = ages[i]
    }
    return data
  }
    
  drivers = mergeArrays(names, ages)

  for(i in drivers){
    let age = drivers[i]
    if(age >= minAge){
      console.log(`${i} (${age}) is allowed to drive`)
    } else {
      console.log(`${i} (${age}) is not allowed to drive`)
    }
  }

  </script>
</body>
</html>
```
### objects

```html
<!DOCTYPE html>
<html>
<head>
  <title>JS is Fun!</title>
</head>
<body>
  <script type="text/javascript">
  /* 
  Create an array (list) of food objects where each food has name:
  kcal (calories) key, value pairs
  Voilà you just wrote your first JSON object (try it: https://jsonlint.com/) :)
  Loop through this array, printing the foods out to the console like so:
  {Egg McMuffin [4.8 oz / 136 g]: "300"}
  {Egg White Delight [4.8 oz / 135 g]: "250"}
  {Sausage McMuffin [3.9 oz / 111 g]: "370"}
  */

  // you code
  
  let foodDb = [
    {'Tacos [4.8 oz / 136 g]': '300'},
    {'Burritos [6.2 / 225 g]': '415'}, 
    {'Guac [2.5oz / 63 g]': '135'} 
  ]
  
  for(let food of foodDb){
    console.log(food)
  }
    
  </script>
</body>
</html>
```