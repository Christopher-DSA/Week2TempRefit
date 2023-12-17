***SRS 2.2.8***

# 2.2.8 Add new equipment
Use case name:  | Add New Equipment
----------------|--------------------------------
Scenario:       | Adding tag to New Equipment
----------------|--------------------------------
Triggering event: | New equipment is delivered and needs to be tagged.
----------------|--------------------------------
Brief description:| When a new equipment is delivered technicians needs to add tag to them. 
----------------|--------------------------------
Actors:         | Technicians
----------------|--------------------------------
Related use cases: |
----------------|--------------------------------
Stakeholders:   | Technicians, Contractor, client, government
----------------|--------------------------------
Preconditions:  |
                |Technicians must be logged in successfully in refit App
                |Technician should have access to Technician Dashboard
----------------|--------------------------------
Postconditions: |The tag should be linked with the Equipment.
----------------|--------------------------------
Flow of activities: | 
----------------|--------------------------------
   *ACTOR*      |  *SYSTEM* 
----------------|--------------------------------
1. Technician enters username and password and logins successfully. | User is signed in Successfully and displays technician Dashboard.
----------------------------------------------------------------|----------------------------------------------------------------
2. User clicks on Scan QR Tags button in Technician Dashboard.  | Only for first use , it asks permission to access phone’s camera and modal is appeared with Deny and Accept as options.
                                                                | User needs to Accept it in order to start scanning. If accepted it will not ask again for permission.
                                                                |If Deny button is clicked, it takes back customer to Technician Dashboard page.
----------------------------------------------------------------|----------------------------------------------------------------
3. User scan the equipment tag successfully.                    | 3.1 New Equipment form is displayed
----------------------------------------------------------------|------------------------------------------------------------
4. Fill all the required details correctly in New Equipment screen-1 and then click Next then again fill all details in Equipment Screen -page 2 and then click Submit |
                                                                                | 4.1 Equipment Tag linked successful page should appear with Add another Tag and Go to Equipment Screen
-------------------------------------------------------------------------------|-----------------------------------------------------
5. User can click on Add another tag if he wants to add another tag and it takes user to QR Scanner page. |
                                                                                                          | 5.1 User can perform same steps to scan again.
----------------------------------------------------------------------------------------------------------|----------------------------------------------------
6. Or user can go back to Equipment Dashboard by clicking on Go to Equipment Screen button | 6.1 Equipment Dashboard is displayed
----------------------------------------------------------------------------------------------------------|----------------------------------------------------
Exception conditions:                                                                                     |
The barcode is not clear or broken                                                                        |
The complete required details are not filled                                                              |
Invalid values provided in New cylinder fields                                                            |
----------------------------------------------------------------------------------------------------------|----------------------------------------------------



## Equipment Create Form

The "Equipment Create Form" is a web form designed for technicians to create new equipment entries. The form displays auto-populated information, including profile info, equipment tag ID, technician ID, and the create date (editable, defaulted to the current date). The technician can also edit the address, and if the organization location exists in the system, the organization's ID will be displayed.

The form dynamically populates the refrigerant ID based on the selected refrigeration type. Additionally, it calculates and displays the "Total Refrigerant Charge," which is the sum of the factory charge and additional charge.

The technician can enter the manufacturer's name, model number, serial number, equipment type, and refrigerant type. They can also input the factory charge amount (lbs) and additional refrigerant charge. If the technician selects "Yes," they can add the amount of refrigerant, which automatically updates the "Total Charge." Additionally, the form includes fields for the location description and additional notes.

# Equipment Create Form

## Auto Populated Information

- Profile Info: [Profile Info]
- Equipment Tag ID: EQUIP001
- Technician ID: TECH001
- Create Date: [Current Date]
- Address: [Editable Address]
- Organization's ID: [Organization ID (if exists in the system)]

## Refrigerant Information

- Refrigeration Type: [Refrigeration Type]
- Refrigerant ID: [Automatically populated based on Refrigeration Type]
- Total Refrigerant Charge (lbs): [Calculated as Factory Charge + Additional Charge]

## Equipment Details

- Manufacturer's Name: [Enter Manufacturer's Name]
- Model Number: [Enter Model Number]
- Serial Number: [Enter Serial Number]
- Equipment Type: [Enter Equipment Type]
- Refrigerant Type: [Enter Refrigerant Type]
- Factory Charge Amount (lbs): [Enter Factory Charge Amount]
- Additional Refrigerant Charge (lbs): [Enter Additional Refrigerant Charge]

## Add Refrigerant

- [ ] Yes
- [ ] No

- Amount of Refrigerant to Add (lbs): [Enter Amount]
- Location Description: [Enter Location Description]

## Additional Notes

When the submit button is pressed, the form also sends gps co-ordinates to the database (for now it just prints into the consol as database needs to be updated), default it asks for user permission for location access, which needs to be added to the previous screen that was disucssed to allow for location access.


