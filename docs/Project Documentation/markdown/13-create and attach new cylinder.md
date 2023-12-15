***SRS 2.2.5 Add New Cylinder***
# 2.2.5 Add new cylinder

Use case name:     |        Add new cylinder 
-------------------|-------------------
Scenario:          |Adding tag to New Cylinder
-------------------|-------------------
Triggering event:  |New cylinders are delivered.
-------------------|-------------------
Brief description: |When new cylinders are delivered technicians needs to add tag to them. 
-------------------|-------------------
Actors:            | Technicians
-------------------|-------------------
Related use cases: | 
-------------------|-------------------
Stakeholders:      |Technicians, Contractor, client, government
-------------------|-------------------
Preconditions:     |Technicians must be logged in successfully in REFit App.
                   |Technician should have access to the Technician Dashboard.
-------------------|-------------------
Postconditions:    |The QR tag should be linked with the cylinder.
-------------------|-------------------
Flow of activities: 
-------------------|-------------------
Actor              |System
-------------------|-------------------
1. Technician enters username and password and logins successfully.| 1.1 User is signed in Successfully and displays technician Dashboard.
-------------------------------------------------------------------|-------------------------------------------------------------
2. User clicks on Scan QR Tags button in Technician Dashboard.     |
                                                                   |2.1  Only for first use , it asks permission to access phone’s camera and modal is appeared with Deny and Accept as options.
                                                                   |2.2 User needs to Accept it in order to start scanning. If accepted it will not ask again for permission.
                                                                   |2.3  If Deny button is clicked, it takes back customer to Technician Dashboard page.
-------------------------------------------------------------------|--------------------------------------------------------------
3. User scans the QR tag                                           |
                                                                   |3.1 The scan is successful and It shows Select Cylinder Type Screen with 3 options:
                                                                   |New Cylinder
                                                                   |Recovery Cylinder Clean/Reusable
                                                                   |Recovery Cylinder Burnout/Recycle
-------------------------------------------------------------------|------------------------------------------------
4. Click on New cylinder button                                    |
                                                                   |4.1 New Cylinder form is displayed.
                                                                   |
                                                                   |This form requires following information:
                                                                   |Create Date:  It should be auto populated with current DateTime.
                                                                   |Wholesaler: Fill the wholesaler detail
                                                                   |
                                                                   |Cylinder information
                                                                   |Cylinder Tare weight: 
                                                                   | Choose unit from dropdown
                                                                   |Put values for lb and oz
                                                                   |Refrigerant Type: Enter refrigerant type
                                                                   |Current Refigerant Weight in Cylinder
-------------------------------------------------------------------|---------------------------------------------------
5. Fill in all the required details correctly in the new cylinder screen and then click Submit. | 5.1 Cylinder Linked page is displayed on successful submission. 
                                                                                                |This page has a  confirmation message and an option to Add another tag or Return to Dashboard.
-------------------------------------------------------------------|-------------------------------------------
6. User can click on Add another tag if he wants to add another tag and it takes user to QR Scanner page.| 6.1 User can perform same steps to scan again.
-------------------------------------------------------------------|--------------------------------
7. Or user can go back to technician Dashboard by clicking on Go to Dashboard button |7.1 Technician Dashboard is displayed
-------------------------------------------------------------------|--------------------------------
Exception conditions:                                              |
                                                                   |The barcode is not clear or broken
                                                                   |The complete required details are not filled
                                                                   |Invalid values provided in New cylinder fields
-------------------------------------------------------------------|-----------------------------------------------------

***SRS 2.2.6 Add Recovery Cylinder***

# 2.2.6 Add new recovery cylinder clean/ reusable
Use case name:  |Add new recovery cylinder clean/ reusable
----------------|-----------------------------------------
Scenario:       |Adding tag to New Recovery Cylinder
----------------|-----------------------------------------
Triggering event: |New cylinders are delivered.
------------------|------------------------------------
Brief description:| When new cylinders are delivered technicians needs to add tag to them. 
------------------|------------------------------------------
Actors:           |Technicians
-------------------|----------------------------------------------------
Related use cases: |
-------------------|----------------------------------------------------
Stakeholders:      | Technicians, Contractor, client, government
-------------------|----------------------------------------------------
Preconditions:     |
                   |Technicians must be logged in successfully in refit App
                   |Technician should have access to Technician Dashboard
-------------------|----------------------------------------------------
Postconditions:    |
                   |The tag should be linked with the cylinder
-------------------|----------------------------------------------------
*Flow of activities:*|
---------------------|----------------------------------------------------
Actor                |System
---------------------|----------------------------------------------------
1. Technician enters username and password and logins successfully.| 1.2 User is signed in Successfully and displays technician Dashboard.
-------------------------------------------------------------------|----------------------------------------------------
2. User clicks on Scan QR Tags button in Technician Dashboard.|
                                                            |2.1 Only for first use , it asks permission to access phone’s camera and modal is appeared with Deny and Accept as options.
                                                            |2.2 User needs to Accept it in order to start scanning. If accepted it will not ask again for permission.
                                                            |2.3 If Deny button is clicked, it takes back customer to Technician Dashboard page.
