from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from model import *
from get_movie_list import *
from genres import *
from gen_user_token import *
from create_user import *
from check_token import *

from fastapi.middleware.cors import CORSMiddleware

class MovieRating(BaseModel):
    user_id: int
    movie_id: int
    rating: float

app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

