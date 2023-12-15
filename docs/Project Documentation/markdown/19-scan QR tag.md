## QR Tag Scanning and Cylinder Selection Page
## Detailed Chart from SRS
2.2.3 Scan QR Tag
------------------|--------------------------------
Use case name:    |Scan QR Tag
------------------|--------------------------------
Scenario:         |The user scans the cylinder or equipment QR tag.
------------------|--------------------------------
Triggering event: |The user wants to update the refrigerant weight, track refrigerant status, submit ODS, add new cylinder/equipment, replace QR tag, etc. 
------------------|--------------------------------
Brief description:|The user scans the QR tag or manually encodes the QR reference number if QR code is unreadable.
------------------|--------------------------------
Actors:           |Technicians and Contractors
------------------|--------------------------------
Related use cases:|Replace QR tag, Add new cylinder, Add new equipment, Submit ODS, Repair equipment, Recover equipment, etc.
------------------|--------------------------------
Stakeholders:     ||Technician, Contractor, Organization, Wholesaler, Management, and Government
------------------|--------------------------------
Preconditions:    |User must be logged in successfully to the REFit application.
------------------|---------------------------------
Postconditions:   |User must be able to scan the QR code successfully.
                  |User must be able to input the QR reference number if QR code is unreadable.
------------------|--------------------------------
Flow of activities:|
------------------|-----------------------------------
Actor             | System
------------------|-----------------------------
1. User successfully logs into REFit account. | 1.1 System displays the Dashboard.
------------------|-----------------------------
2. User clicks the Scan QR Tags button.|


                                        |If the user has a previous permission to access the camera, the system displays the QR scanner screen.
                                        |The QR scanner screen displays the following features:
                                        |a. QR scanner – This feature captures the information encoded in the QR code printed on the equipment tag or cylinder tag.
                                        |b. QR code not working? text button – This button allows the user to try scanning again or sends the user to the Manually Input Identifier screen. 
                                        |
                                        |If the Scan feature is being used for the first time or if permission to access the camera has been previously denied, the system disables the QR scanner and prompts a permission request for camera access.
                                        |
                                        |The permission request modal shows the following buttons:
                                        |a. X button- This button disables the camera and returns the user to the Dashboard.
                                        |b. Don’t Allow button- This button disables the camera and returns the user to the Dashboard page.
                                        |c. OK button – This button grants permission to access the camera. Using this application, the permission access modal will not be displayed in the future once the OK button is clicked unless camera access is modified in the settings menu.
----------------------------------------|----------------------------------------
3. User has the option to grant camera access or not. |

                                                      |3.1 If the user allows camera access, he can click the OK button.
                                                      |
                                                      |3.2 Else, the user clicks the X or Don’t Allow button.
                                                      |
                                                      |
                                                      |
                                                      |
                                                      |3.1.1 System displays the QR scanner.
                                                      |
                                                      |
                                                      |
                                                      |3.2.1 System disables the QR code scanning.
                                                      |3.2.2 System returns the user to the Dashboard page.
------------------------------------------------------|--------------------------------------------------
4. User scans the QR code.                            |
                                                      |4.1 If the QR code is successfully scanned, the system displays a check mark animation along with a message “QR code successfully scanned” and directs the user to the Cylinder / Equipment Dashboard with at least one-second delay.
                                                      |
                                                      |The Cylinder Dashboard shows the following features:
                                                      |a. Cylinder Type - This describes the unit type of the cylinder.
                                                      |b. Refrigerant Type – This shows the type of refrigerant contained in the cylinder.
                                                      |c. Amount of Refrigerant in Cylinder – This displays the amount of refrigerant inside the cylinder.
                                                      |d. Replace QR Tag Card – This sends the user to the Replace QR Tag screen where the Technician can scan and replace the faulty QR tag.
                                                      |e. Usage History Tag – This card sends the user to the history of the QR tag. 
                                                      |f. Remove QR Tag – This sends the user to the Remove QR tag screen.
                                                      |
                                                      |The Equipment Dashboard displays the following features:
                                                      |a. Equipment Unit Type – This describes the unit type of the equipment.
                                                      |b. Equipment Unit # - This shows the unit number of the equipment.
                                                      |c. ODS Card – This card sends the user to the ODS Sheet where the Technician can update the cylinder and equipment details such as weight and type. Once all the necessary details are updated, the Technician can submit the form to the ODS sheet email recipient.
                                                      |d. Recover and Decommission Card -This card sends the user to the Recovery ODS Sheet where the Technician can update recovery information and equipment details. Once all the necessary details are updated, the Technician can submit the form to the relevant email recipient.
                                                      |e. View ODS History Card – This card describes the history of the equipment.
                                                      |f. Maintenance History Card – This card sends the user to the Maintenance sheet where the Technician can update about the maintenance and repair details of the equipment.