------------------------------------------------------------|---------------------------------------------------
3. User scan the QR code                                    |
                                                            |3.1 The scan is successful and It shows Select Cylinder Type Screen with 3 options:
                                                            |a. New Cylinder
                                                            |b. Recovery Cylinder Clean/Reusable
                                                            |c. Recovery Cylinder Burnout/Recycle
------------------------------------------------------------|---------------------------------------------
4. Click on Recovery Cylinder Clean/Reusable                |
                                                            |4.1 New Cylinder form is displayed
                                                            |
                                                            |This form requires following info
                                                            |Create Date:  It should be auto populated with current DateTime.
                                                            |WholeSaler: Fill the wholesaler detail
                                                            |
                                                            |Cylinder information
                                                            |Cylinder Tare weight: 
                                                            |Choose unit from dropdown
                                                            |Put values for lb and oz
                                                            |Refrigerant Type: Enter refrigerant type
                                                            |       III. Current Refigerant Weight in Cylinder
------------------------------------------------------------|---------------------------------------------------
5. Fill all the required details correctly in New cylinder screen and then click Submit| 5.1 Cylinder Linked page is displayed on successful submission. 
                                                                                       |This page has confirmation message and option to Add another tag or Return to Dashboard.
------------------------------------------------------------|------------------------------------------------
6. User can click on Add another tag if he wants to add another tag and it takes user to QR Scanner page. | 6.1 User can perform same steps to scan again.
------------------------------------------------------------|------------------------------------------------
7. Or user can go back to technician Dashboard by clicking on Go to Dashboard button | 7.1 Technician Dashboard is displayed
------------------------------------------------------------|--------------------------------------------------------
Exception conditions:                                       |
1. The barcode is not clear or broken                       |
2. The complete required details are not filled             |
3. Invalid values provided in New cylinder fields           |
------------------------------------------------------------|----------------------------------------

### Note : may need to be moved to 14-cylinder repair and recovery page.md ( based on title , but this file already has the recovery form options so placed it here)-yael

# 2.2.7 Add new recovery cylinder burnout/ recycle
Use case name:                | Add new recovery cylinder burnout/ recycle
------------------------------|--------------------------------------------------------
Scenario:                     |Adding tag to New Recovery Cylinder Burnout/ Recycle
------------------------------|--------------------------------------------------------
Triggering event:             |New cylinders are delivered.
------------------------------|--------------------------------------------------------
Brief description:            |When new cylinders are delivered technicians needs to add tag to them. 
------------------------------|--------------------------------------------------------
Actors:                       |Technicians
------------------------------|--------------------------------------------------------
Related use cases:            |
------------------------------|--------------------------------------------------------
Stakeholders:                 |Technicians, Contractor, client, government
------------------------------|-----------------------------------------------
Preconditions:                |
                              |Technicians must be logged in successfully in refit App
                              |Technician should have access to Technician Dashboard
------------------------------|----------------------------------------------------
Postconditions:               | The tag should be linked with the cylinder
------------------------------|-----------------------------------------------
*Flow of activities:*         |
------------------------------|----------------------------------------------------
*ACTOR*                       |     *SYSTEM*
------------------------------|----------------------------------------------------
1. Technician enters username and password and logins successfully. |1.1 User is signed in Successfully and displays technician Dashboard.
------------------------------|----------------------------------------------------
2. User clicks on Scan QR Tags button in Technician Dashboard.|
                                                            |2.1 Only for first use , it asks permission to access phone’s camera and modal is appeared with Deny and Accept as options.
                                                            |2.2 User needs to Accept it in order to start scanning. If accepted it will not ask again for permission.
                                                            |2.3 If Deny button is clicked, it takes back customer to Technician Dashboard page.
------------------------------|----------------------------------------------------
3. User Scans the QR tag successfully                       |
                                                            |The scan is successful and It shows Select Cylinder Type Screen with 3 options:
                                                            |New Cylinder
                                                            |Recovery Cylinder Clean/Reusable
                                                            |Recovery Cylinder Burnout/Recycle
------------------------------------------------------------|-----------------------------------------
4. Click on Recovery Cylinder Burnout/Recycle               | New Recovery cylinder Burnout form is displayed
------------------------------|----------------------------------------------------
5. Fill all the required details correctly in the form and then click Submit|
                                                                            | Cylinder Linked page is displayed on successful submission. 
                                                                            |This page has confirmation message and option to Add another tag or Return to Dashboard.
