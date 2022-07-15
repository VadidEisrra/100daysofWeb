# DOM

Taken from [MDN](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction):  

>A web page is a document that can be either displayed in the browser window or as the HTML source. In both cases, it is the same document but the Document Object Model (DOM) representation allows it to be manipulated. As an object-oriented representation of the web page, it can be modified with a scripting language such as JavaScript.

>The DOM is not part of the JavaScript language, but is instead a Web API used to build websites. JavaScript can also be used in other contexts. For example, Node.js runs JavaScript programs on a computer, but provides a different set of APIs, and the DOM API is not a core part of the Node.js runtime. 

>The DOM is not a programming language, but without it, the JavaScript language wouldn't have any model or notion of web pages, HTML documents, SVG documents, and their component parts. They can all be accessed and manipulated using the DOM and a scripting language like JavaScript.

The following `index.html` displays some DOM interaction using JavaScript
```html
<!DOCTYPE html>
<head>
  <meta charset="utf-8" />
  <title>My top 10 quotes on living life better | Virgin</title>
</head>
</body>
  <div class="content">

    <p>Here are my top 10 quotes on living life better for some New Year inspiration:</p>

    <ul id="quotes">
      <li>10. "The beautiful thing about learning is nobody can take it away from you." - B.B King</li>
      <li>9. "Inexperience is an asset. Embrace it." - Wendy Kopp</li>
      <li>8. "Change will not come if we wait for some other person, or if we wait for some other time. We are the ones we’ve been waiting for. We are the change that we seek." - Barack Obama</li>
      <li>7. "The sky is not my limit… I am." - T.F. Hodge</li>
      <li>6. "Life is either a daring adventure or nothing at all." - Helen Keller</li>
      <li>5. "It does not matter how slowly you go as long as you do not stop." - Confucius</li>
      <li>4. "Too many of us are not living our dreams because we are living our fears." - Les Brown</li>
      <li class="churchill">3. "Continuous efforts – not strength or intelligence – is the key to unlocking our potential." - Winston Churchill</li>
      <li>2. "Believe you can and you’re halfway there." - Theodore Roosevelt</li>
      <li>1. "Success means doing the best we can with what we have. Success is the doing, not the getting, in the trying, not the triumph. Success is a personal standard, reaching for the highest that is in us, becoming all that we can be." - Zig Ziglar</li>
    </ul>

    <p id="more">-</p>
  </div>

  <script type="text/javascript">
  
  // 1a. get p tag with id "more" and overwrite inner HTML
  alert(document.getElementById("more").innerHTML = "How do you try to live a happier, healthier life?")
  

  // 1b. get all p tags
  let paragraphs = document.getElementsByTagName("p")
  console.log(paragraphs)

  // ... and get all li tags
  let quotes = document.getElementsByTagName("li")
  console.log(quotes.length)
  console.log(quotes[0].innerHTML)

  // 1c. get a tag by class name
  console.log(document.getElementsByClassName("churchill")[0].innerHTML)
   
  // 2. write the quotes back in order
  quotes = Array.from(quotes).reverse()
  let quoteUl = document.getElementById('quotes')

  for(let quote of quotes){
    quoteUl.appendChild(quote)
  }
    
  // 3. add a new quote
  let newQuote = document.createTextNode('11. "Fortunately, JS has some good parts."')

  let newLi = document.createElement("li")
  newLi.appendChild(newQuote)
  quoteUl.appendChild(newLi)
 
  // 4. rm last quote
  quoteUl.removeChild(newLi)

  // 5. color the even quotes
  for(let i=0; i < quotes.length; i++){
    if(i % 2 === 0){
      quotes[i].style.color = "red"
    } else {
      quotes[i].style.color = "blue"
    }
  }

  // 6. add behavior / event listener
  for(let i=0; i < quotes.length; i++){
    quotes[i].addEventListener("click", function(event){
      let targetElement = event.target || event.srcElement
      let tweetUrl = 'https://twitter.com/intent/tweet?text='+encodeURI(targetElement.innerHTML)
      window.open(tweetUrl, '_blank')
    })
  }
  document.getElementById("more").innerHTML += "Click on the quotes to share them on twitter!"

  </script>
</body>
</html>
```