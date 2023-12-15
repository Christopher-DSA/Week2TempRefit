***SRS 2.2.9.1 Submit ODS - unpaid***


# 2.2.9 Submit ODS 
# 2.2.9.1 Submit ODS - Unpaid
Use case name:       | Submit ODS 
---------------------|--------------------
Scenario:            |The user updates ODS sheet and submits to the ODS sheet recipient email.
---------------------|--------------------
Triggering event:    |The user needs to update the ODS sheet due to maintenance and repair of the equipment.
---------------------|--------------------
Brief description:   |The user updates the ODS sheet by providing the test results and weight of the refrigerant added to the equipment if necessary.
---------------------|--------------------
Actors:              |Technician, Contractor, Organization, and Wholesaler
---------------------|--------------------
Related use cases:   |Enter login details and Scan QR Tag
---------------------|--------------------
Stakeholders:        |Technician, Contractor, Organization, Wholesaler, Management, Government
---------------------|--------------------
Preconditions:       |
                     |The user must have a REFit account.
                     |The user must log into his REFit account.
                     |The user must successfully scan the QR Tag or manually encoded the QR Reference number.
---------------------|--------------------
Postconditions:      |The ODS sheet must be updated and submitted.
---------------------|--------------------
Flow of activities:  |
---------------------|--------------------
*ACTOR*              | *SYSTEM*
---------------------|--------------------
1.  User successfully logs into the REFit account. (Refer to the Log into account and Reset password activity). | 1.1 System displays the Technician Dashboard.
---------------------|--------------------
2. User scans the QR tag. (Refer to the Scan QR tag activity).  |
                                                                |2.2 System displays the Equipment Dashboard.
                                                                |Equipment Dashboard features:
                                                                |
                                                                |The ODS Sheet tab 1 shows the following features:
                                                                |a. Back button – This button returns the user to the QR scanner.
                                                                |b. Date – This is a required field and automatically set to current date but the user has the option to change it.
                                                                |c. Job Number – This is a text field where user can input the job number
                                                                |d. Equipment Refrigerant Information – The details are auto-populated and disabled.
                                                                |e. Cancel button – This button returns the user to the Technician Dashboard. 
                                                                |f. Next button – This button sends the user to ODS Sheet tab 2.
----------------------------------------------------------------|--------------------
3. User inputs the ODS details.                                 |3.1 System allows the user to enter the ODS details.
----------------------------------------------------------------|--------------------
4. User has the option to cancel or continue to ODS Sheet tab 2.|4.1 If the user wants to proceed, he can click the Next button.
                                                                |4.2 User clicks the Cancel button.
                                                                | 4.1.1 System validates the entered information.
                                                                |4.1.2 System displays a trigger warning text for incorrect fields.
                                                                |4.1.3 System allows the user to edit details.
                                                                |4.1.4 System displays ODS sheet tab 2.
                                                                |
                                                                |The ODS Sheet tab 2 displays the following features:
                                                                |a. Back button – This button returns the user to ODS Sheet tab 1.
                                                                |b. Leak Test Result radio buttons – This is a required field that must be selected by the user. 
                                                                |c. Other Test Results checkbox – User can select from the given test results.
                                                                |d. PSIG Result – This is a text field where user must input the PSIG result if pressure test is performed.
                                                                |e. Additional Repair Notes – This is a text box where user can input additional notes related to the refrigerant or test results.
                                                                |f. Cancel button- This button returns the user to the Technician Dashboard.
                                                                |g. Next button – This button sends the user to the ODS Sheet tab 3.
                                                                |
                                                                |Constraints:
                                                                |a. Leak detected radio button must be selected to enable the Leak repaired or Leak not repaired radio buttons. 
                                                                |b. Pressure Test Performed must be selected as needed to enable data entry into the PSIG Result field. 
                                                                |
                                                                |4.2.1 System displays a Warning Modal about returning to the Technician Dashboard. 
                                                                |4.2.2 System allows the user to click the X or Back button of the Leave Warning Modal to stay on the current page.
                                                                |4.2.3 System allows the user to click the Leave button to return to the Technician Dashboard.
----------------------------------------------------------------|-------------------
5. User selects leak test result.                               |
                                                                |5.1 If a leak is detected, the user marks the Leak detected radio button.
                                                                |5.2 Else, the user marks the No leak detected radio button.                             
                                                                |5.1.1 System enables the Leak repaired / not repaired radio buttons.
                                                                |5.1.2 System allows the user to select relevant leak test results.
                                                                |5.1.3 System enables the user to select other test results.
                                                                |5.2.1 System allows the user to select other test results