--------------------------------------------------------------------------------------|----------------------------------------------------
6. User can click on Add another tag if he wants to add another tag and it takes user to QR Scanner page. | User can perform same steps to scan again.
--------------------------------------------------------------------------------------|----------------------------------------------------
7. Or user can go back to technician Dashboard by clicking on Go to Dashboard button  |
                                                                                      |7.1 Technician Dashboard is displayed
                                                                                      |
                                                                                      |
                                                                                      |
                                                                                      |
                                                                                      |
                                                                                      |
                                                                                      |
                                                                                      |Exception conditions:
                                                                                      |1. The barcode is not clear or broken
                                                                                      |2. The complete required details are not filled
                                                                                      |3. Invalid values provided in New cylinder fields
--------------------------------------------------------------------------------------|----------------------------------------------------





## Cylinder Type Selection Form

The "Cylinder Type Selection Form" is a web form that allows users to choose between two options: "New Cylinder" or "Recovery Cylinder." Upon selection, the form dynamically redirects the user to the corresponding page for the chosen option.

## New Cylinder Option

If the user selects "New Cylinder," they will be directed to the "New Cylinder Form." This form displays auto-populated information such as cylinder tag ID, refrigerant ID, technician ID, and the select date (which defaults to the current date but can be edited). The user can then enter details such as refrigerant type, cylinder size in lbs, refrigerant weight in lbs, purchase date (if different from the manufacturer date),wholesaler, Cylinder Tare Weight(empty cylinder weight, subtracting the refrigerant weight), refrigenrant type used in the cylinder and its current weight. 

Input is taken from user logged in (Technician) and saved in ounce in the database. It will allow user to input weight for cylinder and refrigerant in lb/oz or Kg/gm but will convert it to oz to save it in the database. 

Once user clicks submit, it redirects to Tag created sucessfully page and ask user to either create new cylinder Tag or return to the Dashboard(Currenly re-directing to Technician)

## Recovery Cylinder Option

If the user selects "Recovery Cylinder," they will be directed to the "Recovery Cylinder Form." This form displays non-editable details such as cylinder tag ID, company name, refrigerant ID, technician ID, and the recovery date (which defaults to the current date but can be edited). The user must then enter details such as refrigerant type, cylinder type (with options: clean/reuse, non-usable, and burnout), cylinder size in lbs, and refrigerant type in lbs.

# Cylinder Type Selection Form

Please select a cylinder type:

- [ ] New Cylinder
- [ ] Recovery Cylinder

[Select](#)

---

## New Cylinder Form



### Auto Populated Information

- Cylinder Tag ID: [Cylinder Tag ID]
- Refrigerant ID: [Refrigerant ID]
- Technician ID: [Technician ID]
- Select Date: [Current Date]

### New Cylinder Details

- Refrigerant Type: [Enter Refrigerant Type]
- Cylinder Size (lbs): [Enter Cylinder Size]
- Refrigerant Weight (lbs): [Enter Refrigerant Weight]
- Purchase Date (if different): [Enter Purchase Date]
- Wholesaler: [Enter Wholesaler]
- Cylinder Tare Weight  - Enter weight in lb/oz or kg/gm
- Refrigernat Type  - select from the provided list of refrigenerat types from Database
- Refrigernat Weight - nter weight in lb/oz or kg/gm
- Current Date - Selects current date(Editable)



---

## Recovery Cylinder Form

### Auto Populated Information

- Cylinder Tag ID: [Cylinder Tag ID]
- Company Name: [Company Name]
- Refrigerant ID: [Refrigerant ID]
- Technician ID: [Technician ID]
- Recovery Date: [Current Date]

### Recovery Cylinder Details

- Refrigerant Type: [Enter Refrigerant Type]
- Cylinder Type:
  - [ ] Clean/Reuse
  - [ ] Non-Usable
  - [ ] Burnout
- Cylinder Size (lbs): [Enter Cylinder Size]
- Refrigerant Type (lbs): [Enter Refrigerant Type]


## Update Cylinder form 
This form allows user(Technichian) to update refrigernat in unit from the cylinder. It shows auto populated fields like technician id, Cylinder Id, Refrigerent Id, Cylinder Type, Cylinder size(lbs). it allows user to update Refrigerant Weight Added to Equipment (lbs). It checks to make sure refrigerent wieght does not exceed then its original weight. Later, Radio selection option ask user to either add cylinder(New Cylinder - replace) or just update the one added already above. 

## Update Cylinder Form 

### Auto Populated Information

- Cylinder Tag ID: [Cylinder Tag ID]
- Refrigerant ID: [Refrigerant ID]
- Technician ID: [Technician ID]
- Cylinder Type
- Cylinder Size 
- Current Refrigerant Weight (lbs)

### Update Cylinder Details
- Create Date(Logging Date)
- Refrigerant Weight After Service (lbs): Changes based on refrigerant needed to be added to the unit 
- Add cylinder : Radio selection to add new cylinder or to update existing. 