------------------------------------------------------|------------------------------------------------
5. User does not align the QR code within the designated box for 15 seconds or the QR code is not readable. |
                                                                                                            |5.1 System displays the QR Code Not Found modal after a time out of 15 seconds.  The modal shows a photo of the REFit QR tag, providing a visual clue of the correct QR code to the user. This modal contains the Try Again button and Manually Input Identifier text button along with the following troubleshooting tips:
                                                                                                            |
                                                                                                            |Try:
                                                                                                            |Cleaning the QR tag surface 
                                                                                                            |Scanning the QR tag in the designated box on the screen
                                                                                                            |
                                                                                                            |The QR Code Not Found modal has the following buttons:
                                                                                                            |a. Try Again button – This sends the user back to the QR scanner.
                                                                                                            |b. Manually Input Identifier text button – This sends the user to the Manual Input screen.
------------------------------------------------------------------------------------------------------------|------------------------------------------------------------
6. User has the option to try scanning again or manually input the identifier.                              |

                                                                                                            |6.1 If the user wants to try again, he can click the Try Again button to scan the QR code again.
                                                                                                            |
                                                                                                            |
                                                                                                            |
                                                                                                            |
                                                                                                            |
                                                                                                            |
                                                                                                            |6.2  Else, the user can click the Manual Input Identifier button.
                                                                                                            |
                                                                                                            |
                                                                                                            |
                                                                                                            |
                                                                                                            |
                                                                                                            |6.1.1 System displays the QR scanner and allows the user to scan again.
                                                                                                            |6.1.2  If the QR tag is scanned successfully, the system displays a check mark animation along with a message “QR code successfully scanned” and directs the user to the  Cylinder / Equipment Dashboard with at least one second delay.
                                                                                                            |6.1.3 If the scanning is not successful after a 15-second time out, the system displays the QR Code Not Found modal and asks the user to try again or manually input the identifier.
                                                                                                            |
                                                                                                            |6.2.1 System displays the Manual Input screen.
                                                                                                            |
                                                                                                            |The Manual Input screen has the following features:
                                                                                                            |a. QR Reference Number - This field is a textbox that allows the user to enter the QR Reference number.
                                                                                                            |b. Cancel button – This button sends the user back to the Dashboard page.
                                                                                                            |c. Next button- If the QR Reference number is correctly encoded, this button sends the user to the Cylinder or Equipment page. Otherwise, the system displays a trigger warning text. 
                                                                                                            |d. Contact Customer Support text button- This button sends the user to the customer support page.
------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------
7. User enters the QR Reference number manually.                                                            |
                                                                                                            |System allows the user to enter the QR reference number.
                                                                                                            |System processes and validates the entered QR Reference number.
                                                                                                            |7.3 If the QR Reference number is correct and existing, the system displays a check mark next to the entered QR reference number to show that the number is successfully located. 
                                                                                                            |
                                                                                                            |From this page, the user can select from the following options:
                                                                                                            |a. Next button – This button sends the user to the Cylinder / Equipment page.
                                                                                                            |b. Cancel button – This button sends the user back to the Dashboard.
                                                                                                            |c. Back button – This button sends the user back to the Dashboard.
                                                                                                            |
                                                                                                            |Also, the user has the option to replace the QR tag before proceeding to the next page:
                                                                                                            |d. Replace Now button- This button sends the user to the Replace QR Tag page.
                                                                                                            |e. Remind Me Later button– This button sends the user back to the Dashboard. After implementing a certain activity, the user will be prompted again to replace the faulty QR tag. 
                                                                                                            |f. Contact Customer Support- This button directs the user to an external link that handles customer concerns. 
                                                                                                            |
                                                                                                            |7.4 If the QR Reference number is not existing, the system displays a message, “This code can’t be located.”
