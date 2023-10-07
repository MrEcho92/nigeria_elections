# Analytics Project

This project utilises data to keep users informed. This project is built using [Djangae scaffold](https://gitlab.com/potato-oss/djangae/djangae-scaffold).

# Website
![web archive org_web_20230117215125_https___transformnaija org_ (2)](https://github.com/MrEcho92/nigeria_elections/assets/60829927/2aadec02-bbc9-4996-aec7-6fb605b82ed3)


## Prerequisite 

- Download Java 17 sdk for your computer
[install Java](https://www.oracle.com/java/technologies/downloads/#jdk17-mac)
- Download Google sdk and follow instructions for installation [gcloud CLI](https://cloud.google.com/sdk/docs/install)

# Formatting and linting
 - black
 - isort
 - flake

 ## Running BE formatter and linter
 - To format you code run `black .`
 - To check linting run `flake8 .`
 - To sort imports run `isort .`

# Running the project

1. Clone this repo from [here](git@gitlab.com:chigozie10/analytics.git)
2. Run the following command, replacing `myproject` with the name of your project
3. Create a virtualenv and activate it (e.g. `python3 -m venv .venv && source .venv/bin/activate`)
4. Install the requirements: `pip3 install -r requirements.txt`
5. Install the local development requirements: `pip3 install -r requirements-dev.txt`
6. Run `python3 manage.py runserver` or `./manage.py runserver`


# Testing
- We write tests for this project.

# Deploy 
- We deployed out application through Google App Engine. To deploy locally, you will need to install gcloud CLI and have an account.
- Run the script `./scripts/deploy.sh `
