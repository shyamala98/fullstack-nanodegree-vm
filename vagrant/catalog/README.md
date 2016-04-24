Project 3: Catalog Project - [Shyamala Prakash]
========================
This application provides a web interface to a list of categories, each category is associated with a list of items.
Users who access the application can browse the categories and items without having to login.
Users can login using either their google or facebook accounts. 
 (The code for the authentication using google and facebook sign in was taken from the sample code used in the lectures)
Once a user is logged into the application, he/she can do the following:
- Add a new Category.
- Add a new Item to a Category.
- Edit a category he/she has created.
- Edit items he/she has created. 
- Delete items he/she has created.


Required Libraries
------------------
The application uses a Postgres database to store the data for the application.
Requires Python v2.*
Requires sqlalchemy module
The applications is built using the python flask framework 
The OAuth2.0 module is used for the authentication components.

How to run this Project
-----------------------
Clone this project from Git to your local machine
This application was deployed and tested on the Vargrant VM. This VM has Postgres installed and configured as well as psql command line interface.
To use the VM:
Navigate to the full-stack-nanodegree-vm/catalog directory
The command vagrant up will start up the virtual machine.
execute vagrant ssh to login to the VM
cd /vagrant to change to the synced folders 
The files for the catalog project will be available in this directory.

1. Run the sql script catalog.sql to create the database for the catalog application. 
\i catalog.sql
This will create a database called catalogdb in postgres.

2. Run the python script database_setup.py to create the tables ct_catalog, ct_items and ct_user in catalogdb
python database_setup.py

3. Run the python script project.py to launch the application
python project.py

To URL to access the application in your browser is: http://localhost:5000/catalog





