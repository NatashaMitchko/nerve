![alt text](https://github.com/NatashaMitchko/nerve/blob/master/readme_images/title.gif "Scavenger Hunt Logo Title")

# SCAVENGERHUNT
Scavenger Hunt is a game where users can accept challenges and complete them for points by uploading a photo of themselves completing the challenge. Scavenger Hunt uses computer vision to determine if the uploaded image constitutes a successful attempt and, if so, calculates the score based on how close the image is to the goal.

I built this app as my final project during my time as a software engineering fellow at [Hackbright academy](https://hackbrightacademy.com/). The program is a 12-week full-time engineering bootcamp that focuses on web-development in python. The main components are a PostgreSQL database, a server built using Flask as a framework, and the views that utilize Jinja templating.

### Check it out: [www.scavengerhunt-app.com](http://www.scavengerhunt-app.com) or at [http://54.202.149.231](http://54.202.149.231)

## Table of Contents

[Orginization](##Organization)
* [Model](###Model)
* [Server](###Server)
* [Views](###Views)

[Built With](##Built-With)

[Use My Code](##Use-My-Code)
* [Console Messages](###Console-Messages)
* [Floating Placeholder Form Styling](###Floating-Placeholder-Form-Styling)

[Things I'd Do Differently](##Things-I'd-Do-Differently)

[Author](##Author)

## Organization

There are three major components to this repository: the The data model resides in [model.py](model.py), the server is in [server.py](server.py) which imports functionality from [vision.py](vision.py). The HTML templates are all in the [templates](/templates) directory.

### Model
The data model implementation uses the [SQLAlchemy ORM](http://docs.sqlalchemy.org/en/latest/orm/). 

There are six tables in the data model, of which only 5 are utilized in the current version of the app. They are:

1. [User](####Users)
2. [User Challenge](####User-Challenges)
3. [Challenge](####Challenges)
4. [Challenge Category](####Challenge-Categories)
5. [Category](####Categories)
6. [User Challenge Categories](####User-Challenge-Categories)

#### Users
In addition to the primary key, each record in the users table contains three not nullable user supplied pieces of information: Username, Password and Email address. An optional piece of information (from the database's perspective) is a phone number. User passwords are hashed using [bcrypt](https://en.wikipedia.org/wiki/Bcrypt) which is why their datatype is VARCHAR(100).
```

  Column  |          Type          |                     Modifiers                      
----------+------------------------+----------------------------------------------------
 id       | integer                | not null default nextval('users_id_seq'::regclass)
 username | character varying(50)  | not null
 password | character varying(100) | not null
 email    | character varying(50)  | not null
 phone    | character varying(30)  | 
Indexes:
    "users_pkey" PRIMARY KEY, btree (id)
    "users_username_key" UNIQUE CONSTRAINT, btree (username)
Referenced by:
    TABLE "user_challenges" CONSTRAINT "user_challenges_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id)
```

#### User Challenges
The User Challenges table handles the many-to-many relationship between users and challenges. A user can have many challenges and a challenge can have many users. One important constraint on this table is that a user may not have the same challenge twice. This was implemented by imposing a unique constraint on a composite index. The syntax in Python-SQLAlchemy for this is: ```user_challenges_index = db.Index('unique_user_challenge_constraint', user_id, challenge_id, unique=True)```

Additional information about the status of a challenge that a user has accepted can be seen in the table description below:

```
       Column        |            Type             |                          Modifiers                           
---------------------+-----------------------------+--------------------------------------------------------------
 id                  | integer                     | not null default nextval('user_challenges_id_seq'::regclass)
 user_id             | integer                     | 
 challenge_id        | integer                     | 
 is_completed        | boolean                     | not null
 is_removed          | boolean                     | not null
 accepted_timestamp  | timestamp without time zone | not null
 completed_timestamp | timestamp without time zone | 
 image_path          | character varying(50)       | 
 points_earned       | integer                     | not null
 attempts            | integer                     | not null
Indexes:
    "user_challenges_pkey" PRIMARY KEY, btree (id)
    "unique_user_challenge_constraint" UNIQUE, btree (user_id, challenge_id)
Foreign-key constraints:
    "user_challenges_challenge_id_fkey" FOREIGN KEY (challenge_id) REFERENCES challenges(id)
    "user_challenges_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id)
Referenced by:
    TABLE "user_challenge_categories" CONSTRAINT "user_challenge_categories_user_challenge_id_fkey" FOREIGN KEY (user_challenge_id) REFERENCES user_challenges(id)
```

#### Challenges
The information about an individual challenge is stored here. Relationships exist between Challenges and Challeenge Categories, Challenges and User Challenges, and extend to Users and Categories through relationships.

```
   Column    |         Type          |                        Modifiers                        
-------------+-----------------------+---------------------------------------------------------
 id          | integer               | not null default nextval('challenges_id_seq'::regclass)
 title       | character varying(35) | not null
 description | text                  | not null
 difficulty  | integer               | not null
 image_path  | character varying(50) | 
Indexes:
    "challenges_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "challenge_categories" CONSTRAINT "challenge_categories_challenge_id_fkey" FOREIGN KEY (challenge_id) REFERENCES challenges(id)
    TABLE "user_challenges" CONSTRAINT "user_challenges_challenge_id_fkey" FOREIGN KEY (challenge_id) REFERENCES challenges(id)
```
#### Challenge Categories
Similarly to the User Challenges table, this table is an association table that simply maps categories to a particular challenge. This table only contains three fields: the autoincrementing primary key and the foreign keys to the Challenge and Category. There is also a composite index with a unique constraint to prevent the same category from being mapped to the same challenge twice.

#### Categories
For every challenge created there is an associated standard image that shows a sucessful challenge. The main functionality of this game is the comparison of the categories of the standard image to that of the user uploaded image. These categories are retrieved from a Google Cloud Vision API call. These calls take up to three seconds to complete so it's not feasible to make a call for the standard image *and* the user uploaded image each time a challenge is attempted. The Categories table essentially serves as a cache by storing all the results returned by the API call for a particular challenge.

This table contains two fields, an autoincrementing primary key and the category itself.

#### User Challenge Categories

This table is an association table that maps a user challenge to a set of categories. This table only get's updated when a user challenge is completed. Upon completion the categories that matched that caused the user to win get mapped to the user challenge record.

### Server

The server is built using [Flask](http://flask.pocoo.org/) as a framework. There are three types of functions in [server.py](server.py): app routes that render html templates, app routes that return jsonified data to the Javascript and helper functions. App route code blocks start with ```@app.route('/some-place')```.

### Views

There are seven HTML templats that extend from a base template. Templating is implemented using Jinja2. The Jinja in the templates handles content and what functionality is available to the user based on information in the session.

## Built With

* [PostgreSQL]()
* [Flask](http://flask.pocoo.org/)
* [Jinja2](http://jinja.pocoo.org/docs/2.9/)
* [JQuery](https://jquery.com/)
* [D3](https://d3js.org/)
* [chart.js](www.chartjs.org/)
* [Google Cloud Vision API](https://cloud.google.com/vision/)

## Use My Code
I built this project with lots of help from the internet, so if you'd like please use what I've done! Below are what I think are the three most reusable components from this code and how to use them in your own projects.

### Console Messages
If you open the console while using my application you will see this message:

![alt text](https://github.com/NatashaMitchko/nerve/blob/master/readme_images/console.gif "Console message")

Inspired by [Pinterest's](https://www.pinterest.com/) console.log message I decided to create one of my own. At the time of writing this I'm job searching so I decided to add a little extra information about myself that can be accessed by following the instructions in the message.

```javascript
 var style1 = [
    'color: #74e3ec',
    'line-height: 1.8;',
    'font-weight: bold;',
    'display: block'].join(';');
  var style2 = [
    'color: #07292c',
    'line-height: 1.8;',
    'font-weight: bold;',
    'display: block'].join(';');

  console.log('%c Hiring? %cGet in touch %c--> %ccontactMe() ', style1, style2, style1, style2);

  function contactMe(){
    window.open('/contact-me', '_blank'); 
    console.log('%c Talk to you soon!', style1);
  };
```
Variables style1 and style2 are CSS-like in that they define the look of the message displayed in the console. 

After the styles are defined there is a simple console.log statement. This is executed when the javascript on your webpage is executed. The styles are applied in this line. The ```%c``` that comes before the text ```Hiring?``` get's styled with style1, the text after the second ```%c``` get's styled with style2. The order of which style is applied where is defined in a comma-separated list after the string.

In the printed text itself I alert the user to a function: ```contactMe()```. This function opens a new tab and prints another message to the console. You need to specify the route you'd like to open and where to open it in your ```window.open```. You can see that I'm opening the route ```/contact-me``` and that I'm opening that route in a new tab (```'_blank'```). Now if the user closes that tab and returns to the app they will see in the console another message saying "Talk to you soon!". This is a cute easter egg that doesn't require a lot work to get set up.

### Floating Placeholder Form Styling

![alt text](https://github.com/NatashaMitchko/nerve/blob/master/readme_images/register.gif "Console message")

I got this form styling from [this codepen](https://codepen.io/anon/pen/zwbKGq) and adapted it to what I needed. This is HTML/CSS only - no javascript required. From the gif below you can see that there are four states that a field can be in:

Input | Label
--- | ---
 Not in focus, no text entered | Full size, grey 
 Not in focus, text entered| Hovering, grey 
 In focus, no text entered | Full size, highlight color
 In focus, text entered | Hovering, highlight color

 In order to make this happen I needed to write CSS selectors that could handle each of those states. Each label and input pair is wrapped in a fieldset tag that has the class "floating-placeholder". The two main selectors are:

```.floating-placeholder input:valid~label```
and 
```.floating-placeholder input:focus+label```

The first handles the styling of the label when there is input in the input field. The second styles the label when the input is in focus. The plus sign is the [adjacent sibling selector](https://developer.mozilla.org/en-US/docs/Web/CSS/Adjacent_sibling_selectors) in CSS - this means that in the HTML the label element needs to come directly after the input element.

You can see another version of this [here](https://codepen.io/NatashaMitchko/pen/BZNPgq/) that I wrote to include radio button and file upload styling.

## Things I'd Do Differently
This is the first web application that I've ever built and in the process I learned a ton. Although I love this app and am very proud of it, I'm probably not going to make any more dramatic changes to it. There are, however, a lot of things that I'd do differently if I had to start over knowing what I know now. Here's a loosely organized list of features I wish I had implemented, things I'd change about the structure of my code and miscelaneous thoughts:

* Un-nest my CSS
    * Currently my CSS uses nested selectors, some that are nested 4 deep, while my front-end looks nice as-is this code isn't maintainable
* Use the information in the User Challenge Categories table
    * When a user completes a challenge I store the categories they won on. This information should be displayed somewhere for the user
* Not nearly enough user feedback
* Make it mobile-friendlier
    * This app is about taking photos - nowhere here do I attempt to interface with a phone's camera
* Host the images somewhere
    * I'm currently just saving the images to the images folder in the static directory of this project - not good!
* Loading bar - MOAR FEEDBACK FOR THE USER
    * The API calls in this app take forever, a loading bar would make this user experience a little better
* Send feedback & Report a problem

## Author

#### Hi, I'm Natasha

I graduated with a degree in chemistry from NYU and am a New York native. After graduating I worked at Google for two years as a technical specialist for Google's emerging local ad products. After realizing I was passionate about the technical side of that role I decided to up-skill my computer science knowledge and pursue a career in software engineering. I recently completed a fellowship program at Hackbright Academy in San Francisco where I learning the hard skills to become a backend/ full-stack developer. In my free time, I enjoy 3D modeling in Maya and Unity as well as reading about current trends in chemistry and physics.
