echo "-> Drop Database"
dropdb wye

echo "-> Create Database"
createdb wye

echo "-> Run migrations"
python manage.py migrate

echo "-> Add sample data"
python manage.py sample_data