----------------------------------------------------------------|-------------------
6. User marks the Pressure test performed checkbox.             | 6.1 System enables the PSIG result field for the user to enter the PSIG result.
----------------------------------------------------------------|-------------------
7. User enters additional details as needed.                    | 7.1 System allows the user to input repair notes as needed.
----------------------------------------------------------------|-------------------
8. User has the option to cancel or continue to ODS Sheet page 3. |8.1 If the user wants to proceed to ODS Sheet tab 3, he can click the Next button.
                                                                  |8.2 Else, the user clicks the Cancel button.
                                                                  |8.1.1 System validates the entered information.
                                                                  |8.1.2 System displays a trigger warning text for incorrect fields.
                                                                  |8.1.3 System allows the user to edit details.
                                                                  |8.1.4 System displays ODS Sheet tab 3-Unpaid if unpaid account.  
                                                                  |The ODS Sheet tab 3 - Unpaid has the following features:
                                                                  |a. Access Premium Feature popup message – This feature recommends the user to upgrade membership to Contractor.
                                                                  |    a.1 User has the option to show the message again.
                                                                  |    a.2 User can opt to upgrade the account or choose “Maybe Later”. 
                                                                  |b. Back button – This button returns the user to ODS Sheet tab 2
                                                                  |c. Added Refrigerant – This field allows the user to input the refrigerant weight added from the cylinder.
                                                                  |d. Review ODS Sheet button- This button sends the user to the Review ODS sheet page.
                                                                  |
                                                                  |8.1.5 System sends the user to ODS Sheet tab 3- Paid if paid account.  
                                                                  |
                                                                  |The ODS Sheet tab 3 – Paid has the following features:
                                                                  |a. Back button – This button returns the user to the ODS Sheet tab 2.
                                                                  |b. Scan Cylinder – This button sends the user to the QR scanner.
                                                                  |c. Review ODS Sheet – This button sends the user to the Review ODS Sheet page.
                                                                  |
                                                                  | 8.2.1 System displays a Warning Modal about returning to the Technician Dashboard 
                                                                  |8.2.2 System allows the user to click the X or Back button of the Leave Warning Modal to stay on the current page.
                                                                  |8.2.3 System allows the user to click the Leave button to return to the Technician Dashboard.
------------------------------------------------------------------|----------------------------------------------------------------
9. On the ODS Sheet tab 3 – Unpaid , the user has the option to not show the message to Access Premium Feature again. |
                                                    |9.1 If the user ticks the checkbox Don’t show me again, the message to Access Premium Feature would not show up again in the future.
                                                    |9.2 Else, the user can skip the checkbox.
                                                    |9.1.1 System allows the user to mark the checkbox of Don’t show Access Premium Feature message again.
                                                    |9.2.1 System allows the user not to mark the checkbox of Don’t show Access Premium Feature message again.
----------------------------------------------------|-------------------
10. User has the option to upgrade account.         |
                                                    |10.1 If the user wants to upgrade his account, he can click the Upgrade button (Refer to the Upgrade account activity).
                                                    |10.2 Else, the user clicks the Maybe Later button.
                                                    |10.1.1 If the upgrading of the account is successful, the system sends the user to ODS Sheet tab 3 for the paid account (Refer to Submit ODS – Paid from steps 9 to 13)
                                                    |10.2.1 System displays the ODS Sheet page 3 - Unpaid.
----------------------------------------------------|-------------------
11. User can enter the added refrigerant weight.    |
                                                    |11.1 User inputs the refrigerant weight and clicks the Review ODS Sheet button.
                                                    |11.2 User has not added refrigerant weight and just clicks the Review ODS Sheet button. 
                                                    |11.1.1 System allows the user to input the refrigerant.
                                                    |11.1.2 System sends the user to the Review ODS Sheet page.
                                                    |Constraint:
                                                    |a. Weight must include digits or numbers only.
                                                    |11.2.1 System displays the Review ODS Sheet page.
----------------------------------------------------|---------------------------------------
12. For each ODS section, the user is able to edit the entered details. |
                                                                        |12.1 After the user clicks the Edit button, the system changes the subheading into a text field and simultaneously changes the Edit button to Save button.
                                                                        |12.2 System allows the user to save changes.
                                                                        |12.3 System enables the Submit button once the Save button is clicked.
