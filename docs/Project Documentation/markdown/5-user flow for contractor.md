***SRS 2.2.12***

# 2.2.12 Create and Set up account – Contractor Flow 
Use case name:   |   Create and Set up Contractor account
--------------------|-----------------------------------
Scenario: |Create an online REFit account.
-------------------|--------------------------------
Triggering event:  | A new Contractor wants to register a contractor’s account.
-------------------|--------------------------------
Brief description: |User creates a REFIT account online by providing login details, personal information, and company details.
-----------------------------------|--------------------------------
Actors:        | Contractor
-----------------------------------|--------------------------------
Related use cases: | View ODS History
-----------------------------------|--------------------------------
Stakeholders: | Technicians, Contractors, Organization, Wholesaler, Management, and Government
-----------------------------------|--------------------------------
Preconditions:                     |
                                    |The Create and Set up account feature must be available and accessible.
                                    |User email must be provided by the user.
-----------------------------------|--------------------------------
Postconditions:                    |
                                    |REFit contractor account must be created and saved.
                                    |The generated REFit account is associated with the user’s email account. 
------------------------------------|-----------------------------------------------
Flow of activities:                  |
-----------------------------------|------------------------------------
*ACTOR*                           | *SYSTEM*
-----------------------------------|---------------------------------------
1.  User goes to REFit’s login page.|
                                    |1.1 System displays REFit’s Login page. 
                                    |
                                    |The Login module contains the following fields:
                                    |a. Email – This field is a textbox that requires the user to enter the email address.
                                    |b. Password- This field is a textbox that requires the user to enter the password. The entered password is not shown to the user and is encrypted as an asterisk “*”. 
                                    |c. “Forgot Password?” text button – This text button, when clicked, sends the user to the Forgot Password screen.
                                    |d. Submit button – This button, when clicked, validates the entered details. The system shall display a trigger warning text if there are incorrect fields.
                                    |e. “Sign up” text button – This text button sends the user to the Create Account page. 
                                    | 1.2 System shows users with the choice to either log in or sign up for a new account.
------------------------------------|------------------------------------------
2. User clicks the Sign Up text button. |
                                        |2.1 System displays the Create Account page.
                                        |
                                        |The Create Account module shows the following features:
                                        |a. Back button – This button returns the user to previous screen.
                                        |b. Email - This field is a textbox that requires the user to enter the email address.
                                        |c. Password - This field is a textbox that requires the user to enter the password. The entered password is not shown to the user and is encrypted as an asterisk “*”.
                                        |d. Confirm Password -  This field is a textbox that requires the user to re-enter the password for confirmation. The re-entered password is also not shown to the user and is encrypted as an asterisk “*”.
                                        |e.  Submit button – This button sends the user to the Verify Your Email page and sends the verification link to the user’s email address. The verification link expires within 72 hours. 
                                        |f. A consent statement is shown above the Submit button informing the user that by creating an account, they are automatically agreeing with the REFit’s Terms and Conditions and Privacy Policy. Clicking on the hyperlinked Terms and Conditions and Privacy Policy directs the user to the corresponding document.
                                        |
                                        |Constraints: 
                                        |a. User must input correct details on required fields: email address, password, and confirm password.
                                        |b. Email must include “@” and “.” symbols.
                                        |c. Email must have a maximum limit of 320 characters: 64 characters before “@” and 255 after “@” .
                                        |d. Password length must be ≥ 8 characters.
                                        |e. Passwords must match.
---------------------------------------------------|------------------------------------
3. User inputs login details. | 
                              |System allows user to enter login details.
                              |The entered passwords are hidden and shown by the system as “*”.
                              | System allows the user to click the eye-fill icon to unhide the password.
                              | The eye-fill icon changes to eye-slash-fill once the eye-fill icon is clicked.  
