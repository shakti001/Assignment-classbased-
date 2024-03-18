# Create a virtual environment (optional but recommended)
python -m venv myenv
cd myenv/bin/activate  # On Windows: myenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Create a superuser (if applicable)
python manage.py createsuperuser

# Run the development server
python manage.py runserver
