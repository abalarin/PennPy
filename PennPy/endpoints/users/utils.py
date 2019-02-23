from PennPy.models import Users


# Check if username or email are already taken
def user_exsists(username, email):
    # Get all Users in SQL
    users = Users.query.all()
    for user in users:
        if username == user.username or email == user.email:
            return True

    # No matching user
    return False