---------------------------------------------------|------------------------------------
4. User can click the Terms & Conditions and Privacy Policy of REFit. |
                                        | System shows related documents when the “REFit’s Terms & Conditions” and “Privacy Policy” links are clicked, respectively.
---------------------------------------------------|------------------------------------                                       
5. User has the option to proceed in creating the account or not. | 5.1 If the user agrees with the Terms & Conditions and Privacy Policy, he can click the Submit button.
                                                                |
                                                                |5.1.1  System validates the entered information.
                                                                |5.1.2  System displays a trigger warning text if there are incorrect fields.
                                                                |
                                                                |Possible causes of errors:
                                                                |a. Incorrect email address: email not found, email already exists, or incorrect format
                                                                |b. Password length < 8 characters
                                                                |c. Passwords mismatched
                                                                |
                                                                |5.1.3 System allows the user to edit the login details after a trigger warning text is shown.
                                                                |5.1.4  System displays the Verify Your Email page if all fields are correct.
                                                                |
                                                                |The Verify Your Email screen contains the following fields:
                                                                |a. Back button-  This button returns the user to the Create Account  page.  
                                                                |b. Set Up Account button- This button becomes active once the user clicks the verification link sent to the associated email. If this button is activated and clicked, the user will be directed to Account Setup page where user can select role. Above this button is a message showing that the verification link is sent to the user: “A verification email was sent to user@email.com. Once you click “verify” you’ll be able to proceed with setting up your account.”
                                                                |
                                                                |Constraint:
                                                                |The user must click the Verification link in his email within 72 hours.
                                                                |
                                                                |c. “Didn’t get the email? Send it again” text button – This button sends a new verification link to the user’s email and cancels the old verification link. The page also provides troubleshooting tips to assist the user before they click this button to send a new verification link. 
                                                                |
                                                                |Troubleshooting tips
                                                                |Try: 
                                                                |o	Check if your email address is correct.
                                                                |o	Check your email spam folder.
                                                                |o	Check email filters and adjust them if necessary.
                                                                |o	Ensure that the inbox is not full.
                                                                |o	Wait and refresh the page.
                                                                |o	Ensure that the link is not expired
                                                                |
                                                                |5.1.5 System saves all the entered information.
                                                                |5.1.6 System allows the user to return to the Create Account page to edit the entered details.
                                                                |
5.2 Else, user cannot create an account.                        |5.2.1 System does not permit the user to proceed in creating an account if he does not click the Submit button.
----------------------------------------------------------------|-------------------------------------------------------
6. User checks the verification link in the email. |6.1 If the user receives the verification link, he can click the verification link in the associated email.
                                                   |6.1.1 System displays the Verify Your Email page with the Set Up Account button activated.
6.2 Else, the user clicks “Didn’t get the email? Send it again” text button. 
                                                 |6.2.1 System allows the user to click the “Didn’t get the email? Send it again” text button to send a new verification link to the user’s email.
--------------------------------------------------------------|--------------------------
7. User clicks Set Up Account button on the Verify Your Email page.|
                                                        |7.1 System displays Account Setup – Select your role page.
                                                        |
                                                        |The Account Setup – Select your role page shows the following features:
                                                        |a. Selection cards – The selections cards allow the user to select a role. Only one role should be selected from the options: Technician, Contractor, Organization, and Wholesaler.
                                                        |b. Next button – This button sends the user to the next page.
--------------------------------------------------------|---------------------------------------------
8. User selects the role.                   |
                                            | 8.1 System highlights the role selected.  
                                            | Constraint:
                                            |System must allow only one selection of role at a time.
