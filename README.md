# Sprint 4 Team 18
## Introduction

**Beer Game Project:** Software Engineering Project to create a supply chain game I,e, Beer Game. 

### The Beer Game Documentation

This project is built on Flask Python Framework and plain HTML/CSS.


## Software Requirements
Python 3.8.5

## Setup and Deployment:

Download the folder to your respective device. 
### Install project dependencies

```
pip3 install -r requirements.txt
```

Then,

```
python3 main.py 
```

To support the SQL database setup, mysql-python needs to be installed. The following tutorials can be followed:
https://stackoverflow.com/a/66033872
https://stackoverflow.com/a/5873259

Also, the credentials for the local MySQL installation must be set at the variable SQLALCHEMY_DATABASE_URI in the Config class in config.py and the database must already be created.

## For Tests:

1. To Run the tests, run
   ```
   pytest
   ```

## For Documentation:

1. Download the sphinx theme:
```
pip3 install sphinx_rtd_theme

```
2. To make the html documentation and then clean it:

```
cd docs
make html
make clean
```
3. The documentation will be then created under docs/\_build/html/index.html To run the Sphinx documentation in firefox:
```
firefox _build/html/index.html &
```

4. To recompile the Sphinx documentation:

```
cd docs
sphinx-apidoc --ext-autodoc -o . ..
```


Note that sphinx must be installed for this to work.


## Contributions: 

**XP Phase 1 (Shramish Kafle, Muhammad Dorrabb Khan)**
*Submission Date: March 9, 2020*

### Contributions in Front End :
 The application consists of the main introduction page with a navbar and a general banner displaying list of 3 different pages as: Instructor page, Student page, and General Game instructions page.

**Instructor page:** The instructor page consists of list of 3 different views for instructor as : <br/>
    • create account and login view ( This consists of a login page and if user is not registered, clicking on create account directs user to the register page.) <br>
    • game creation view ( This view consists a form that allows a user to create a game with respective information)<br>
    • Instructor dashboard (It displays the main instructor view which consists of tables showing all the relevant information of game. It also consists of several options that instructor can apply as update, reset games, etc.<br>

**Student page:** The student page redirects a user to a student/player login page which consists of a form for an email and password to be inputted.

**General Game Instructions Page:** This page displays the general game instructions for both the player and instructor.

*All the styling have been made using Bootstrap and CSS.*

*The folder is setup in Flask framework. All the respective HTML pages are found inside the template directory and CSS stylings are under CSS directory inside the static folder. The main.py file consists of route to the respective pages for the website.*


### Contributions in Back End : 

- The endpoints for creating instructors, players and games was created.
- Games are created only if the instructor is authenticated.
- Login pages for instructors and players are created with fairly basic authentication, enough to be demonstrated.
- Flask models for the classes created.
- Tests for all endpoints created using pytest.
- Documentation created using sphinx.


# se-02-team-18
Khurshid Ernazarov, Dongwook Lee

### Overall Progress
1. Resolved the bug with database table compilation at startup, so the project can start and work properly.
2. Reworked Front-end for all .html static files, so the project looks much prettier now.
3. Reworked navigation across the website - by eliminating redundant pages and refactoring the structure of the project: now dashboard pages for logged users are directly accessible from homepage.
4. Integrated sessions which allow to remember logged users. For example, as instructor you log in, then go to homepage, and want to return to dashboard - you don't have to log in repeatedly, you will be redirected to the dashboard right away. Also, the method to fetch user data was implemented via session variables, you may want to find a way to fetch everything you need via 1 object, e.g. more concisely.
5. Created the templates for tables in dashboard: they are easily manageable for future refactoring of the database.
6. Linked game creation page with dashboard.

### Recommendations for further steps
- As the templates are ready, we would recommend you to work on display of the Games data. For this you will need to adjust database (or templates) so that fields and data-values match each other and are displayed properly. First experiments in this direction can be found in file *example.html*.  After that you may think about the method to join the games as a Student.
- instructor_dashboard.html: deletion of games and function of updating the value of game information need to be implemented. The buttons on below page is not functional yet.
- student_dashboard.html: link to game page needs to be implemented. Searching engine is not functional yet.

# se-03-team-18
Aarshika Singh, Michael Demse

## Improvements made in Sprint 3:

## Frontend:

1. When an instructor logins then the instructor dashboard is diplayed. The instructor dashboard has the options to Create and Delete games. It also consists of several options that instructor can apply as update, reset games, etc.
2. When players login through the main page, then they are redirected student dashboard, where they can select a game through the link. The dashboard shows the name and email of the instructor of the game.
3. The players can use the filter on the student dashboard to filter the game according to the instructor email and name.
4. Once the player chooses a game usign the link, they are redirected to the chosen_role page: (It allows user to chose either factory, distibutor, wholesaler, retailer)
5. After chosing the role, players are directed to the Player Screen which consists of 4 screens as (Input Screen, Player Information, Status of other supply chain, and Inventory and Order Status).
6. After choosing the role, the player is redirected to the game screen.

## Backend:

1. The authentication was changed with inclusion of error handling and redirecting to a specific page if the entered credentials are missing or wrong.
2. The password is encoded for instructor login.
3. Delete game, reset a specific game, reset all games, edit a specific game functionalities were added to the instructor dashbaord.
4. A player an only choose roles and go to game screen, if authenticated.

## Tests

1. Previous tests were changed as they were completely failing.
2. Authentication was tested using Mock pytest
3. Page loading and redirections were tested using pytest and their respective status code.

## Documentation

1. The documentation has been re-created using Sphinx and the steps included at the top.

## How do I work on front-end?

The frontend templates is contained in the folder templates

## How to work on back-end?

All the views are present in main.py and all the models are on the file models.py

# se-04-team-18

Tsayem Daniela, Nitesh Khatiwada

## Instructions to run the server:

1. Clone repository with `git clone git@github.com:lorenzorota/se-04-team-18.git`
2. cd with `cd se-08-team-18/src`
3. Install python requirements with `make`. Your password will be asked.
4. Log into MySQL first with the root user (mysql -u root -p) and password and create a new user using the CLAMV credentials provided to you by the TA:

mysql> `CREATE USER 'seteam18'@'localhost' IDENTIFIED BY 'evlxey';`

mysql> `GRANT ALL PRIVILEGES ON * . * TO 'seteam18'@'localhost';`

5. Log into MySQL with mysql -u seteam18 -p and create a database with `create database BeerGame;`
6. Exit mysql. Type `make run` to run the server. 
It should be accessible at http://localhost:5000

## Improvements made:

1. Dramatically simplified installation process (wrote Makefile, using venv, updated config.py to use CLAMV credentials)
2. Fixed gameplay so it's now possible to create and play an entire game
3. Created all tables in the database
4. Fixed bugs with creation of tables and database by python script
