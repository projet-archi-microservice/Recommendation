import numpy as np
import pandas as pd
import pickle
import json

from pandas import json_normalize
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def get_best_movies():
    """
    Cette fonction lit le fichier 'movies.json', trie les films en fonction de leur note décroissante 
    et renvoie les informations des trois meilleurs films en JSON.
    
    Returns:
        JSON: un dictionnaire contenant les informations des trois meilleurs films triés par note décroissante.
    """
    
    # On lit le fichier 'movies.json' avec Pandas et on trie les films par note décroissante.
    df = pd.read_json('movies.json')
    df = df.sort_values(by='vote_average', ascending=False)
    
    # On crée une liste pour stocker les informations des trois meilleurs films.
    best_movies = []
    
    # On parcourt les trois meilleurs films et on ajoute les informations dans la liste 'best_movies'.
    for i in range(3):
        genres = [{'id': genre_ids} for genre_ids in df.iloc[i]['genre_ids']]
        movie = {'title': df.iloc[i]['title'],
                 'genre_ids': genres,
                 'vote_average': df.iloc[i]['vote_average']}
        best_movies.append(movie)
    
    # On retourne les informations des trois meilleurs films en JSON.
    print(df.iloc[0])
    return best_movies





def get_model(df):
    
    """this function gets the prediction model and the data divided in both train and test data
    
    Args: 
        df (dataframe): movies.json
    
    Returns:
        model: prediction model
        x_train: features of training (movie criterias)
        x_test: features of test data
        y_train: features of training (scores)
        y_test: features of test data
    """
    
    # Convert the JSON file into a pandas dataframe
    df = pd.DataFrame(df)
    
    # Normalize the genres column and drop unnecessary columns
    df = pd.json_normalize(df, record_path='genres', meta=['adult', 'name', 'poster_path', 'note'])
    df = df.drop(columns=['adult', 'poster_path'])
    
    # Group the dataframe by movie name and score, and aggregate the genres column into a list
    df = df.groupby(['name', 'note'])['id'].apply(list).reset_index(name='genres')
    
    # Sort the dataframe by score and reset the index
    df = df.sort_values(by='note', ascending=False)
    df = df.reset_index(drop=True)

    # Split the genres list into separate columns and drop the 'id' column
    features = pd.concat([df.drop(['note', 'genres'], axis=1), pd.json_normalize(df['genres'])], axis=1)
    features = features.drop(columns=['id'])

    # Split the data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(features, df['note'], test_size=0.2, random_state=40)
    
    # Create a regression model using Random Forest
    model = RandomForestClassifier(random_state=1)
    
    return model, x_train, x_test, y_train, y_test




def train_model(model, x_train, y_train):   

    """trains the model thanks to the train data
    
    Args:
        model (RandomForestClassifier): current model that will be trained
    
    Returns:
        model (RandomForestClassifier) : model that was trained
    """

    model.fit(x_train, y_train)
    return(model)


def predict_rating(new_movie, model):
    """
    Predicts the movie's rating using the given model. Useful to predict scores for movies that the user has not seen before.

    Args:
        new_movie (dict): Dictionary containing the movie's data.
        model (RandomForestRegressor): Model used to predict the rating.

    Returns:
        predicted_rating (float): The movie's predicted rating.
    """
    
    # Create a DataFrame with the new movie data
    new = pd.json_normalize(new_movie, record_path='genres', meta=['adult', 'name', 'poster_path'])
    new = new.drop(columns=['adult', 'poster_path'])
    new = new.groupby(['name'])['id'].apply(list).reset_index(name='genres')
    new = pd.concat([new.drop(['genres'], axis=1), pd.json_normalize(new['genres'])], axis=1)
    new = new.drop(columns=['id'])
    
    # Predict the rating using the model
    predicted_rating = model.predict(new)[0]
    
    return predicted_rating



def description(model, x_test, y_test):
    
    """ gets the model description: parameters, lenght of train data, the classification report and the accuracy of the model based on test data

    Args:
        model (RandomForestClassifier): current model
        x_test (dataframe): features of test data
        y_test (dataframe): features of test data

    Returns:
        params (dict): model parameters
        accuracy (float) : model accuracy
    """
    
    y_pred = model.predict(x_test)
    support_test = classification_report(y_test,y_pred,output_dict=True)['macro avg']['support']

    params = model.get_params()
    support_train = support_test * 0.8 / 0.2
    report = classification_report(y_test,y_pred)
    accuracy = accuracy_score(y_test,y_pred)
    
    return params, accuracy


def add_to_df(df, new_row):
    """
    This function adds a new movie entry to the movies dataframe.

    Args:
        df (dataframe): movies dataframe.
        new_row (dict): new movie entry.

    Returns:
        None
    """
    
    last_row = df.tail(1)
    new_id = int(last_row.iloc[0]['id']) + 1
    new_row['id'] = new_id
    
    with open('movies.json', 'r') as f:
        data = json.load(f)
    
    data.append(new_row)

    with open('movies.json', 'w') as f:
        json.dump(data, f)


#save model in model.pkl
def pickle_model(model):
    
    """serialise the model into a pickle file
    
    Args:
        model (RandomForestClassifier): last trained model
        
    Returns:
        pickle file modified with the last trained model
    """
    
    pickle.dump(model, open('model.pkl', 'wb'))