--------------------------------------------|------------------------------------------------------
9. User clicks the Next button.             |
                                            |9.1 System sends user to Account Setup  page.
                                            |
                                            |The Account Setup – Company Details page displays the following features:
                                            |a. Back button – This button returns the user to Account Setup – Personal Information.
                                            |b. Company Name – This is a text box that allows the user to enter the company name.
                                            |c. Company Branch Number – This is a text box that allows the user to enter the company branch number.
                                            |d. Company Phone Number - This is a text box that allows the user to enter the company phone number.
                                            |e. ODS Sheet Recipient Email – This is a required field that allows the user to enter the ODS Sheet Recipient Email.
                                            |f. Company Address - This is a text box that allows the user to enter the address.
                                            |g. Province - This is a text field that allows the user to enter the province.
                                            |h. Postal Code - This is a text field that allows the user to enter the postal code.
                                            |i. Upload your company logo – This button allows user to upload company logo
                                            |j. Submit button: This button allows the user to submit the account setup information.
                                            |
                                            |Constraints:
                                            |a. Company name must be auto-capitalized and entered without spaces with a maximum of ____ character limit.
                                            |b. Company branch number must contain numeric characters only with a maximum of ____ character limit. Use the mobile keypad in entering the digits. 
                                            |c. Company phone number must contain 10 digits with a total of 14 characters.  Use the mobile keypad in entering the digits. System applies auto-fill formatting: (###) ###-####.
                                            |d. ODS Sheet Recipient Email must be entered. It must include “@” and “.” symbols and have a maximum limit of 320 characters: 64 characters before “@” and 255 after “@” .
                                            |e. Company address, city, province, and postal code must be auto-capitalized when entered with a maximum limit of _____ characters. 
                                            |f. Postal code must contain alphanumeric characters. Auto-fill formatting is applied: A#A #A#.
---------------------------------------------|--------------------------------------------------------------
10. User inputs company details.   | 10.1 System allows the user to enter the company details.
---------------------------------------------|--------------------------------------------------------------
11. User clicks the Submit button.
                                            |11.1 System validates the entered information.
                                            |11.2 System displays trigger warning text for incorrect fields.
                                            |11.3 System saves the entered information.
                                            |11.4 System sends the user to the Contractor Dashboard if the entered information is all correct.
---------------------------------------------|--------------------------------------------------------------
Exception conditions:
1. User has no ODS sheet recipient email.
2. User does not agree with the consent statement.
3. User’s login information is incorrect.
---------------------------------------------|--------------------------------------------------------------














# User Flow for Contractor

## Create a New Account

1. User accesses the account creation page.
2. User provides necessary details to create a new account, such as name, user ID, logo, subscription ID, status, and 2FA code.
3. System validates the information provided.
4. If validation is successful, the contractor account is created.
5. User can now log in to the system.

## Login and Logout

1. User enters their credentials (user ID and password) on the login page.
2. System verifies the credentials.
3. If the credentials are valid, the user is granted access to the system.
4. User performs desired actions within the system.
5. When finished, the user logs out of the system to end the session.

## Offer a Technician to Join the Team

1. User (contractor) accesses the technician management section.
2. User selects the option to invite a new technician.
3. User provides the necessary details for the technician invitation, such as name and email.
4. System sends an invitation email to the technician.
5. Technician receives the invitation and can choose to accept or decline it.
6. If the technician accepts, they are added to the contractor's team.

## Purchase the Tags

1. User (wholesaler) accesses the tag purchase section.
2. User selects the desired quantity and type of tags.
3. User proceeds with the purchase and provides necessary payment details.
4. System processes the payment and generates the tags.
5. User receives the purchased tags.

## Delete the Connection of Technician

1. User (contractor) accesses the technician management section.
2. User selects the technician account to be removed.
3. User confirms the deletion request.
4. System removes the technician's connection from the contractor's team.
5. The technician's historical records are retained, and they can still access their records independently.

## Replace the Invalid QR Tag with a New One

1. User (service person) encounters an invalid QR tag on a refrigeration unit.
2. User accesses the QR tag replacement section.
3. User scans the invalid tag and selects the replacement option.
4. User attaches a new QR tag to the unit.
5. User logs the replacement in the system, associating the new tag with the unit.
