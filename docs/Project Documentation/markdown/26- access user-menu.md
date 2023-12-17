
***SRS 2.2.11***

# 2.2.11 Access user menu   
Use case name:   | Access user menu 
-----------------|--------------------------
Scenario:        |The user explores the user menu.
-----------------|--------------------------
Triggering event: |
                 |The user needs to update account details such as email address, phone number, and password. 
                 |The user needs to upgrade membership.
                 |The user needs to view the privacy policy.
-----------------|--------------------------
Brief description: | The user explores the user menu by clicking the menu icon that shows a drop-down menu with various options.
-----------------|--------------------------
Actors:          | Technician and Contractor
-----------------|--------------------------
Related use cases: | Enter login details, Scan QR Tag, Replace QR Tag, Submit ODS, Recover and Decommission, etc.
-----------------|--------------------------
Stakeholders:    |Technician, Contractor, Organization, Wholesaler, Management, Government
-----------------|--------------------------
Preconditions:   |
                 |The user must have a REFit account.
                 |The user must log into his REFit account.
-----------------|--------------------------
Postconditions:  | The user menu must be accessible and available to the user.
-----------------|--------------------------
Flow of activities: |
-----------------|--------------------------
*ACTOR*          | *SYSTEM*
-----------------|--------------------------
1. User logs into the REFit account (Refer to the Log into account and Reset Password activity).|1.1 System displays the Technician or Contractor Dashboard.
-----------------|--------------------------
2. User clicks the User menu.|
                            |2.1 The system displays the Settings menu with the following options:
                            |a. Edit Profile – This feature allows the users to upload a photo and edit their information such as Name, ODS Certification, and Address.
                            |b. Account – This feature helps the users update their email address, change their phone number, change their password, and seek customer assistance.
                            |c. Membership – This feature allows the users to upgrade their membership from Technician to Contractor or vice-versa. 
                            |d. Privacy Policy- This allows the user to view and read the privacy policy of the company.
-----------------|--------------------------
3. User clicks the Edit Profile. |
                                |3.1 System displays the Edit Profile page where the user can upload a profile picture and edit personal details.
                                |
                                |Upload photo options:
                                |a. Gallery – This allows the user to select a photo from the gallery.
                                |b. Camera – This allows the user to take a photo using the phone camera.
-----------------|--------------------------
4. User has the option to upload a photo. | 4.1 If the user selects a photo from the gallery icon, then he can click the Gallery icon.
                                          |4.1.1 System displays the Gallery.
                                          |4.1.2 System displays the photo selected by the user.
                                          |4.1.3 If the photo is okay with the user, the system updates the user’s profile picture. Otherwise, the user can cancel and select another photo.
                                          |4.1.4 The user can click the Back button to return to the Edit Profile page if he decides not to upload a photo.
4.2 If the user wants to take a photo, click the Camera icon. |
                                                              |4.2.1  System displays the camera and allows the user to capture a photo.
                                                             |4.2.2 System displays the photo taken by the user
                                                             |4.2.3 If the photo is okay with the user, the system updates the user’s profile picture. Otherwise, the user can click Retry to take another photo.
                                                             |4.2.4 The user can click the Back button to return to the Edit Profile page if he decides not to upload a photo.
4.3 Else, the user can proceed in editing his personal details. |4.3.1 System allows the user to edit his details.
---------------------------------------------------------------|----------------------------------------------
5. User has the option to edit his information details. | 5.1 If the user needs to edit his details, he can update his information and click the Update button.
                                                        |5.1.1 System allows the user to update his details.
                                                        |5.1.2 System validates if all the fields are correct.
                                                        |5.1.3 System displays a trigger warning text if there are incorrect fields.
                                                        |5.1.4 System allows the user to re-enter his details for the incorrect fields.
                                                        |5.1.5 System displays a confirmation message to the user if the details are already updated.
                                                        |5.1.6 System saves the information and disables the Update button once all information is updated.
5.2 Else, the user can click Back to return to the Settings menu. |5.2.1 System displays a Warning modal for unsaved changes.
                                                                |5.2.2 If the user wants to leave the current page, he can click the Discard Changes button and return to the Settings menu.
                                                                |5.2.3 Otherwise, the user can click the Cancel button to return the user to the Edit Profile page.
--------------------------------------------------------------|------------------------------------------------
6. User clicks the Account menu.                              |
                                                              |6.1.2 System displays the Account menu options:
                                                              |a. Email Address – This feature helps the user to update the email address.
                                                              |b. Change Phone – This feature allows the user to change his phone number.
                                                              |c. Change Password – this feature allows the user to change his password.
                                                              |d. Contact Us – This feature helps the user to communicate with the customer support team.
  -----------------------------------------------------------|------------------------------------------ 
