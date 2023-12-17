***SRS 2.2.10***
# 2.2.10 Recover equipment ODS
## 2.2.10.1 Recover equipment ODS - Unpaid 
Use case name:                      | Recover equipment ODS
------------------------------------|--------------------------------------
Scenario:                           |The user updates ODS sheet for recovery and decommission.
------------------------------------|--------------------------------------
Triggering event:                   |The user needs to update the ODS sheet for recovery and decommission
------------------------------------|--------------------------------------
Brief description:                  |The user needs to recover and decommission ODS
------------------------------------|--------------------------------------
Actors:                             |Technician 
------------------------------------|--------------------------------------
Related use cases:                  |Scan QR Tag, Replace QR Tag
------------------------------------|--------------------------------------
Stakeholders:                       |Technician, Contractor, Organization, Wholesaler, Management, Government 
------------------------------------|--------------------------------------
Preconditions:                      |
                                    |1. The user must have a REFit account. 
                                    |2. The user must log into his REFit account.
                                    |3. The user must successfully scan the QR Tag or manually input identifier
------------------------------------|--------------------------------------
Postconditions:                     |The Recovery ODS sheet must be updated and submitted. 
------------------------------------|--------------------------------------
Flow of activities:                 |
------------------------------------|--------------------------------------
*ACTOR*                               | *SYSTEM*
------------------------------------|--------------------------------------
1. User logs into the REFit account (Refer to the Log into account and Reset Password activity). | 1.1 System displays the Technician Dashboard.
------------------------------------|--------------------------------------
2. User clicks the 'Recover and Decommission' card. | 2.1 The system displays the Display 'Prepare Equipment Tag' Screen.
                                                    | The Prepare Equipment Tag Screen shows the following features: 
                                                    |a. Back button – This button returns the user to the Technician Dashboard. | b. ‘Don’t show me again’ checkbox – If selected it goes straight to the QR Scanner page the next time the user clicks on the 'Recover and Decommission' card.
                                                    |c. ‘Ready to Scan’ button – This is a button that takes the user to the ‘QR Scanner’ page.
                                                    |d. ‘Add New QR’ button – This is a button that takes the user to the Replace QR code page.
------------------------------------|--------------------------------------
3. User has the option to Scan the existing QR code or Add new QR code if the previous one is damaged.|
(Refer to the ‘Replace QR Tag’ and ‘Scan QR Tag’ activity) |
3.1 If the user wants to use the existing QR code, they click the ‘Ready to Scan’ button. | 3.1.1 System displays the ‘QR Scanner’ Page
3.2 If the user wants to scan a new QR code, they click the ‘Add New QR’ button. | 3.2.1 System displays the ‘Replace Tag’ page
------------------------------------|--------------------------------------
4. User scans the QR tag | 4.1 The scan is successful and goes to the ‘Equipment Page’
                          |The Equipment Page shows the following cards: 
                          |a. Repair and ODS – This button returns the user to the Technician Dashboard. 
                          | b. Recover and Decommission – If selected it goes straight to the QR Scanner page the next time the user clicks on the 'Recover and Decommission' card.
                          |c. Unit ODS History – This is a button that takes the user to the ‘QR Scanner’ page.
                          |d. Maintenance History – This is a button that takes the user to the Replace QR code page.
------------------------------------|--------------------------------------
5. The user clicks on the ‘Recover and Decommission’ card | 5.1.1 If the user has scanned the QR code it goes to the ‘Recovery-1’ page
                                                          |5.1.2 If the user has used a manual input identifier, it gives the option to either Replace the QR Tag or to Remind the User later and goes to the ‘Recovery-1’ page.
                                                          |The Recovery ODS Sheet tab 1 shows the following features: 
                                                          |a. Back button – This button returns the user to the Equipment Page. 
                                                          | b. Date – This is a required field and automatically set to the current date, but the user has the option to change it.
                                                          |c. Job Number – This is a text field where the user can input the job number 
                                                          | d. Equipment Refrigerant Information – The details are auto-populated and disabled.
                                                          |e. Cancel button – This button returns the user to the Technician Dashboard. 
                                                          | f. Next button – This button sends the user to ODS Sheet tab 2
------------------------------------|--------------------------------------
6. User changes the date if required and inputs the Job Number | 6.1 System allows the user to enter the ODS details.
------------------------------------|--------------------------------------
7. User has the option to cancel or continue to ODS Sheet tab 2.|
                                                                |7.1 User clicks the Cancel button. | 7.1.1 System displays a Warning Modal about returning to the Equipment Page.  
                                                                |7.1.2 System allows the user to click the X or Back button of the Leave Warning Modal to stay on the current page. 
                                                                |7.1.3 System allows the user to click the Leave button to return to the Equipment Page.
