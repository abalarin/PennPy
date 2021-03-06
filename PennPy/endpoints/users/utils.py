from PennPy.models import User, Address


# Check if username or email are already taken
def user_exsists(username, email):
    # Get all Users in SQL
    users = User.query.all()
    for user in users:
        if username == user.username or email == user.email:
            return True

    # No matching user
    return False


def get_addresses(user_id):
    return(Address.query.filter_by(user_id=user_id))
