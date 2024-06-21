from flask import Blueprint, request

from .data.search_data import USERS


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200


def search_users(args):
    """Search users database

    Parameters:
        args: a dictionary containing the following search parameters:
            id: string
            name: string
            age: string
            occupation: string

    Returns:
        a list of users that match the search parameters
    """

    # Implement search here!

    id_param = args.get("id")
    name_param = args.get("name", "").lower()
    age_param = args.get("age")
    occupation_param = args.get("occupation", "").lower()

    matched_users = []

    for user in USERS:
        # ID Match Check
        if id_param and user["id"] == id_param:
            matched_users.append(user)
            continue

        # Name Match Check
        if name_param and name_param in user["name"].lower():
            matched_users.append(user)
            continue

        # Age Match Check
        if age_param:
            age = int(age_param)
            if age - 1 <= user["age"] <= age + 1:
                matched_users.append(user)
                continue

        # Occupation Match Check
        if occupation_param and occupation_param in user["occupation"].lower():
            matched_users.append(user)
            continue

    # Remove duplicates and sort based on priority(i.e bonus points)
    seen_ids = set()
    unique_users = []
    for user in matched_users:
        if user["id"] not in seen_ids:
            seen_ids.add(user["id"])
            unique_users.append(user)

    def sort_key(user):
        id_score = 0 if id_param and user["id"] == id_param else 1
        name_score = 0 if name_param and name_param in user["name"].lower() else 1
        age_score = 0 if age_param and (age - 1 <= user["age"] <= age + 1) else 1
        occupation_score = 0 if occupation_param and occupation_param in user["occupation"].lower() else 1
        return (id_score, name_score, age_score, occupation_score)

    unique_users.sort(key=sort_key)
    return unique_users
