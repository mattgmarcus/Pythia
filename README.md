To set up your environment, follow these instructions:

If you don’t have postgresql installed, you can get it here: http://postgresapp.com
If you see issues (now or later) related to libssl or libcrypto, try setting up symbolic links with these two lines. This worked for us:
  sudo ln -s /Applications/Postgres.app/Contents/Versions/9.4/lib/libssl.1.0.0.dylib /usr/lib
  sudo ln -s /Applications/Postgres.app/Contents/Versions/9.4/lib/libcrypto.1.0.0.dylib /usr/lib


easy_install pip
pip install -r requirements.txt
createdb pythia_dev
python manage.py db upgrade

python init_test_db.py
       Should give 1231 accepted loans, 1998 rejected loans

