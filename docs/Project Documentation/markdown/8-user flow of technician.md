# User Flow for Technician

# Detailed Description from SRS Document:

## Create and set up account - Technician FLow

-----------------------|-------------------------
Use case name:         |           Create and Set up account
-----------------------|------------------------
Scenario:              |          Create an online REFit account.
-----------------------|---------------------
Triggering event:      |       A new REFit user wants to set up an account online.
-----------------------|------------------------ 
Brief description:     |        User creates a REFIT account online by providing login details ,personal  information, and company details.
-----------------------|--------------------------
Actors:                |        Technician, Contractor, Organization, and Wholesaler
-----------------------|-----------------------
Related use cases:     |       View ODS History
-----------------------|------------------------
Stakeholders:          |Technicians, Contractors, Organization, Wholesaler, Management, and Government
-----------------------|----------------------------
Preconditions:         |- The Create and Set up account feature must be available and accessible.
                       |- An ODS sheet recipient email must be provided by the user.
                       |- An ODS license number must be provided by Technicians.
-----------------------|-----------------------------
Postconditions:        |- REFit account must be created and saved.
                       |- The generated REFit account is associated with the user’s email account. 
-----------------------|-----------------------------

## Flow of activities:  


       **ACTOR**                      |     **SYSTEM**                          
----------------------------------|-------------------------------------
1. User goes to REFIT's login page.| 1.1 System displays REFIT's login page:                           
                                                                   
                                   |     The Login module contains the following fields:
                                   |     Email – This field is a textbox that requires the user to enter the email address.
                                   |     Password- This field is a textbox that requires the user to enter the password. The entered password is not shown to the user and is encrypted  as an asterisk “*”. 
                                   |     “Forgot Password?” text button – This text button, when clicked, sends the user to the Forgot Password screen.
                                   |     Submit button – This button, when clicked, validates the entered details. The system shall display a trigger warning text if there are incorrect fields.
                                   |     “Sign up” text button – This text button sends the user to the Create Account page.  

                                   | 1.2 System shows users with the choice to either log in or sign up for a new account.

----------------------------------|------------------------------------------------
2. User clicks the Sign Up text button. | 2.1 System displays the Create Account page:
                                        |   The Create Account module shows the following features:
                                        |    - Back button – This button returns the user to previous screen.
                                        |    - Email - This field is a textbox that requires the user to enter the email address.
                                        |    - Password - This field is a textbox that requires the user to enter the password. The entered password is not shown to the user and is   encrypted as an asterisk “*”.
                                        |    - Confirm Password -  This field is a textbox that requires the user to re-enter the password for confirmation. The re-entered password is also not shown to the user and is encrypted as an asterisk “*”.
                                        |    - Submit button – This button sends the user to the Verify Your Email page and sends the verification link to the user’s email address. The verification link expires within 72 hours. 
                                         |   - A consent statement is shown above the Submit button informing the user that by creating an account, they are automatically agreeing with the REFit’s Terms and Conditions and Privacy Policy. Clicking on the hyperlinked Terms and Conditions and Privacy Policy directs the user to the corresponding document.

                                         |   Constraints: 
                                         |   - User must input correct details on required fields: email address, password, and confirm password.
                                         |   - Email must include “@” and “.” symbols.
                                         |   - Email must have a maximum limit of 320 characters: 64 characters before “@” and 255 after “@” .
                                         |   - Password length must be ≥ 8 characters.
                                         |   - Passwords must match.
-------------------------------|-------------------------------------------------------
3. User inputs login details.  | System allows user to enter login details.
                               | The entered passwords are hidden and shown by the system as “*”.
                               | System allows the user to click the eye-fill icon to unhide the password.
                               | The eye-fill icon changes to eye-slash-fill once the eye-fill icon is clicked.
