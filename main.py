# class Wine(BaseModel):
#     fixedAcidity : float
#     volatileAcidity : float
#     citricAcid : float
#     residualSugar : float
#     chlorides : float
#     freeSulfurDioxide : float
#     totalSulfurDioxide : float
#     density : float
#     pH : float
#     sulphates : float
#     alcohol : float
    
# class New_wine_in_df(BaseModel):
#     fixedAcidity : float
#     volatileAcidity : float
#     citricAcid : float
#     residualSugar : float
#     chlorides : float
#     freeSulfurDioxide : float
#     totalSulfurDioxide : float
#     density : float
#     pH : float
#     sulphates : float
#     alcohol : float
#     quality : float

# app = FastAPI()

# #print(predict_quality(new_wine,model))

# #routes 

# @app.get("/")
# async def root():
#     return {"message": "Bonjour Lucas, tu devrais essayer /docs en premier :)"}

# @app.get("/api/model")
# async def get_module():
#     file_path = "model.pkl"
#     return FileResponse(path=file_path, filename=file_path, media_type='model/pkl')

# @app.get("/api/predict")
# async def get_module():
#     return get_best_wine()

# @app.get("/api/model/description")
# async def get_module():
#     df = pd.read_csv("Wines.csv")
#     model, x_train, x_test, y_train, y_test = get_model(df)   
#     model = pickle.load(open('model.pkl', 'rb'))
#     descript = description(model, x_test, y_test)
#     return{"Voici les paramètres du modèle": descript[0] , " avec un précision de" : descript[1]}


# @app.post("/api/predict")
# async def create_wine(Wine: Wine):
#     Wine = {'fixedAcidity' : Wine.fixedAcidity,
#     'volatileAcidity' : Wine.volatileAcidity,
#     'citricAcid' : Wine.citricAcid,
#     'residualSugar' :Wine.residualSugar,
#     'chlorides' : Wine.chlorides,
#     'freeSulfurDioxide' : Wine.freeSulfurDioxide,
#     'totalSulfurDioxide' : Wine.totalSulfurDioxide,
#     'density' : Wine.density,
#     'pH' : Wine.pH,
#     'sulphates' : Wine.sulphates,
#     'alcohol' : Wine.alcohol
#     }
#     model = pickle.load(open('model.pkl', 'rb'))
#     return predict_quality(Wine,model)

# @app.post("/api/model/retrain")
# async def get_module():
#     df = pd.read_csv("Wines.csv")
#     model,x_train,x_test,y_train,y_test = get_model(df)
#     model = train_model(model,x_train,y_train)
#     pickle_model(model)
#     return {"Modèle réentrainé et sérialisé"}

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from model import *
from get_movie_list import *
from genres import *
from gen_user_token import *
from create_user import *
from check_token import *

class MovieRating(BaseModel):
    user_id: int
    movie_id: int
    rating: float

app = FastAPI()

@app.get("/")
async def root():
    best_movies = get_best_movies()
    return {"message": "Welcome to the movie recommendation API!", "best_movies": best_movies}

@app.get("/api/movieList/{search}")
async def get_search_api(search, token):
    if(check_token(token)):
        list_movies = get_search_result(search)
        return {list_movies}
    else:
        return {"Invalid token"}

@app.get("/api/genre/{id}")
async def get_genre_api(id, token):
    if(check_token(token)):
        genre = get_genre(id)
        return {genre}
    else:
        return {"Invalid token"}

@app.get("/api/token/")
async def get_token_api(username, password):
    token = get_user_token(username, password)
    return {token}

@app.post("/api/user/")
async def create_user_api(username, email, password):
    create_user(username, email, password)
    return {"User Created!"}

@app.get("/api/model")
async def get_model(token):
    if(check_token(token)):
        file_path = "model.pkl"
        return FileResponse(path=file_path, filename=file_path, media_type='model/pkl')
    else:
        return {"Invalid token"}

@app.post("/api/predict")
async def predict_rating(movie_rating: MovieRating, token):
    if(check_token(token)):
        model = pickle.load(open('model.pkl', 'rb'))
        prediction = predict_rating(movie_rating.user_id, movie_rating.movie_id, model)
        return {"prediction": prediction}
    else:
        return {"Invalid token"}

@app.post("/api/model/retrain")
async def retrain_model(token):
    if(check_token(token)):
        train_data = pd.read_csv('train_data.csv')
        model = train_model(train_data)
        pickle_model(model)
        return {"message": "Model retrained and saved as model.pkl"}
    else:
        return {"Invalid token"}

