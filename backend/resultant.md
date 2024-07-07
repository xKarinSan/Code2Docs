
# BlockUser and User Models

The first code snippet imports the BlockUser and User models.

# checkIfBlocked Function

The second code snippet creates an asynchronous function called checkIfBlocked that takes in two parameters: blocker_user_email and blocked_user_email. Within the function, it queries the BlockUser model to check if the blocker_user_email is blocked by the blocked_user_email. If either the blocker or blocked user is not found, it returns false.

# BlockUser and User Models

The third code snippet contains two functions: checkIfBlocked and blockUser. The checkIfBlocked function takes in three parameters: isAlreadyBlocked, blockingUser, and blockedUser. It first checks if any of these parameters are false, and if so, it returns false. Otherwise, it uses the BlockUser model to create a new entry with the blocker_id and blocked_id set to the corresponding user ids. Finally, it returns true if the creation is successful, or false if there is an error.

The blockUser function also takes in three parameters: blockingUser, blockedUser, and BlockUser. It first calls the checkIfBlocked function with the same parameters. If the function returns false, it means that the user is already blocked or one of the users is invalid, so