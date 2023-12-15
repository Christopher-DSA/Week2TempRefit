
***This file Corresponds to Chapter 2.2.2 in SRS***



# 2.2.2 Log into account and Reset password
-----------------------|------------------------------
Use case name:         | Log into account and Reset password
-----------------------|------------------------------
Scenario:              | The user logs in to the REFit account and resets password as needed.
-----------------------|------------------------------
Triggering event:      | The user wants to access his REFit account to update details, track refrigerant status, submit ODS, etc.  
                       | Password resetting happens when the user forgot his password.
-----------------------|------------------------------
Brief description:     | The user enters his login details by providing the associated email and password. 
                       |  For password resetting, a link to reset the password will be sent to the user's email. Clicking on this reset password link takes the user to a page where he  can create a new password.
-----------------------|------------------------------
Actors:                | Technician, Contractor, Organization, and Wholesaler
-----------------------|-------------------------------
Related use cases:     |Scan a QR tag, Add new cylinder, Add a new equipment, Submit ODS, Recovery Equipment ODS, and Access user menu
-----------------------|-------------------------------
Stakeholders:          |Technician, Contractor, Organization, Wholesaler, Management, and Government
-----------------------|--------------------------------
Preconditions:         | 
                       |The Log into account and Reset password modules must be available and accessible.
                       |The user must have a REFit account.
                       |The user must have an email associated with the REFit account.
-----------------------|--------------------------------
Postconditions:        |
                       | The user must be able to log in to his account.
                       | The user must be able to create a new password for password resetting.
-----------------------|---------------------------------
Flow of activities:    |
-----------------------|--------------------------------
Actor                  | System
-----------------------|--------------------------------
1. User goes to REFit’s login page. | 1.1 System displays REFit’s Login page. 

                                    |The Login module contains the following fields:
                                    |a. Email – This field is a textbox that requires the user to enter the email address.
                                    |b. Password- This field is a textbox that requires the user to enter the password. The entered password is not shown to the user and is encrypted as an asterisk “*”. 
                                    |c. “Forgot Password?” text button – This text button, when clicked, sends the user the Forgot Password screen.
                                    |d. Submit button – This button, when clicked, validates the entered details. The system shall display a trigger warning text if there are incorrect fields.
                                    |e. “ Sign up” text button – This text button sends the user to the Create Account page. 
                                    |
                                    |Constraint:
                                    |User must input correct details on the required fields: email address and password.
                                    |
                                    |1.2 System shows an option for users to log in or sign up for a new account.
------------------------------------|------------------------
2. User enters login details.       |
                                    |2.1 System allows user to input login details.
                                    |2.2 The entered password is hidden and shown by the system as “*”.
                                    |2.3 System allows the user to click the eye-fill icon to unhide the password.
                                    |2.4 The eye-fill icon changes to eye-slash-fill once the eye-fill icon is clicked.  
------------------------------------|------------------------
3. User clicks the Submit button.   |
                                    |3.1 System validates the entered information.
                                    |3.2 System displays trigger warning text for incorrect fields.
                                    |3.3 System allows the user to re-enter information for incorrect fields.
                                    |3.4 System allows the user to resubmit login details.
                                    |3.3 System sends the user to the Dashboard if all the entered login details are correct.
------------------------------------|-------------------------
4. User clicks the “Forgot Password?” text button if he wants to reset the password. |


                                                                                    |  4.1 System allows the user to access the Forgot Password? Text button.
                                                                                    |  4.2 System displays the Forgot Password Page.
                                                                                    |  
                                                                                    |  The Forgot Password page shows the following features:
                                                                                    |  Back button – This button allows the user to return to the previous page.
                                                                                    |  Email – This field is a textbox that requires the user to enter the email associated to REFit account.
                                                                                    |  Continue button – This button sends a reset password link to the user’s email.
                                                                                    |  “Sign up” text button – This text button sends the user to the Create Account page.
                                                                                    |  Contact Customer Support text button- This text button sends the user to the Customer Support page.
                                                                                    |  
                                                                                    |  Constraints:
                                                                                    |  User must input the associated email address.
                                                                                    |  Email must include “@” and “.” symbols.
                                                                                    |  Email must have a maximum limit of 320 characters: 64 characters before “@” and 255 after “@” .