------------------------------------------------------------------------|------------------------------------------
13. User has the option to cancel or submit the ODS sheet.  |
                                                        |13.1 If the user wants to submit the ODS sheet, he can click the Submit button.
                                                        |13.2 Else, the user can click the Cancel button.
                                                        |13.1.1 System validates if all the fields are correct.
                                                        |13.1.2 System displays a trigger warning text for incorrect fields.
                                                        |13.1.3 System allows the user to edit and save the details.
                                                        |13.1.4 If all fields are correct, the system displays the ODS Sheet Submitted page.
                                                        |13.1.5 If the cylinder needs tag replacement, the system displays the ODS Sheet Submitted page along with a message to replace the tag.
                                                        |13.2.1 System displays a Warning Modal about returning to the Technician Dashboard 
                                                        |13.2.2 System allows the user to click the X or Back button of the Leave Warning Modal to stay on the current page.
                                                        |13.2.3 System allows the user to click the Leave button to go to the Technician Dashboard.4
--------------------------------------------------------|-------------------
14. User has the option to replace the faulty cylinder QR tag or not. |
                                                                      |14.1 If the user decides to replace the tag, he can click the Replace Tag button (Please refer to the Replace tag activity).
14.2 Else, the user clicks the Return to Dashboard button.            | 
                                                                      |14.1.1 If the QR tag is successfully replaced and the user clicks the Return to Dashboard button, the system  displays the Technician Dashboard.
                                                                      |14.2.1 The system sends the user back to the Technician Dashboard.
----------------------------------------------------------------------|-------------------
Exception conditions:                                                 |
1. Pressure test is performed but the PSIG result is not available.   |
2. The QR code cannot be scanned nor manually input into the system.  |
3. The user has no ODS license.                                       |
----------------------------------------------------------------------|-------------------



# 2.2.9.1 Submit ODS - Unpaid

 Use case name       | Submit ODS                    
---------------------|-------------------------------
 Scenario            | The user updates ODS sheet and submits to the ODS sheet recipient email. 
---------------------|-------------------------------
 Triggering event    | The user needs to update the ODS sheet due to maintenance and repair of the equipment. 
 ---------------------|-------------------------------
 Brief description   | The user updates the ODS sheet by providing the test results and weight of the refrigerant added to the equipment if necessary. 
 --------------------|-------------------------------
 Actors              | Technician, Contractor, Organization, and Wholesaler 
 ---------------------|-------------------------------
 Related use cases   | Enter login details and Scan QR Tag 
 ---------------------|-------------------------------
 Stakeholders        | Technician, Contractor, Organization, Wholesaler, Management, Government 
 ---------------------|-------------------------------
 Preconditions        | - The user must have a REFit account. 
                      | - The user must log into his REFit account. 
                      | - The user must successfully scan the QR Tag or manually encoded the QR Reference number. 
---------------------|-------------------------------
 Postconditions      | The ODS sheet must be updated and submitted. 
 --------------------|-------------------------------
 Flow of activities  |                                
 --------------------|-------------------------------
 *ACTOR*             | *SYSTEM*                       
---------------------|-------------------------------
 1. User successfully logs into the REFit account. (Refer to the Log into account and Reset password activity). | 1.1 System displays the Technician Dashboard.
 ---------------------|-------------------------------
 2. User scans the QR tag. (Refer to the Scan QR tag activity). | 2.2 System displays the Equipment Dashboard.
                                                                |Equipment Dashboard features: 
                                                                | - The ODS Sheet tab 1 shows the following features: 
                                                                |   a. Back button – This button returns the user to the QR scanner. 
                                                                |   b. Date – This is a required field and automatically set to the current date but the user has the option to change it. 
                                                                |   c. Job Number – This is a text field where the user can input the job number 
                                                                |   d. Equipment Refrigerant Information – The details are auto-populated and disabled. 
                                                                |   e. Cancel button – This button returns the user to the Technician Dashboard. 
                                                                |   f. Next button – This button sends the user to ODS Sheet tab 2.
