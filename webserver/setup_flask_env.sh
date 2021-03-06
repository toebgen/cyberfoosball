echo "Setting up flask virtual environment..."

python3 -m venv flask

flask/bin/pip install flask
flask/bin/pip install flask-sqlalchemy
flask/bin/pip install sqlalchemy-migrate
flask/bin/pip install flask-whooshalchemy
flask/bin/pip install flask-wtf
flask/bin/pip install flask-babel
flask/bin/pip install guess_language
flask/bin/pip install flipflop
flask/bin/pip install coverage

mkdir app
mkdir app/static
mkdir app/templates
mkdir tmp