------------------------------------------------------------------------------------------------------------| ----------------------------------------------------------------
8. If the manually entered QR Reference number is successfully found,                                   |
the user has the option to proceed to the Cylinder/ Equipment Dashboard or return to the Dashboard page.|

                                                                                                        |8.1 If the user wants to go to the Cylinder / Equipment page, he can click the Next button and decide whether to replace the QR tag or not.
                                                                                                        |8.2 Else, the user clicks the Cancel button to return to the Dashboard page.
                                                                                                        |8.1.1 If the user clicks the Next button and the Replace Now button to replace the tag, the system displays the QR Tag page (Refer to the Replace QR tag activity). After successfully replacing the faulty QR tag, the system sends the user to the Cylinder / Equipment Dashboard.
                                                                                                        |8.1.2 If the User clicks the Next button and the Remind Me Later button, the system directs him to the Cylinder / Equipment Dashboard. After an activity, the user will be prompted again to replace the faulty QR tag.
                                                                                                        |8.2.1 System displays a Warning Modal about returning to the Dashboard. 
                                                                                                        |8.2.2 System allows the user to click the X or Back button of the Leave Warning Modal to stay on the current page.
                                                                                                        |8.2.3 In the Leave Warning Modal, the system allows the user to click the Leave button to return to theDashboard.
--------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------
9. If the QR code is not found, the user has the option to replace the tag or seek assistance from Customer Support. |

                                                                                                                     |9.1 If the user wants to replace the tag, he can click the Replace Now button.
                                                                                                                     |
                                                                                                                     |9.2 Else the user can click the Contact Customer Support button.
                                                                                                                     |
                                                                                                                     |
                                                                                                                     |
                                                                                                                     |
                                                                                                                     |
                                                                                                                     |
                                                                                                                     |9.1.1 System displays the Replace QR Tag page (Refer to the Replace QR tag activity). 
                                                                                                                     |9.1.2 If the QR tag is successfully replaced, the system sends the user to the Cylinder or Equipment page.
                                                                                                                     |
                                                                                                                     |9.2.1 System displays the Contact Customer Support page which is an external solution that handles customer concerns (Refer to the Contact customer support activity).
                                                                                                                     |
                                                                                                                     |
                                                                                                                     |
                                                                                                                     |Exception conditions:
                                                                                                                     |1. The QR Reference number is missing, unavailable, or unreadable.
---------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------




When a technician scans a QR tag, they are directed to a page that allows them to choose a cylinder type. The page presents two options: "New Cylinder" or "Recovery Cylinder." Here's how the process unfolds:

## Select Cylinder Type
When a technician scans a QR tag, they are presented with the option to select a cylinder type.

 New Cylinder 
 Recovery Cylinder
 
## New Cylinder Option
If the technician chooses the "New Cylinder" option, they are directed to a form where they can input information. The form includes non-editable auto-populated fields:

Cylinder Tag ID: [Auto-Populated]
Refrigerant ID: [Auto-Populated]
Technician ID: [Auto-Populated]
Select Date: [Choose Date]
Additionally, the technician can input the following details:

Refrigerant Type: [Enter Refrigerant Type]
Cylinder Size (lbs): [Enter Cylinder Size]
Refrigerant Weight (lbs): [Enter Refrigerant Weight]
Purchase Date: [Enter Purchase Date]
Wholesaler: [Enter Wholesaler Name]
## Recovery Cylinder Option
If the technician selects the "Recovery Cylinder" option, they are directed to a form where they can input information. The form includes non-editable auto-populated fields:

Cylinder Tag ID: [Auto-Populated]
Company Name: [Auto-Populated]
Refrigerant ID: [Auto-Populated]
Technician ID: [Auto-Populated]
Recovery Date: [Choose Recovery Date]
The technician is prompted to provide the following details:

Refrigerant Type: [Enter Refrigerant Type]
Cylinder Type: [Select Cylinder Type: Clean/Reuse, Non-Usable, Burnout]
Cylinder Size (lbs): [Enter Cylinder Size]
Refrigerant Type (lbs): [Enter Refrigerant Weight]
The technician is provided with an interactive experience where they can select the appropriate cylinder type and proceed to enter the corresponding details. This process aids in efficient data collection and tracking for cylinder management.