# Step 1: Create a virtual environment
python -m venv venv

# Step 2: Activate the virtual environment
# On Windows
.\venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Step 3: Install dependencies
pip install -r requirements.txt --break-system-packages

# Step 4: Run your application
python manage.py runserver  # Replace with your app’s entry point
