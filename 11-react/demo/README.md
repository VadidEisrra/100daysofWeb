# React

React is a JS library for building user interfaces. The intention is to make working with the DOM easier on the frontend.

### Demo

For the demo app - we'll be interacting with the Pybite Tips API. With node installed on our system, we can bootstrap a react application called tips using `npx create-react-app tips` in our demo folder. For the difference between NPM and NPX check out [this](https://stackoverflow.com/questions/50605219/difference-between-npx-and-npm) stackoverflow post. 

###### tldr; NPM is used to install packages, NPX is used to execute them with an advantage - NPX can execute a packages that are not installed.

- `tips/package.json` is similar to requirements file in python  
- `tips/src` contains css and js files for project  
- `tips/public` index.html lives here

Install two other dependencies for the project - `Axios` and `react-highlight-words`

- `npm install axios`
- `npm install react-highlight-words`

Watch video 4/18 to get site page setup  
Watch video 5/18 to setup DRF tips API back-end, to start it:

- `cd tips/code/python_tips;source venv/bin/activate;python manage.py runserver`
- `curl 127.0.0.1:8000/api/10` to test