-------------------------------|-------------------------------------------------------  
4. User can click the Terms & Conditions and Privacy Policy of REFit.| System shows related documents when the “REFit’s Terms & Conditions” and “Privacy Policy” links are clicked, respectively.
-----------------------------|---------------------------------------------
5. User has the option to proceed in creating the account or not.| 5.1 If the user agrees with the Terms & Conditions and Privacy Policy, he can click the Submit button.
                                                                 | 5.2 Else, user cannot create an account.
                                                                 | 5.1.1  System validates the entered information.
                                                                 | 5.1.2  System displays a trigger warning text if there are incorrect fields.

                                                                 |   *Possible causes of errors:*
                                                                 |   a. Incorrect email address: email not found, email already exists, or incorrect format
                                                                 |   b. Password length < 8 characters
                                                                 |  c. Passwords mismatched

                                                                | 5.1.3 System allows the user to edit the login details after a trigger warning text is shown.
                                                                | 5.1.4  System displays the Verify Your Email page if all fields are correct.

                                                                |    The Verify Your Email screen contains the following fields:
                                                                |    - Back button-  This button returns the user to the Create Account  page.  
                                                                |    - Set Up Account button- This button becomes active once the user clicks the verification link sent to the associated email. If this button is activated and clicked, the user will be directed to Account Setup page where user can select role. Above this button is a message showing that the verification link is sent to the user: “A verification email was sent to user@email.com. Once you click “verify” you’ll be able to proceed with setting up your account.”

                                                                |  Constraint:
                                                                |  The user must click the Verification link in his email within 72 hours.

                                                                | “Didn’t get the email? Send it again” text button – This button sends a new verification link to the user’s email and  cancels the old verification link. The page also provides troubleshooting tips to assist the user before they click this button to send a new verification link. 

                                                                | Troubleshooting tips
                                                                | Try: 
                                                                | o	Check if your email address is correct.
                                                                | o	Check your email spam folder.
                                                                | o	Check email filters and adjust them if necessary.
                                                                | o	Ensure that the inbox is not full.
                                                                | o	Wait and refresh the page.
                                                                | o	Ensure that the link is not expired

                                                                | 5.1.5 System saves all the entered information.
                                                                | 5.1.6 System allows the user to return to the Create Account page to edit the entered details.
                                                                | 5.2.1 System does not permit the user to proceed in creating an account if he does not click the Submit button.
------------------------------------------------------------|--------------------------------------------------
6. User checks the verification link in the email. |  6.1 If the user receives the verification link, he can click the verification link in the associated email.

                                                   | 6.2 Else, the user clicks “Didn’t get the email? Send it again” text button.

                                                    | 6.1.1 System displays the Verify Your Email page with the Set Up Account button activated.




                                                    | 6.2.1 System allows the user to click the “Didn’t get the email? Send it again” text button to send a new verification link to the user’s email.
---------------------------------------------|-------------------------------------------

7. User clicks Set Up Account button on the Verify Your Email page.| 7.1 System displays Account Setup – Select your role page.

                                                                    |The Account Setup – Select your role page shows the following features:
                                                                    |a. Selection cards – The selections cards allow the user to select a role. Only one role should be selected from the options: Technician, Contractor, Organization, and Wholesaler.
                                                                    |b. Next button – This button sends the user to the next page.
-----------------------------------------------|------------------------------------------------------------                                                                    
8. User selects the role.   | 8.1 System highlights the role selected.

                            | Constraint:
                            | System must allow only one selection of role at a time.
-----------------------------|----------------------------------------------------------------

9. User clicks the Next button. | Constraint:
                                |User must select a role before clicking the Next button.
                                |9.1 System displays a trigger warning text if role is not selected.
                                |9.2 System saves the information.
                                |9.3 System displays Account Setup – Personal Information page.
                                |
                                |The Account Setup – Personal Information page contains the following features:
                                |Back button – This button returns the user to the Account Setup – Select your role page.
                                |First Name- This is a textbox that requires the user to enter his first name.
                                |Last Name- This is a textbox that requires the user to enter his last name.
                                |ODS License – This a textbox that requires the user to enter the ODS license.
                                |Next button – This button sends the user to the Account Setup – Company Details page.
                                |
                                |Constraints:
                                |Names must be entered without spaces
                                |First letter of names must be auto-capitalized.
                                |ODS license must have _____ characters.
                                |All details in the required fields must be entered.
                                |
                                |9.4 System allows the user to click the Back button to return to the previous page.
--------------------------------|---------------------------------------------------

