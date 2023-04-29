<<<<<<< HEAD
# Movie recommendation

API applied to AI

TP noté pour le 30/04/2023

## Pré-requis

Téléchargez les documents :

- main.py

- model.py

- movies.json

- model.pkl


Liste des packages nécessaires :

- fastapi

- pydantic

- sklearn

- pandas

- pickle

- json

## Utilisation

Lancez sur votre terminal la commande : 

uvicorn main:app --reload

Puis rendez-vous sur le lien qui s'affiche.

En rajoutant /docs à l'adresse vous verrez apparaître toutes les commandes API disponibles.

GET/api/model : Permez de lancer le téléchargement du fichier model.pkl conenant le modèle préentrainé.

GET/api/predict : Affiche les caractéristiques du meilleur film.

POST/api/predict : Rentrez les caractéristiques d'un vin pour prédire sa qualité.

GET/api/model/description : Affiche les paramètres du modèle ainsi que sa précision.

POST/api/model/retrain : Relance l'entraînement du modèle.
(il est conseillé d'avoir utilisé la commande PUT/api/model avant si vous espérez un changement dans la prédiction) 


## Auteurs

Ruau Nicolas
=======
# Recommendation
Python (Panda, sklearn, json, pickle)
>>>>>>> f87069056ba51d84b0d524eb61c11e96c3b1eecb
