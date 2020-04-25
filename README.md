This program takes factors such as actors,directors,genres,IMDB ratings,release year,budget and predicts the estimation of revenue can be collected in released country.

The datascience part uses python. It uses RandomForest Regression to predict revenue and success.

preprocessingAndAccuracy.py file is used to clean and modify the meta dataset of IMDB and also train the model to get accuracy.

main.py file takes the cleaned data and according to the input values it predicts the revenue in Released country which shows success if the revenue collected is atleast 50% more than the budget 

The datsets were obtained from kaggle which were scraped from IMDB. it has 5000 data entries