7.2 If the user wants to proceed, they can click the Next button. | 7.2.1 System validates the entered information.
                                                                 |7.2.2 System displays a trigger warning text for incorrect fields. 
                                                                 | 7.2.3 System allows the user to edit details.
                                                                |7.2.4 System displays ODS sheet tab 2.

                                                                |The ODS Sheet tab 2 displays the following features: 
                                                                |a. Back button – This button returns the user to ODS Sheet tab 1. 
                                                                | b. Leak Test Result radio buttons – This is a required field that must be selected by the user.
                                                                |c. Other Test Results checkbox – User can select from the given test results. 
                                                                | d. PSIG Result – This is a text field where the user must input the PSIG result if a pressure test is performed.
                                                                |e. Additional Repair Notes – This is a text box where the user can input additional notes related to the refrigerant or test results. 
                                                                | f. Cancel button- This button returns the user to the Equipment Page.
                                                                |g. Next button – This button sends the user to the ODS Sheet tab 3.

                                                                |Constraints: 
                                                                |a. Leak detected radio button must be selected to enable the Leak repaired or Leak not repaired radio buttons. 
                                                                | b. Pressure Test Performed must be selected as needed to enable data entry into the PSIG Result field.
------------------------------------|--------------------------------------
8. User selects the Leak Test Result.                     | 8.1 If a leak is detected, the user marks the Leak detected radio button.
                                                            | 8.1.1 System enables the Leak repaired / not repaired radio buttons. 
                                                            | 8.1.2 System allows the user to select relevant leak test results.
                                                            |8.1.3 System enables the user to select other test results. | 
8.2 Else, the user marks the No leak detected radio button.| 8.2.1 System allows the user to select other test results.
------------------------------------|--------------------------------------
9. User marks the Pressure test performed checkbox. | 9.1 System enables the PSIG result field for the user to enter the PSIG result.
------------------------------------|--------------------------------------
10. User enters additional details as needed. | 10.1 System allows the user to input Recovery notes as needed.
------------------------------------|--------------------------------------
11. User has the option to cancel or continue to ODS Sheet page 3. | 11.1 Else, the user clicks the Cancel button.


                                                                    |11.1.1 System displays a Warning Modal about returning to the Equipment Page. | 11.1.2 System allows the user to click the X or Back button of the Leave Warning Modal to stay on the current page.
                                                                    |11.1.3 System allows the user to click the Leave button to return to the Equipment Page. | 11.2.1 System validates the entered information.
11.2 If the user wants to proceed to ODS Sheet tab 3, he can click the Next button. | 11.2.2 System displays a trigger warning text for incorrect fields. 
                                                                                    | 11.2.3 System allows the user to edit details.
                                                                                    | 11.2.4 System displays ODS Sheet tab 3-Unpaid.
                                                                                    |The ODS Sheet tab 3 - Unpaid has the following features: 
                                                                                    |a. Access Premium Feature popup message – This feature recommends the user to upgrade membership
------------------------------------|--------------------------------------
15. The user clicks the Review ODS Sheet | 15.1 System sends the user to the ‘Review Recovery ODS Sheet’ page.
                                          | The Review Recovery ODS page has the following features: 
                                          | a. Back button – This button returns the user to the ODS Sheet tab 3. 
                                          | b. Edit button – When clicked, this button changes subheadings into a text field to enable editing. Also, the Edit changes into Save and is required to be clicked to save information to the database.
                                          |c. Cancel – This button returns the user to the Technician Dashboard. 
                                          |d. Submit button- This button sends the user to the ODS Submitted page. However, this button is disabled (if the user clicked the ‘Edit’ button) until the user clicks the Save button. 
--------------------------------------------|------------------------------------- 
16. For each Review Recovery ODS section, the user is able to edit the details entered. |
                                                            |16.1 After the user clicks the Edit button, the system changes the subheading into a text field and simultaneously changes the Edit button to Save button. 
                                                            |16.2 System allows the user to save changes. 
                                                            |16.3 System enables the Submit button once the Save button is clicked. 
--------------------------------------------|------------------------------------- 
17. User has the option to cancel or submit the Recovery ODS sheet. | 17.1 Else, the user can click the Cancel button. 
                                                                    |17.1.1 System displays a Warning Modal about returning to the Equipment Page. 
                                                                    |17.1.2 System allows the user to click the X or Back button of the Leave Warning Modal to stay on the current page. 
                                                                    |17.1.3 System allows the user to click the Leave button to return to the Equipment Page.
17.2 If the user wants to submit the Recovery ODS sheet, they can click the Submit button.  |
                                                      |17.2.1 System validates if all the fields are correct. 
                                                      |17.2.2 System displays a trigger warning text for incorrect fields. 
                                                      |17.2.3 System allows the user to edit and save the details. 
                                                      |17.2.4 If all fields are correct, the system displays the ODS Sheet Submitted page. 
                                                      |17.2.5 If the cylinder needs tag replacement, the system displays the ODS Sheet Submitted page along with a message to replace the tag. 
