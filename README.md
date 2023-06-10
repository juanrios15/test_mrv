# TEST MRV7

## Installation
1. Create and activate a virtual environment:
```
python -m venv .env
cd .env/Scripts/
activate
```
If you are using linux:
```
python3 -m venv .env
source .env/bin/activate
```
2. Clone this repo to an specific folder
```
git clone https://github.com/juanrios15/test_mrv.git
```
3. Install required libraries
```
cd test_mrv
pip install -r requirements.txt
```
4. Migrate data models and run project
```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
## Usage