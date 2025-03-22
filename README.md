# Snowrunner Custom Colours

Simple editor for Snowrunner Custom Colours. Displays a spreadsheet like display with the colour ID, Tint1, Tint2, Tint3 as background colours and then as text. The text can be updated to change the colour and will accept any entry supported by the python wx.Colour class. The background colour columns can be clicked on to open the Color Dialog. The ID's can be edited. The snowrunner developers start with 100 as the first and create sequentially. It works with all three tints for the version of Snowrunner 34.2 even though the game editor for this version does not support all three tints.

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