-------------------------------------------------------|----------------------------------------------------
18. User has the option to replace the faulty cylinder QR tag or not. 
                                                        |18.1 If the user decides to replace the tag, he can click the Replace Tag button (Please refer to the Replace tag activity). 
                                                        |18.1.1 If the QR tag is successfully replaced and the user clicks the Return to Dashboard button, the system displays the Technician Dashboard. 
18.2 Else, the user clicks the Return to Dashboard button. | 18.2.1 The system sends the user back to the Technician Dashboard. 
-----------------------------------------------------------|---------------------------------------------------------



















## Equipment repair form

The "Repair Form" is a web form designed for technicians to document equipment repairs. The form displays auto-populated information, including the equipment tag ID, technician ID, and the repair date (editable, defaulted to the current date). It also provides details such as refrigerant ID, refrigeration type, factory charge amount of refrigerant (lbs), additional amount added (lbs), and the total refrigerant amount in the equipment (automatically calculated as the sum of factory charge and additional amount).

The form further includes fields for the equipment's model number, serial number, and ODS Sheet number. Technicians can enter test results using checkboxes with options such as repaired discharge, line on compressor, leak detected, leak repair, vacuum test performed, leak not repaired, no leak detected, no longer contains refrigerant, and compressor oil removed. Additionally, there's a checkbox labeled "Other," allowing technicians to provide specific details if none of the predefined options fit.

Upon filling out the form, the technician can click the "Submit" button. However, before submitting, the form prompts the technician to enter a unique job number, which helps identify and track the repair.

# Repair Form

## Auto Populated Information

- Equipment Tag ID: EQUIP001
- Technician ID: TECH001
- Repair Date: [Current Date]

- Refrigerant ID: REF001
- Refrigeration Type: [Refrigeration Type]
- Factory Charge Amount Refrigerant (lbs): 50
- Additional Amount Added (lbs): [Enter additional amount]
- Total Refrigerant Amount in Equipment (lbs): [Calculated]

- Model Number: [Enter model number]
- Serial Number: [Enter serial number]
- ODS Sheet Number: [Enter ODS sheet number]

## Test Results

- [ ] Repaired Discharge
- [ ] Line on Compressor
- [ ] Leak Detected
- [ ] Leak Repair
- [ ] Vacuum Test Performed
- [ ] Leak Not Repaired
- [ ] No Leak Detected
- [ ] No Longer Contains Refrigerant
- [ ] Compressor Oil Removed
- [ ] Other: [Enter specific problem]

## Job Number

- Job Number: [Enter job number]


## Equipment Recovery form 

The "Recovery Form" is a web form designed for technicians to document refrigerant recovery processes. The form displays auto-populated information, including the equipment tag ID, technician ID, and the repair date (editable, defaulted to the current date). It also provides details such as refrigerant ID, refrigeration type, factory charge amount of refrigerant (lbs), additional charge amount, and the total charge (automatically calculated as the sum of factory charge and additional amount).

The form further includes fields for the equipment's model number, serial number, and ODS Sheet number. Technicians can enter test results using checkboxes with options such as repaired discharge, line on compressor, leak detected, leak repair, vacuum test performed, leak not repaired, no leak detected, no longer contains refrigerant, and compressor oil removed. Additionally, there's a checkbox labeled "Other," allowing technicians to provide specific details if none of the predefined options fit.

After selecting "Reclaim Gas," the form will display the option to choose "Recovery Cylinder" or use a "Scan Button" to reclaim the cylinder. The form then prompts the technician to enter a unique job number before submission, which helps identify and track the recovery process

# Recovery Form

## Auto Populated Information

- Equipment Tag ID: EQUIP001
- Technician ID: TECH001
- Repair Date: [Current Date]

- Refrigerant ID: REF001
- Refrigeration Type: [Refrigeration Type]
- Factory Charge Refrigerant (lbs): 50
- Additional Charge (lbs): [Enter additional charge]
- Total Charge (lbs): [Calculated]

- Model Number: [Enter model number]
- Serial Number: [Enter serial number]
- ODS Sheet Number: [Enter ODS sheet number]

## Test Results

- [ ] Repaired Discharge
- [ ] Line on Compressor
- [ ] Leak Detected
- [ ] Leak Repair
- [ ] Vacuum Test Performed
- [ ] Leak Not Repaired
- [ ] No Leak Detected
- [ ] No Longer Contains Refrigerant
- [ ] Compressor Oil Removed
- [ ] Other: [Enter specific problem]

## Reclaim Gas

- [ ] Reclaim Gas
  - [ ] Recovery Cylinder
  - [ ] Scan Button

## Job Number

- Job Number: [Enter job number]



