# Snowrunner Custom Colours

Simple editor for Snowrunner Custom Colours. Displays a spreadsheet like display with the colour ID, Tint1, Tint2, Tint3 as background colours and then as text. The text can be updated to change the colour and will accept any entry supported by the python wx.Colour class. The background colour columns can be clicked on to open the Color Dialog. The ID's can be edited. The snowrunner developers start with 100 as the first and create sequentially.
![Screenshot 2025-03-30 110939](https://github.com/user-attachments/assets/4917fc2e-d5ff-4ade-ace5-30b5f4187e42)

## File Menu

### Open
Open a Snowrunner save file. Wild card for files that start with CompleteSave.

### Save
Save edited colours to open save file

### Save As
Save edited colours to new or existing save file. It will only save the CustomColors attribute and will not affect save progress. This allows coping colours from one save file to another so your company colours can be used in multiple slots.

### About
About.

### Exit
Exit.

## Row Menu

### Add
Add a new colour. It will pick first availabe ID number starting at 100. It will use the current cursor row tints to create the new colour which is a way to copy colours. If the save has no colours it will add one using the same default solid colour as Snowrunner.

### Delete
Delete the current cursor row. Gives you an "are you sure" dialog.

### Sort
Sort the colours by ID.

### Renumber
Renumbers the colours starting at 100 to look more like Snowrunner created ones.

### CSS/HTML
Toggles the text colour columns between CSS "rgb(15, 101, 192)" and HTML "#OF65C0"

### Combinations
It will take the current row and generate all 27 color combinations for the 3 colors. It will deleted the current row as it is duplicated in the combination. If the current row has less than three colors it will still generate all 27 combinations creating duplicates.

## Font Menu

### Size +
Make font larger.

### Size -
Make font smaller.


## Example Colours
![Screenshot 2025-03-21 233412](https://github.com/user-attachments/assets/ce28ca77-b969-45fb-a2f9-a7c562c1f11e)



