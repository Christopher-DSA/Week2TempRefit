#Refit Database

##Introduction
Introduction:


This database facilitates the storage and organization of critical data. It acts as a repository for user accounts, content, transactions, and various other essential components of your web application. The database empowers your application to handle high volumes of data and concurrent user interactions.

This documentation aims to help you gain insights into the database's structure, schemas, and relationships, enabling you to effectively navigate and understand its underlying data model. You will discover how to interact with the database through querying and data manipulation techniques, ensuring that your web application can seamlessly retrieve and update information as needed.



##Tables

###User:
The user table stores email and password information of a user. It also stores their role and when they were added. 

###User_detail:
This table stores all the personal information of the user. The information include first name, last name, birth date, gender, addresses, province, city, postal code, and telephone. 
This table is directly linked to user table using foreign key user_id

###USER LOGGING
This table stores the login information of a user each time they login to the application. It stores the user_id, login date, ip address, and the gps location. 

###Refit admin
This table store information about the admins. It stores the name, user_id, 2fa code, and the admin level. 

###Organizations
This table stores information about the users whose role is organization. This table stores their name, user_id, logo, status, 2fa code, and subscription id.

###Store
This table stores the information of branches of an organization. It stores the name, its branch, and address. This table connects to the organization table using the foreign key organization_id, and to the user table using the foreign key user_id

###Store_locations
This table store location of each store using their GPS coordinate. The 


##ERD Diagram

