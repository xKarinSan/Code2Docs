
# BlockUser and User Models

The first two lines of code import the BlockUser and User models from their respective files. The next line defines a function called checkIfBlocked that takes in two parameters: blocker_user_email and blocked_user_email. The function is asynchronous, meaning it will run in the background while the rest of the code continues to execute. 

The next few lines are comments that describe what the function does. It checks if the blocker_user_email is blocked by the blocked_user_email. This is done by querying the Blocked table. The function then returns either true or false, depending on the result of the query.

The next two lines use the User model to find a user with the specified email for both the blocker and blocked user. If either of these users cannot be found, the function returns false.

Finally, there is an if statement that checks if either the blocker or blocked user is not found. If this is the case, the function returns false. 

# Functions

## checkIfBlocked

The `checkIfBlocked` function takes in two parameters, `blockingUser` and `blockedUser`, and checks if the `isAlreadyBlocked` variable is true or if either of the user parameters are false. If any of these conditions are met,