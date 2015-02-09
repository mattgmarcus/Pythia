# Pythia
Predict the approval and rating of your Lending Club application


To point to config locally,
export APP_SETTINGS=config.DevelopmentConfig

For heroku
heroku config:set APP_SETTINGS=config.StagingConfig --remote stage
heroku config:set APP_SETTINGS=config.ProductionConfig --remote pro


Environment variable for DB:
export DATABASE_URL="postgresql://localhost/pythia_dev"

To create the DB:
createdb pythia_dev
python manage.py db init
python manage.py db migrate
python manage.py db upgrade