10. User inputs all the required personal details.|10.1 System allows the user to his enter personal information.
-------------------------------|---------------------------------------
11. User clicks the Next button.|
                                |11.1 System displays a trigger warning text for incorrect fields.
                                |11.2 System sends user to Account Setup – Company Details page.
                                |
                                |The Account Setup – Company Details page displays the following features:
                                |Back button – This button returns the user to Account Setup – Personal Information.
                                |Company Name – This is a text box that allows the user to enter the company name.
                                |Company Branch Number – This is a text box that allows the user to enter the company branch number.
                                |Company Phone Number - This is a text box that allows the user to enter the company phone number.
                                |ODS Sheet Recipient Email – This is a required field that allows user to enter the ODS Sheet Recipient Email.
                                |Company Address - This is a text box that allows the user to enter the address.
                                |City -  This is a text box that allows the user to enter the city.
                                |Province - This is a text field that allows the user to enter the province.
                                |Postal Code - This is a text field that allows the user to enter the postal code.
                                |Next button – This button sends the user to Technician Dashboard.
                                |
                                |Constraints:
                                |Company name must be auto-capitalized and entered without spaces with a maximum of ____ character limit.
                                |Company branch number must contain numeric characters only with a maximum of ____ character limit. Use the mobile keypad in entering the digits. 
                                |Company phone number must contain 10 digits with a total of 14 characters.  Use the mobile keypad in entering the digits. System applies auto-fill formatting: (###) ###-####.
                                |ODS Sheet Recipient Email must be entered. It must include “@” and “.” symbols and have a maximum limit of 320 characters: 64 characters before “@” and 255 after “@” .
                                |Company address, city, province, and postal code must be auto-capitalized when entered with a maximum limit of _____ characters. 
                                | Postal code must contain alphanumeric characters. Auto-fill formatting is applied: A#A #A#.
--------------------------------|-------------------------------------------
12. User inputs company details. | 12.1 System allows the user to enter the company details.
---------------------------------|------------------------------------------------------
13. User clicks the Submit button.|
                                  |13.1 System validates the entered information.
                                  |13.2 System displays trigger warning text for incorrect fields.
                                  |13.3 System saves the entered information.
                                  |13.4 System sends the user to the Technician Dashboard if the entered information is all correct.
----------------------------------|--------------------------------------
Exception conditions:             |
                                  |1. User has no ODS license.
                                  |2. User has no ODS sheet recipient email.
                                  |3. User does not agree with the consent statement.
                                  |4. User’s login information is incorrect.
                                  |
----------------------------------|--------------------------------------


### previous version of user flow , general overview
## Create a New Account

1. User accesses the account creation page.
2. User provides necessary details to create a new account, such as name, user ID, status, and 2FA code.
3. System validates the information provided.
4. If validation is successful, the Technician account is created.
5. User can now log in to the system.

## Login and Logout

1. User enters their credentials (user ID (email) and password) on the login page.
2. System verifies the credentials.
3. If the credentials are valid, the user is granted access to the system.
4. User performs desired actions within the system.
5. When finished, the user logs out of the system to end the session.

## Make Changes to Account

1. User accesses the account settings page.
2. User views and updates their account information, such as name, email, and password.
3. User can modify their account details as needed.

## Technician Dashbaord
1. User is redirected to dashboard displaying 7 buttons
 -a. Add New QR Tag
 -b. Scan QR Tag
 -c. Repair and ODS
 -d. Recovery and decommission
 -e. View my history
 -f. Delete Qr Tag
 -g. Buy QR tag ( ONLY for paid account)


## Add New QR Tag
1. User scans the NEW QR TAG and is able to enrol it into the system
 (TBC)



## Scan QR Tag
1. User scans the QR code from the scanner in the app
2. Depending on the type of tag (cyl / eqp), user is redirected to respective pages



## Repair and ODS -  Record Repairs and Refills

1. User (Service Person) uses the Refit app to record any repairs or refills performed on equipment.
2. User provides necessary details, such as repair type, quantity of refrigerant refilled, and maintenance notes.
3. The system logs the repair and refill information for the equipment unit.

## Recovery and Decommission -
1. User fills out the ODS sheet for recovery and if its to be decommissioned. User must cut the QR Tag .


##  View History - of Equipment /cylinder Repairs and Refills

1. User (Service Person) accesses the equipment history section.
2. User views the repair and refill history of a specific equipment unit.
3. The system displays details such as repair dates, refill quantities, and maintenance records.

