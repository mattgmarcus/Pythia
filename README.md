# Pythia
Predict the approval and rating of your Lending Club application


To point to config locally,
  export APP_SETTINGS=config.DevelopmentConfig

For heroku
  heroku config:set APP_SETTINGS=config.StagingConfig --remote stage
  heroku config:set APP_SETTINGS=config.ProductionConfig --remote pro


Environment variable for Database
  export DATABASE_URL="postgresql://localhost/pythia_dev"
OR if that doesn't work then do
  export DATABASE_URL="postgresql:///pythia_dev"

To create the DB:
  createdb pythia_dev
  python manage.py db init
  python manage.py db migrate
  python manage.py db upgrade


To get up to do on migrations, you only have to do the command:
   python manage.py db upgrade



To install autoenv
   brew install autoenv
Add this line to ~/.bash_profile or ~/.bashrc, whichever one you use
    source /usr/local/opt/autoenv/activate.sh
Note: For Shuo, in the .env file you may have to change your DATABASE_URL to the 2nd one above