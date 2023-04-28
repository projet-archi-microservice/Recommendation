import numpy as np
import pandas as pd
import pickle
import json

from pandas import json_normalize
from csv import writer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def get_best_wine():
    
    """this function returns the best wine possible in the given dataset

    Returns:
        best_wine (dict): wine criterias that can be used to determine its quality.
    """
    
    df = pd.read_csv("Wines.csv")
    df = df.sort_values(by = 'quality', ascending=False)

    best_wine = {'fixedAcidity' : df.iloc[0][0],
        'volatileAcidity' : df.iloc[0][1],
        'citricAcid' : df.iloc[0][2],
        'residualSugar' : df.iloc[0][3],
        'chlorides' : df.iloc[0][4],
        'freeSulfurDioxide' : df.iloc[0][5],
        'totalSulfurDioxide' : df.iloc[0][6],
        'density' : df.iloc[0][7],
        'pH' : df.iloc[0][8],
        'sulphates' : df.iloc[0][9],
        'alcohol' : df.iloc[0][10]}

    return best_wine

def get_best_movies(n=3):
    
    """
    Cette fonction lit le fichier 'movies.json', trie les films en fonction de leur note décroissante 
    et renvoie un dictionnaire contenant les informations des n premiers films (5 par défaut).
    
    Args:
        n (int): nombre de films à renvoyer (5 par défaut).
    
    Returns:
        List[Dict]: une liste contenant les informations des n premiers films triés par note décroissante.
    """
    
    # On lit le fichier 'movies.json' avec Pandas et on trie les films par note décroissante.
    df = pd.read_json('movies.json')
    df = df.sort_values(by='score', ascending=False)
    
    # On crée une liste pour stocker les informations des n premiers films.
    best_movies = []
    
    # On parcourt les n premiers films et on ajoute les informations dans la liste 'best_movies'.
    for i in range(n):
        movie = {'adult': df.iloc[i]['adult'],
                 'name': df.iloc[i]['name'],
                 'genres': df.iloc[i]['genres'],
                 'poster_path': df.iloc[i]['poster_path'],
                 'score': df.iloc[i]['score']}
        best_movies.append(movie)
    
    # On renvoie la liste 'best_movies'.
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
    model = RandomForestRegressor(random_state=1)
    
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


def predict_quality(new_wine,model):
    
    """predicts the wine's quality thanks to the model
    
    Args:
        new_wine (Wine): new wine, wich we want to rate
        model (RandomForestClassifier) : model used to predict the quality

    Returns:
        model.predict(new)[0] (int): the wine's quality (from 3 to 8 because of the data set, but could be different if we add more data)
    """
    
    new = pd.DataFrame(new_wine, index=[0])
    return int(model.predict(new)[0])


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


def add_to_df(df,new_row):
    
    """adds a new entry (wine) to the csv
    
    Args:
        df (dataframe): Wines.csv
        new_row (dataframe): new wine entry
    """
    
    last_row = df.tail(1)
    new_id = int(last_row.iloc[0][12]+1)
    new_line = [new_row['fixedAcidity'],new_row['volatileAcidity'],new_row['citricAcid'],new_row['residualSugar'],
    new_row['chlorides'],new_row['freeSulfurDioxide'],new_row['totalSulfurDioxide'],new_row['density'],new_row['pH'],
    new_row['sulphates'],new_row['alcohol'],new_row['quality'],new_id]

    with open('Wines.csv', 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(new_line)
        f_object.close()


#save model in model.pkl
def pickle_model(model):
    
    """serialise the model into a pickle file
    
    Args:
        model (RandomForestClassifier): last trained model
        
    Returns:
        pickle file modified with the last trained model
    """
    
    pickle.dump(model, open('model.pkl', 'wb'))