import json

def delete_movies():
    str_empty= ''

    # empty json file
    with open('movies.json', 'w') as f:
        json.dump(str_empty, f, indent=0)

delete_movies()