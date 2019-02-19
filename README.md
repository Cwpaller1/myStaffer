# myStaffer
myStaffer project start. 

TODO's
ChooseFile Page
#1: File Page needs to detect column headers of the file and import based on that. 

#2: File Page is taking in the first row which is the column headers...that needs to stop. 

EditPerson Page
#1: Change title of page to EditPerson

#2: When a Result Button is pressed, have the SearchPage create a new instance of EditButton. 

#3: use .raise function to raise proper button if someone clicks on a new Result Button. 

#3: Destroy the EditButton when a new search is done (in the 'submit_search' function on the SearchPage)

#3: Finish the GUI for the EditPerson Page

#4: When the 'submit edit' button is pressed, change the variables in the person object.

***NEW***
CampaignFinance Page
#1: Create a new page called 'Campaign Finance'. Add it to StartPage.

#2: CampaignFinance Page is going to have two options: 'Add New Contribution' and 'Add New Expenditure'

AddNewContribution Page
#1: Create a new page called 'Add New Contribution' and add it to CampaignFinance Page

#2: Create a new class object called 'Contribution'. Must have a 'Contribution ID #', 'Contributor', 'Date', 'How it was recieved' and 'Amount'.

#3: Create GUI for user to add these variables in. 

#4: Take variables the user added and assign them to an instance of a Contribution object. 

#5: Add a Contributions list variable into our Person object. 

#6: Take that Contribution and add it into the right Contributor's object in list_of_people. 

AddNewExpenditure Page
#1: Create a new page called 'AddNewExpenditure' and add it to the CampaignFinance Page

#2: Create a new class object and call it 'Expenditure'. Must have an 'Expenditure ID #', 'Recipient of Expenditure', 'Date', 'Amount', 'address of recipient', 'service' and 'how they were paid'.

#3: Create GUI for user to add these variables in. 

#4: Take variables the user added and assign them to an instance of an Expenditure object. 

#5: Create a new class object and call it 'ExpenseRecipient'. Must have a 'first', 'last', 'business', 'address', 'service'. 

#6: Create a global list of 'ExpenseRecipient' objects. 

#7: Create a global list of 'Expenditure' objects. 

#8: Use Expenditure object to retrieve or create a new ExpenseRecipient. 

#9: Attach new instances of both variables to their respective global lists. 
