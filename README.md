# wye
Wye: Platform connects trainers to educational institutes and open source organisation who has interested in conducting trainings

How to setup
===

 - Create a PostgreSQL 9.3 database
 - It is advised to install all the requirements inside virtualenv, use virtualenvwrapper to manage virtualenvs.
``` 
	pip install -r requirements/dev.txt
	python manage.py migrate --noinput
```

 
# License

This software is licensed under The MIT License(MIT). See the LICENSE file in the top distribution directory for the full license text.
