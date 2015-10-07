# Step-by-Step Guide

Follow this guide to setup your development machine.

1. Install [git], [postgresql] and [virtualenv], in your computer, if you don't have it already.
2. Get the source code on your machine via git.
    
    ```shell
    git clone https://github.com/pythonindia/wye.git
    ```

3. Create an isolated python 3 environment and install python dependencies.

    ```shell
    cd wye
    virtualenv -p $(which python3) venv
    source venv/bin/activate  # run this command everytime before working on project
    pip install -r requirements/dev.txt
    ```

4. Copy over `settings/dev.sample.py` to `settings/dev.py`.

    ```
    cp settings/dev.sample.py settings/dev.py
    ```

5. Create an empty postgres database and run database migration.

    ```
    createdb wye
    python manage.py migrate
    python manage.py sample_data
    ```

6. That's it. Now you can run development server and open the site admin at http://localhost:8000/django-admin/ (initial creds: admin / 123123)

    ```
    python manage.py runserver
    ```


[git]: https://git-scm.com/downloads
[virtualenv]: https://virtualenv.pypa.io/
[postgresql]: http://www.postgresql.org/download/
