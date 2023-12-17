*** Coressponds to CHapter 2.2.4 in SRS Replace QR tag***
### Note : maybe more cohesive if combine this in chapter 19 in mdwn , scan QR code -yael

# 2.2.4 Replace QR tag

Use case name:        |       Replace QR Tag
----------------------|------------------------
Scenario:             | The technician wants to replace a faulty cylinder or equipment QR tag.
----------------------|----------------------------
Triggering event:     |The QR code is unreadable by the QR scanner or not existing even if manually encoded.
----------------------|----------------------------
Brief description:    |The technician replaces the faulty QR tag by successfully scanning a new and readable QR tag. 
----------------------|----------------------------
Actors:               |Technician
----------------------|----------------------------
Related use cases:    |Scan QR Tag, Add new cylinder, Add new equipment, Equipment recovery, Submit ODS, etc.
----------------------|----------------------------
Stakeholders:         |Technician, Contractor, Organization, Wholesaler, Management, and Government
----------------------|----------------------------
Preconditions:        |The technician must be logged in successfully into the REFit  application.
----------------------|----------------------------
Postconditions:       |The faulty QR tag must be replaced successfully with a new and readable QR tag.
----------------------|----------------------------
Flow of activities:
----------------------|----------------------------
Actor                 |System
----------------------|----------------------------
1. User successfully logs into the REFit account (Please refer to the Log into account and Reset password activity).| 1.1 System displays the Technician Dashboard.
-----------------------------------------------------------------------|----------------------------
2. User scans the QR tag (Please refer to Scan QR tag activity).|2.1 If the QR tag is manually encoded and needs replacement, the system displays Replace QR Tag page.
----------------------------------------------------------------|----------------------------
3. User clicks the Scan New Tag button.                         | 3.1 System displays the QR scanner.
----------------------------------------------------------------|----------------------------
4. User scans the new QR code.                                  |
                                                                |4.1 System displays an animated check mark along with a message, “QR code successfully scanned.” 
                                                                |
                                                                |Constraint: A new and readable tag must be used to replace the tag.
                                                                |
                                                                | 4.2 System displays the Confirm Raplace Tag modal.
----------------------------------------------------------------|--------------------------------
5. User has the option to confirm the tag replacement  or return to the Technician Dashboard. |5.1 If the user wants to confirm the tag replacement, he can click the Confirm button.
                                                                                         
                |
                                                                                              |5.1.1 System displays a message “Your tag has been replaced.”
                                                                                              |5.1.2 If the user clicks the Continue button, the system directs him to the Cylinder / Equipment page.
                                                                                              |
                                                                                              |
5.2 Else, the user can click the Cancel button to return to the Dashboard.                    |5.2.1 System displays a Warning Modal about returning to the Technician Dashboard. 
                                                                                              |5.2.2 System allows the user to click the X or Back button of the Leave Warning Modal to stay on the current page.
                                                                                              |5.2.3 In the Leave Warning Modal, the system allows the user to click the Leave button to return to the Technician Dashboard.
                                                                                              |Exception conditions:
                                                                                              |1. The new QR code is unreadable.
                                                                                              |2. The original QR tag attached to the cylinder/equipment is missing.
                                                                                              |
                                                                                              |
                                                                                              |
 ---------------------------------------------------------------------------------------------|--------------------------------------------------