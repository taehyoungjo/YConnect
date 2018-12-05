# Yale Connect Design
Contained in this document is the design rational behind the largest elements of our code. These include creating and updating profiles, making connections, searching, database organization, and the implementation of profile pictures.

## Update Profile
# Yale Connect Design
Contained in this document is the design rational behind the largest elements of our code. These include creating and updating profiles, making connections, searching, database organization, and the implementation of profile pictures.

## Update Profile
Update profile uses a substantial amount of javascript in order to dynamically display html for both the search and selected classes display functions. This is done through using 4 functions:
	* `search();`
	* `startup();`
	* `addclass();`
	* `remove_class()`

The first function,  `search();` , is used to query the classes table within the database and find classes that match the inputted text. The second, `startup();` is run when the page loads and also after a class is removed and the class list has to update itself. The third, `addclass();`, is where classes are added through and the final `remove_class();` deletes the record of registration from the table class_registration. It appears that much of the code between 3 of these functions are very similar, however, because it is generating html there are slight changes between each of the functions that have to be separated out. Therefore, it is not possible to abstract most of these elements of the code into another function that could be shared across the higher level functions in a way that would make sense.

## Connections
!!!JK!!!

## Search
!!!TAE!!!

## Databases
Our project is structured using one database with 6 separate tables contained within.  Including:
	* users
	* profile
	* majors
	* connections
	* classes
	* class_registration

### Users
This table is used to track the usernames and hashed passwords of each of the users that use the website. This database is populated through the /register route in app.py. After checking if the form is populated with the proper information the database is then queried with an INSERT command. If  `if not result`  returns as true the code returns an error because the user name is already in use within the code. After inserting the user into the table username is then in  `session[“user_id”]` for use throughout the rest of the program.

### Profile
This table stores most of the information that is associated with each user’s profile. This includes the `id` which is critical to many of the other operations on our website. Other information is used to fill out the profile page. Finally, this table stores `file_path` which is how profile pictures are stored within our project. Photos are addressed further later in this document.

### Majors
We decided to use a table instead of hardcoding the majors into the html using an option menu because of the amount of majors that Yale offers. This table is also created in order to simplify the process to add and change the majors that are offered at Yale. Through using a database majors can be updated much more through the code than updating the html.

### Connections
!!!JK!!!


### Classes
This database stores the class id (ex. ECON110) and class name (ex. An Introduction to Microeconomic Analysis) for offered classes. As a design decision we only included a limited list of classes. If we pursued this project further, we would seek to use the same API that course table uses in order to pull the names and other information of the thousands of classes that are taught at Yale. By using classes as a database we are able to use db.execute() to search through and use the data that is contained within. This is substantially easier than using hard-coded html class names.

### class_registration
Class registration is implemented in a similar manner to how stocks were traded in the finance PSet. This is because we implemented class registration in a transactional manner. Classes are added and removed from the table and are tracked through the a user_id that is attached to the table. This decision means that all class registration can be kept in the same place and easily queried and used in javascript to dynamically add html to the page.

## Photos
!!!TAE!!!







## Connections
!!!JK!!!

## Search
!!!TAE!!!

## Databases
Our project is structured using one database with 6 separate tables contained within.  Including:
	* users
	* profile
	* majors
	* connections
	* classes
	* class_registration

### Users
This table is used to track the usernames and hashed passwords of each of the users that use the website. This database is populated through the /register route in app.py. After checking if the form is populated with the proper information the database is then queried with an INSERT command. If  `if not result`  returns as true the code returns an error because the user name is already in use within the code. After inserting the user into the table username is then in  `session[“user_id”]` for use throughout the rest of the program.

### Profile
This table stores most of the information that is associated with each user’s profile. This includes the `id` which is critical to many of the other operations on our website. Other information is used to fill out the profile page. Finally, this table stores `file_path` which is how profile pictures are stored within our project. Photos are addressed further later in this document.

### Majors
We decided to use a table instead of hardcoding the majors into the html using an option menu because of the amount of majors that Yale offers. This table is also created in order to simplify the process to add and change the majors that are offered at Yale. Through using a database majors can be updated much more through the code than updating the html.

### Connections
!!!JK!!!


### Classes
This database stores the class id (ex. ECON110) and class name (ex. An Introduction to Microeconomic Analysis) for offered classes. As a design decision we only included a limited list of classes. If we pursued this project further, we would seek to use the same API that course table uses in order to pull the names and other information of the thousands of classes that are taught at Yale. By using classes as a database we are able to use db.execute() to search through and use the data that is contained within. This is substantially easier than using hard-coded html class names.

### class_registration
Class registration is implemented in a similar manner to how stocks were traded in the finance PSet. This is because we implemented class registration in a transactional manner. Classes are added and removed from the table and are tracked through the a user_id that is attached to the table. This decision means that all class registration can be kept in the same place and easily queried and used in javascript to dynamically add html to the page.

## Photos
!!!TAE!!!


