# cs50-2020-project4 NETWORK

### Author/Date

      Juan Gabriel MEJÍA / 2020-07-30

## INTRODUCTION
### Description
A Twitter-like social network website for making posts and following users.

### Technologies
Python, JavaScript, HTML, and CSS.

## PROJECT DETAILS
### General requirements implemented
* New Post
* All Posts
* Profile Page
* Following
* Pagination
* Edit Post
* “Like” and “Unlike”

### Spetial requirements implemented
* Show number of follwers in profile page.
* Show Thumb Up Icon in a different color when a post has been given a like by the current user.
* ! Althought the display pages ware not implemented, the app is capable of (because of its models design):
	* List the users who have given a like to a post.
	* List the users who follows the current user. 

### Project files and directories
* network/:    The aplication directory (Application name: Network)
	* migrations/:   migrations files * .py
	* static/
		* network/:  Static files for the Network application
			* favicon.ico: small icon associated with the website
			* main.js:  Javascript code for Edit and Like implementations using js Fetch requests to Django views.
			* styles.css:  Style sheet
	* templates/
		* network/:  the templates for the Network application
			* error.html: general error template.
			* following.html:  lists of posts of all users followed by current user- Inherits from listsposts.html.
			* index.html:  lists of posts of all registered users- Inherits from listsposts.html.
			* listpost.html: template for listing any list of posts (all or following), from which following and index inherit.
			* layout.html: root template from which every other template inherits.
			* profile.html: Current user informaction, post from users followed by current user, and users followed by current user-
			* login.html: login page
			* register.html: new user registraton form.
	* templatetags/: Template tags used in django templates.
			* range.py: generate a range from < start > to < end > for iterating through a for loop.
	* admin.py: For registering models to be accessed from /admin 
	* apps.py: registered apps for the current project
	* models.py: app models- Only 2: Post and User (abstract).
		* User likes is a ManyToMany relationship with Post - A user likes posts, and a post is liked by users.
		* User follows is a ManyToMany non symmetrical relationship with User itself - A user follows and is followed.
		* Post Author is a One to Many relationship with User
	* test.py: dummy file for tests
	* urls.py: html app routes
	* views.py: app controllers responding to routes 
* project4/   The project directory	
	* asgi.py: ASGI config for project4 project.
	* setting.py: project setting file (Django settings).
	* urls.py: html project routes
	* wsgi.py: WSGI config for project4 project.
* db.sqlite3: The databse file. 
* manage.py:  Django's command-line utility for administrative tasks
* README.md: This file. 

## RUNNING APP in Ubuntu
### Create an Enviroment 

 Before running a project, an Environment must be set for Python 3 and requirements.txt must be then installed
 For example to create an environment called: /env-py3.9
 
 First create directory:
 	mkdir env-py3.9

 Then set environment:
 	python3 -m venv env-py3.9

Finally, activate envirinment:
	source env-py3.9/bin/activate

Now is time time install Python packages - If requirements.txt is present:
	pip install requests

	I have created an environment called: /env-py3.9

### Prepare environment
	> source active.sh

	# Where active.sh is a file with 2 lines:
	source env-py3.9/bin/activate
	cd env-py3.9/pr*1*/pr*1