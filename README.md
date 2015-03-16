To view in browser (with nice formatting)
--------------------------
Go here: https://gist.github.com/mattgmarcus/bc0908c9be25a832611f

Setup
--------------------------

To set up your environment, follow these instructions:

If you don’t have postgresql installed, you can get it here: http://postgresapp.com
You'll need to make sure to move the postgres app to your /Applications folder, which it will prompt you to do when you start the application.
You'll need to add this to your PATH in order to access Postgres commands. The easiest way is to put it in your ~/.bash_profile. You can do that in one line:
```
echo "export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/9.4/bin" >> ~/.bash_profile
```
Or if you'd prefer to do it on your own, you can just copy this line in:
```
export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/9.4/bin
```
Either way, start a new terminal window afterwards to source the updated bash profile so the new PATH variable is in effect.

If you see issues (now or later) related to libssl or libcrypto, try setting up symbolic links with these two lines. This worked for us:
```
sudo ln -s /Applications/Postgres.app/Contents/Versions/9.4/lib/libssl.1.0.0.dylib /usr/lib
sudo ln -s /Applications/Postgres.app/Contents/Versions/9.4/lib/libcrypto.1.0.0.dylib /usr/lib
```


To install our dependencies (Note: you may or may not have to use sudo for some of these. I included sudo in front of the ones I think you may have to for):
```
sudo easy_install pip
sudo pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pip install psycopg2
```

If the installation fails on psycopg2, make sure you have the Apple developer command line tools installed (you need the gcc capabilities to compile psycopg2).

To setup the database (which should result in 1231 records for accepted loans and 1998 for rejected loans)
```
createdb pythia_dev
python manage.py db upgrade
python init_test_db.py
```


Note: If this installation doesn't work fully, please let us know. We've done this on our own computers, and we did test it on one separate computer we had access to, but depending on your specific operating system, things may not work fully. You can email us and we'll try to see if we can figure it out. It's also possible that there would be a stackoverflow topic about this (especially for installation-type issues)

If you want to delete the database later, you can do this command:
```
dropdb pythia_dev
```


How to run our code
---------------------------------

All of our code is run from the file pythia.py. The syntax to call it is:
```
python pythia.py <test_type> -n <num_iterations> -m <num_samples> -t <num_trees>
```

We solved three problems:
1. Accept - Will a loan be accepted
2. Grade - What grade will be assigned to the loan
3. Quality - Will the loan be paid back or defaulted on

The test types are: [accept, grade, grade_logit, quality]. 
For grade, we have two implementations. If you use the test_type "grade", you will use the random forest regressor. If you use test_type "grade_logit", you'll use the ordinal logit

For the other parameters, they have default values if you don't set them. They are:
 - Number iterations = 1
 - Number samples = 1000
 - Number trees = 16

So, if you want to test our program on the acceptance algorithm with 10 trees, 500 samples, and 2 iterations, you can do:
```
python pythia.py accept -n 2 -m 500 -t 10
```

This will print separate results from 2 runs, each of which will contain a score and an OOB score.

So if you want to test all of our implementations with 500 samples across 2 iterations, with 10 trees for each of the random forest algorithms, you can do:
```
python pythia.py accept -n 2 -m 500 -t 10
python pythia.py grade -n 2 -m 500 -t 10
python pythia.py grade_logit -n 2 -m 500
python pythia.py quality -n 2 -m 500 -t 10
```


Web Application
---------------------------------
Our web application can be run using the command "python app.py" in the root Pythia folder and then navigating to localhost:5000 in your web browser (note: we have only tested on Google Chrome and not other web browsers, so Google Chrome should be used to observe the proper behavior of the application). 



Use of external software
---------------------------------
We used a few external software packages as benchmarks for the code that we wrote ourselves. We used the implementations of Random Forest Classifier and Regressor in SciKit-Learn (https://github.com/scikit-learn/scikit-learn), and the implementation of Ordinal Logit in the minirank package (https://github.com/fabianp/minirank).

When we implemented our own code, we did not use any of the external code for the main aspect of our algorithms. We only used external code for two ancillary functions. 
The first place is when we use DictVectorizer in pythia.py and app.py, which is a scikit-learn class that performs binary one-hot coding on features that have string values such that each string value of a feature is represented by a boolean valued feature. This allowed us to use features from our data set that were originally strings.
The second place we used external code was in the predict method in ordinal_logit.py. This method was a fairly straightforward matrix operation so we used the 4 lines of code from the minirank implementation, which seemed to be the most efficient way to do the computation using numpy.

Throughout our code, we have some parts where we've commented out this external code. This is there so you can see how we would switch between using our implementations and the external ones. When we use the SciKit RandomForestClassifier, for instance, we have to comment in the import statements for it and comment out our own implementation, and then change the constructor too