---------------------|------------------------------- 
 3. User inputs the ODS details. | 3.1 System allows the user to enter the ODS details. 
 ---------------------|-------------------------------
 4. User has the option to cancel or continue to ODS Sheet tab 2. | 4.1 If the user wants to proceed, he can click the Next button. 
                                                                  | 4.2 User clicks the Cancel button. 
                                                                  |   4.1.1 System validates the entered information. 
                                                                  |   4.1.2 System displays a trigger warning text for incorrect fields. 
                                                                  |   4.1.3 System allows the user to edit details. 
                                                                  |   4.1.4 System displays ODS sheet tab 2. 
                                                                  | The ODS Sheet tab 2 displays the following features: 
                                                                  |   a. Back button – This button returns the user to ODS Sheet tab 1. 
                                                                  |   b. Leak Test Result radio buttons – This is a required field that must be selected by the user. 
                                                                  |   c. Other Test Results checkbox – User can select from the given test results. 
                                                                  |   d. PSIG Result – This is a text field where the user must input the PSIG result if a pressure test is performed. 
                                                                  |   e. Additional Repair Notes – This is a text box where the user can input additional notes related to the refrigerant or test results. 
                                                                  |   f. Cancel button- This button returns the user to the Technician Dashboard. 
                                                                  |   g. Next button – This button sends the user to the ODS Sheet tab 3. 
                                                                  | Constraints: 
                                                                  |   a. Leak detected radio button must be selected to enable the Leak repaired or Leak not repaired radio buttons. 
                                                                  |   b. Pressure Test Performed must be selected as needed to enable data entry into the PSIG Result field.
                                                                  | 4.2.1 System displays a Warning Modal about returning to the Technician Dashboard. 
                                                                  | 4.2.2 System allows the user to click the X or Back button of the Leave Warning Modal to stay on the current page. 
                                                                  | 4.2.3 System allows the user to click the Leave button to return to the Technician Dashboard. 
------------------------------------------------------------------|-------------------------------
 5. User selects leak test result. | 5.1 If a leak is detected, the user marks the Leak detected radio button. 
                                   | 5.1.1 System enables the Leak repaired / not repaired radio buttons. 
                                   | 5.1.2 System allows the user to select relevant leak test results. 
                                   | 5.1.3 System enables the user to select other test results. 
5.2 Else, the user marks the No leak detected radio button. |  5.2.1 System allows the user to select other test results 
------------------------------------------------------------|----------------------------------------------------------
 6. User marks the Pressure test performed checkbox. | 6.1 System enables the PSIG result field for the user to enter the PSIG result. 
 ------------------------------------------------------------|---------------------------------------------------------
 7. User enters additional details as needed. | 7.1 System allows the user to input repair notes as needed. 
 ------------------------------------------------------------|---------------------------------------------------------
 8. User has the option to cancel or continue to ODS Sheet page 3. | 8.1 If the user wants to proceed to ODS Sheet tab 3, he can click the Next button.
                                                                   | 8.1.1 System validates the entered information.
                                                                   |8.1.2 System displays a trigger warning text for incorrect fields.
                                                                   |8.1.3 System allows the user to edit details.
                                                                   |8.1.4 System displays ODS Sheet tab 3-Unpaid if unpaid account.  
                                                                   |
                                                                   |The ODS Sheet tab 3 - Unpaid has the following features:
                                                                   |a. Access Premium Feature popup message – This feature recommends the user to upgrade membership to Contractor.
                                                                   |    a.1 User has the option to show the message again.
                                                                   |    a.2 User can opt to upgrade the account or choose “Maybe Later”. 
                                                                   |b. Back button – This button returns the user to ODS Sheet tab 2
                                                                   |c. Added Refrigerant – This field allows the user to input the refrigerant weight added from the cylinder.
                                                                   |d. Review ODS Sheet button- This button sends the user to the Review ODS sheet page.
                                                                   |
                                                                   |8.1.5 System sends the user to ODS Sheet tab 3- Paid if paid account.  
                                                                   |
                                                                   |The ODS Sheet tab 3 – Paid has the following features:
                                                                   |a. Back button – This button returns the user to the ODS Sheet tab 2.
                                                                   |b. Scan Cylinder – This button sends the user to the QR scanner.
                                                                   |c. Review ODS Sheet – This button sends the user to the Review ODS Sheet page.
                                                                   |                                                                
8.2 Else, the user clicks the Cancel button.                       |
                                                                   |8.2.1 System displays a Warning Modal about returning to the Technician Dashboard 
                                                                   |8.2.2 System allows the user to click the X or Back button of the Leave Warning Modal to stay on the current page.
                                                                   |8.2.3 System allows the user to click the Leave button to return to the Technician Dashboard.
-------------------------------------------------------------------|----------------------------------------------------------------
9. On the ODS Sheet tab 3 – Paid , the user has the option to  scan a cylinder if refrigerant is added to the equipment or just review the ODS sheet.

                                                                        | 9.1 If the user has added refrigerant to the cylinder, he clicks the Scan Cylinder button (Refer to the Scan QR tag activity).
                                                                        | 9.1.1 System allows the user to scan the cylinder.
