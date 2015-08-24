Court and Tribunal Finder search
==================

## Installation

This applies to OSX, but should be similar with any other Unix variant.

Clone the repository:

    git clone git@github.com:ministryofjustice/courtfinder-search.git

Next, create the environment and start it up:

    virtualenv env --prompt=\(courtfinder-search\)

    source env/bin/activate

Install python dependencies (ignore the warnings):

    pip install -r requirements/local.txt

Install node packages, gulp and sass:

    npm install
    npm install gulp -g
    npm install gulp --save-dev
    gem install sass


Compile the static assets:

    gulp

Setup postgres: create a user courtfinder with no password and create a database called courtfinder_search, which user courtfinder has owner and superuser rights:

    psql template1
    template1=> create user courtfinder login;
    template1=> create database courtfinder_search;
    template1=> alter database courtfinder_search owner to courtfinder;
    template1=> alter user courtfinder with superuser;
    template1=> \q

Create the database and put sample data in it:

    python manage.py makemigrations
    python manage.py migrate
    python manage.py populate-db

Start the server:

    python manage.py runserver

## Testing and code coverage

Testing uses Django's standard unit testing library. In order to run the tests, use:

    python manage.py test

Code coverage is measured using 'coverage', speficied in the requirements file for the testing environment. In order to run coverage, use:

    coverage run --source='.' manage.py test staticpages courts search
    coverage run --append --source='.' manage.py populate-db data/test_data

The two lines above runs the unit tests, so it can replace the first command mentioned above. The coverage report is then available by using:

    coverage report -m

py.test can also be used to run tests faster:

    py.test -n 3

will run the tests using 3 processes. To show the coverage report:

    py.test -n 3 --cov . --cov-report term-missing

## Environment variables

The application uses the following environment variables.

* `FEEDBACK_EMAIL_SENDER`: the from address of the feedback emails sent by the application
* `FEEDBACK_EMAIL_RECEIVER`: the email addresses of the recipients of the feedback emails (comma separated)
* `SMTP_HOSTNAME`
* `SMTP_PASSWORD`
* `SMTP_PORT`
* `SMTP_USERNAME`: SMTP details for sending feedback emails
* `SENTRY_URL`: for monitoring. See <https://getsentry.com/>
* `S3_KEY`, `S3_BUCKET`, `S3_SECRET`: the `populate-db` command above either reads the court data from local files or, if those variables are set, from an S3 bucket.