------------------------------------------------------------------------------------|----------------------------------------------------------------
5. User inputs the associated email address.                                        | 5.1 System allows the user to enter his email address.
------------------------------------------------------------------------------------|----------------------------------------------------------------
6. User clicks the Continue button.                                                 |
                                                                                    |6.1 System validates the entered email address
                                                                                    |6.2 System displays a trigger warning text if the email address is incorrect.
                                                                                    |6.3 System allows the user to re-enter the email address if the email is invalid.
                                                                                    |6.4 System allows the user to click the Continue again.
                                                                                    |6.5 System sends the reset password link to the associated email if the entered information is correct.
                                                                                    |
                                                                                    |Constraint:
                                                                                    |User must access the reset password in email within 72 hours after clicking the Continue button. 
------------------------------------------------------------------------------------|--------------------------------------------------------------------
7. User checks the reset password link in the email.                                |

                                                                                    |7.1 If the user receives the reset password link, he can click the reset password link in the associated email.
                                                                                    |7.2 Else, the user can do implement troubleshooting tips.
                                                                                    |7.1.1 System displays the Reset Password page.
                                                                                    |The Reset Password page contains the following fields:
                                                                                    |New Password – This is a required field that allows the user to enter a new password. The entered password is not shown to the user and is encrypted as an asterisk “*”.
                                                                                    |Confirm New Password – This is a required field that allows the user to re-enter the new password for confirmation. Likewise, the re-entered password is not shown to the user and is encrypted as an asterisk “*”.
                                                                                    |Submit button – This button sends the user to the Reset Successful page.
                                                                                    |7.2.1 In the Forgot Password page, a troubleshooting guide may be included to assist the user in receiving the reset password link. 
                                                                                    |Troubleshooting tips
                                                                                    |Try: 
                                                                                    |o	Check if your email address is correct.
                                                                                    |o	Check your email spam folder.
                                                                                    |o	Check email filters and adjust them if necessary.
                                                                                    |o	Ensure that the inbox is not full.
                                                                                    |o	Wait and refresh the page.
                                                                                    |o	Ensure that the link is not expired
                                                                                    |
                                                                                    |7.2.2 System allows the user to click the Continue again.
                                                                                    |7.2.3 If the user successfully receives the reset password link after implementing the troubleshooting tips, he can click the reset password link to direct him to the Reset Password page.
                                                                                    |7.2.4 If the user still does not received the reset password link after implementing the troubleshooting tips, he can click the Customer Support text button (Please refer to the Contact customer support activity).
------------------------------------------------------------------------------------|----------------------------------------------------------------
8. User enters new password twice.                                                  |
                                                                                    |8.1. System allows the user to enter a new password twice.
                                                                                    |8.2 The entered password is hidden and shown by the system as “*”.
                                                                                    |8.3 System allows the user to click the eye-fill icon to unhide the password.
                                                                                    |8.4 The eye-fill icon changes to eye-slash-fill once the eye-fill icon is clicked.  
                                                                                    |
                                                                                    |Constraints:
                                                                                    |Password length must be ≥ 8 characters.
                                                                                    |Passwords must match.
------------------------------------------------------------------------------------|-------------------------------------------------------------
9. User clicks the Submit button.                                                   |
                                                                                    |9.1 System validates the new password.
                                                                                    |9.2 System displays a trigger warning text if the password is invalid.
                                                                                    |
                                                                                    |Possible causes of errors:
                                                                                    |a. Required information is incomplete
                                                                                    |b. Password length < 8 characters
                                                                                    |c. Passwords mismatched
                                                                                    |
                                                                                    |9.3 System allows the user to re-enter a new password twice if the password is invalid.
                                                                                    |9.4  System sends the user to the Reset Successful page if the new password is valid.
------------------------------------------------------------------------------------|----------------------------------------------------------------
10. User clicks the Proceed to Log in button.                                       |
                                                                                    |10.1 System displays the Dashboard.
                                                                                    |
                                                                                    |
                                                                                    |
                                                                                    |
                                                                                    |Exception conditions:
                                                                                    |1. User’s login information is incorrect.
                                                                                    |2. User forgot the email associated with the REFit account.
------------------------------------------------------------------------------------|----------------------------------------------------------------