9.2 Else, the user clicks the Review ODS Sheet (Refer to Steps 13 to 15). |
                                                                          |9.2.1 System sends the user to Review ODS Sheet (Empty) page.
                                                                          |
                                                                          |The Review ODS -Empty page has the following features:
                                                                          |a. Back button – This button returns the user to the ODS Sheet tab 3.
                                                                          |b. Edit button – When clicked, this button changes subheadings into a text field to enable editing. Also, the Edit changes into Save and is required to be clicked to save information to the database.
                                                                          |c. Cancel – This button returns the user to the Technician Dashboard.
                                                                          |d. Submit button- This button sends the user to the ODS Submitted page. However, this button is disabled until the user clicks the Save button. 
--------------------------------------------------------------------------|---------------------------------------------------------------
10. User scans the QR tag successfully. |
                                |10.1 System displays a check mark animation along with the message “QR code successfully scanned”.
                                |10.2 System checks if refrigerants match. 
                                |10.3 If refrigerants are matched, the system displays the ODS Sheet tab 3 (Paid) along with the total added refrigerant with at least a one-second delay.
                                |10.4 If refrigerants are not matched, the system displays a Refrigerant Warning message with at least a one-second delay.
                                |10.5 Even though the refrigerants do not match, the system still allows the user to proceed and displays the ODS Sheet tab 3 (Paid) along with the total added refrigerant.
                                |10.6 However, the system also allows the user to go back and scan the correct QR tag.
-----------------------------------|---------------------------------------------------
11. On the ODS Sheet tab 3 (Paid), the user inputs the added refrigerant weight.|
                                                                                |11.1 System auto-updates the cylinder weight and total.
                                                                                |11.2 The cylinder section changes into text fields to allow the user to edit details as needed.
                                                                                |11.3 System changes the Edit button to the Save button to allow the user to save changes.
                                                                                |11.4 Once the Save button is clicked, the system enables the Scan Another Cylinder button.
-----------------------------------|---------------------------------------------------
12. User has the option to scan another cylinder.   |
                                                    |12.1 If the user has another cylinder to scan, he can click the Scan Another Cylinder button (Refer to the Scan QR tag activity).
                                                    |12.2 Else, the user clicks the Review ODS Sheet button.
                                                    |12.1.1 If the scanning is successful, the system allows the user to add the refrigerant weight, edit details, and save the information as detailed in the previous steps.
                                                    |12.2.1 System displays the Review ODS Sheet page.
-----------------------------------|---------------------------------------------------
13. For each ODS section, the user is able to edit the entered details. |
                                                        |13.1 After the user clicks the Edit button, the system changes the subheading into a text field and simultaneously changes the Edit button to the Save button.
                                                        |13.2 System allows the user to save changes.
                                                        |13.3 System enables the Submit button once the Save button is clicked.
-----------------------------------|---------------------------------------------------
14. User has the option to cancel or submit the ODS sheet. |
                                                           |14.1 If the user wants to submit the ODS sheet, he can click the Submit button.
                                                           |14.2 Else, the user can click the Cancel button.
                                                           |14.1.1 System validates if all the fields are correct.
                                                           |14.1.2 System displays a trigger warning text for incorrect fields.
                                                           |14.1.3 System allows the user to edit and save the details.
                                                           |14.1.4 If all fields are correct, the system displays the ODS Sheet Submitted page.
                                                           |14.1.5 If the cylinder needs tag replacement, the system displays the ODS Sheet Submitted page along with a message to replace the tag.
                                                           |14.2.1 System displays a Warning Modal about returning to the Technician Dashboard 
                                                           |14.2.2 System allows the user to click the X or Back button of the Leave Warning Modal to stay on the current page.
                                                           |14.2.3 System allows the user to click the Leave button to go to the Technician Dashboard.
-----------------------------------|---------------------------------------------------
15. User has the option to replace the faulty cylinder QR tag or not. |
                                                                      |15.1 If the user decides to replace the tag, he can click the Replace Tag button (Please refer to the Replace tag activity).
                                                                      |15.2 Else, the user clicks the Return to Dashboard button.
                                                                      |15.1.1 If the QR tag is successfully replaced and the user clicks the Return to Dashboard button, the system displays the Technician Dashboard.
                                                                      |15.2.1 The system sends the user back to the Technician Dashboard.
-----------------------------------|---------------------------------------------------
Exception conditions:
1. Pressure test is performed but the PSIG result is not available.
2. QR code cannot be scanned nor manually input into the system.
3. The user has no ODS license.
-----------------------------------|---------------------------------------------------

