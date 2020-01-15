# Project 3

Web Programming with Python and JavaScript

Hi, this is an web application for handling a pizza restaurant’s online orders. Users will be able to browse the restaurant’s menu, add items to their cart, and submit their orders. Meanwhile, the restaurant owners will be able to add and update menu items, and view orders that have been placed.


A new user can register and then login to their account for ordering pizza, salad, pasta etc .
After login , the user can view all the items provided by the restaurant . The user can buy any item and before buying it will ask for the confirmation . Finally , a order number will be generated and an email will be sent to the user . The email will contain the ordered item and it's total cost .

Once the items are purchased , the cart will be cleared . If not purchased , then cart item will remain in cart even after logout or browser is closed or viewed from other machine .

## Files of project :
- project3
  - orders
   - static
     - orders
      - base.css    	- contains style for navigation bar
      - favicon.png 	- this image will be displayed in browser address bar
      - index.css   	- styles registration form and contains pizza image 
      - index.js 		- contains ajax code for checking availability of username as the user typing it
      - login.css 		- styles login form
      - menu.css 		- styles the product of pizza restaurant . When viewed in mobile phone , the cart will     	              shown  below the products 
      - menu.js 		- contains code for adding item to cart , removing it from cart . Cart items are saved           to database using ajax request . Calculates total cost cart items . This file contains major portion of code .
      - orderConfirmation.css 	- basic style for cart items 
      - pizza1.jpg  			- background image of pizza 

  - templates
    - orders
      - base.html           - This is the main template , which is inherited by other html files 
      - emailTemplate.html  - formats the purchased item for sending email to user 
      - index.html 			- contains registration form
      - login.html 			- contains login form
      - menu.html 			- all the items of restaurant are shown and cart is displayed 
      - orderConfirmation.html  - items will shown before buying it 
      - success.html 			- displays the order number  
  - models.py 				- contains total 6 models . The main model is Product . It contains a field name "parentProduct" , which is used to handle the case when a product is available in multiple sizes say small pizza, medium pizza, large pizza . And "ProductSize" and "Category" are also separate tables . Modelling in this way allows it to add more sizes or pizza category in future if required .

  - views.py 					- contains the code for user registration, login, logout, sending menu item, rendering order confirmation, buying , saving or removing cart item from database, sending email to user, checks username availability 
 - pizza
   - settings.py 			- contains setting for sending email to user
   - urls.py 				- contains route to different view function


## Personal Touch
- I chose to implement the functionality of sending email to user .
- I included the setting for gmail in settings.py file . Values are stored in environment variables 
- Once the order is confirmed , a email is sent to user showing their purchased item and total cost .
- The message is formated in html .

App screencast : https://youtu.be/JY6TB9d3TWU

Try it : https://pizzacs50w.herokuapp.com
