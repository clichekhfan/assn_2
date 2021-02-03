* meta notes: I already did the steps and just read the need for notes, so I'm doing this from memory.

1. Load the users database.
* this did not work. there was user_selection in place of user_collection pram in
main.load_users() call

1. Add a new user and confirm you get a success message.
* I think this one worked.

1. Try to add the same user ID again and confirm you get an error message.
* i think this worked.

1. Update the name of an existing user.
* i think this worked.

1. Try to update the name of a non-existing user and confirm you get an error message.
* i think this worked.

1. Search for an existing user and return that user's email, name and last name.
* i think this worked.

1. Search for a non-existing user and return a message indicating that the user does not exist.
* i think this was calling the wrong function.

1. Delete an existing user.
* i think this worked

1. Try to delete a non-existing user and confirm you get an error message.
* I think this worked.

1. Save the users database.
* i think this worked.

1. Load the status database.
* i think this worked.

1. Add a new status and confirm you get a success message.
* i think this worked.

1. Try to add the same status ID again and confirm you get an error message.
* I think this worked.

1. Update the text of an existing status ID.
* this one was calling the wrong function and asking for input in the wrong order.

1. Try to update the text of a non-existing status ID and confirm you get an error message.
* i think this worked after fixing previous.

1. Search for an existing status ID and return the ID of the user that created the status and the status text.
* I think this worked

1. Search for a non-existing status ID and return a message indicating that the status ID does not exist.
* I think this called the wrong function.

1. Delete an existing status.
* I think this worked

1. Try to delete a non-existing status and confirm you get an error message.
* I think this worked.

1. Save the status database.
* I think this worked.

1. Make sure menu options are case-insensitive (i.e., typing "a" or "A" works in the same way).
* .upper() was in the comparison but not the dict key assignment
*if user_selection.upper() in menu_options:*
    *menu_options[user_selection.upper()]()*