7. User clicks the Email Address feature and has the option to update his email address. |
                                                            | 7.1 If the user needs an update, he enters his new email address into the email address text field.
                                                            |7.1.1 System displays the Email address page.
                                                            |7.1.2 System validates the email provided by the user.
                                                            |7.1.3 System displays a trigger warning text for the incorrect fields.
                                                            |7.1.4 System allows the user to re-enter the new email address if incorrect.
                                                            |7.1.5 System displays a confirmation message that the mail address has been updated.
                                                            |7.1.6 System disables the Update button once the email address is updated.
                                                            |Constraints: 
                                                            |a. Email must include “@” and “.” symbols.
                                                            |b. Email must have a maximum limit of 320 characters: 64 characters before “@” and 255 after “@” .
7.2 Else, the user clicks the Back button to return to the Account page. | 7.2.1 System returns the user to the Account page.
------------------------------------------------------------|----------------------------------------------------
8. User clicks the Change Phone Number feature and has the option to update his phone number.
                                                                            | 8.1 If the user wants to  update his phone number, he can select the country code, enter his new number, and click the Save button.
                                                                            |8.1.1 System displays the Change Phone Number Feature.
                                                                            |8.1.2 System displays the list of country codes.
                                                                            |8.1.3 System allows the user to select the country code.
                                                                            |8.1.4 System displays the selected country code of the user.
                                                                            |8.1.5 System validates the new number entered by the user.
                                                                            |8.1.6 System displays a trigger warning text for the incorrect fields.
                                                                            |8.1.7 System allows the user to edit the fields that are incorrect.
                                                                            |8.1.8 System displays a confirmation message that the phone number has been updated.
                                                                            |8.1.9 System disables the Update button once the phone number is updated.
8.2 Else, the user can click the Back button.                               | 8.2.1 System returns the user to the Account page.
---------------------------------------------------------------------------|------------------------------------------------------
9. User clicks the Change Password feature and has the option to update the password.|
                                                                                     | 9.1 If the user needs to update his password, he can enter the current password, enter the new password twice, and click the Save button.
                                                                                     |9.1.1 System displays the Change Password Feature.
                                                                                     |9.1.2 System allows the user to enter the current password.
                                                                                     |9.1.3 System allows the user to enter the new password.
                                                                                     |9.1.4 System allows the user to re-enter the new password for confirmation.
                                                                                     |9.1.5 System validates the new password entered by the user.
                                                                                     |9.1.6 System displays a trigger warning text for the incorrect fields.
                                                                                     |9.1.7 System allows the user to edit the fields that are incorrect.
                                                                                     |9.1.8 System displays a confirmation message that the password has been changed.
                                                                                     |9.1.9 System disables the Save button once the password is updated.
                                                                                     |Constraints: 
                                                                                     |a. Password length must be ≥ 8 characters.
                                                                                     |b. Passwords must match.
9.2 Else, the user can click the Back button.                                        | 9.2.1 System returns the user to the Account page.
------------------------------------------------------------------------------------|------------------------------------------------------
10. User clicks the Contact Us page. | 10.1 System sends the user to an external link that manages customer concerns (Refer to the Contact customer support activity).
------------------------------------------------------------------------------------|------------------------------------------------------
11. User clicks the Membership feature. | 11.1 System displays the Contractor or Technician Membership page.
------------------------------------------------------------------------------------|------------------------------------------------------
12. The Contractor has the option to unlock the Technician features. | 
                                                                    |12.1 If the Contractor wants to unlock the Technician features, he can click the Unlock Technician Features button, enter the ODS license number, and click the Save button.
                                                                    |12.1.1 System displays the Unlock Technician Features page.
                                                                    |12.1.2 System allows the user to input the ODS license into the ODS license text field.
                                                                    |12.1.3 System validates the entered ODS license number.
                                                                    |12.1.4 System displays a trigger warning text if the ODS license number is incorrect. 
                                                                    |12.1.5 System allows the user to re-enter his ODS license number if incorrect.
                                                                    |12.1.6 If the entered ODS license number is correct, the system displays a confirmation message that the Technician features are unlocked.
                                                                    |12.1.7 Systems saves the ODS license number and disables the Save button.
12.2 Else, the user clicks the Back button to return to the Settings menu. |12.2.1 System allows the user to click the Back button to return to the Contractor Membership page.
------------------------------------------------------------------------|-----------------------------------------------
13. The Technician has the option to upgrade his membership to Contractor. | 13.1 The system allows the user to click the Upgrade button. 
                                                                         | 13.2 Else the user can click the Back button to return to the Settings menu.
                                                                        | 13.2.1 System returns the user to the Settings menu.
------------------------------------------------------------------------|-----------------------------------------------
14. User displays the Privacy Policy.                                   |
                                                                        |14.1 System displays the Privacy Policy.
                                                                        |14.2 System allows the user to read the Privacy Policy.
                                                                        |14.3 System allows the user to click the Back button to return to the Settings menu. 
------------------------------------------------------------------------|--------------------------------------------------
Exception conditions:
1. There is an internet connectivity issue.
2. There are downtime or server issues.
3. The user is unfamiliar with navigating the application.
----------------------------------------------------------------------|---------------------------------------------------------------------
