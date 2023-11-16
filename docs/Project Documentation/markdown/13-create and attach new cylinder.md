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


