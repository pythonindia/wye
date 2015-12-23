# Step-by-Step Guide

Follow this guide to setup your development machine.

1. Install [git], [postgresql] and [virtualenv], in your computer, if you don't have it already.
2. Ensure that python3-dev and libpq are installed on your system.

    ```shell
    # if you are using a debian based os for development run:
    sudo apt-get install -y python3-dev python3-pip libpq-dev libjpeg-dev
    ```

3. Get the source code on your machine via git.
    
    ```shell
    git clone https://github.com/pythonindia/wye.git
    ```

4. Create an isolated python 3 environment and install python dependencies.

    ```shell
    cd wye
    virtualenv -p $(which python3) venv
    source venv/bin/activate  # run this command everytime before working on project
    pip install -r requirements/dev.txt
    ```

5. Copy over `settings/dev.sample.py` to `settings/dev.py`.

    ```
    cp settings/dev.sample.py settings/dev.py
    ```
    
6. Change credential in setting/dev.py
    
    ```
    nano settings/dev.py
    ```
    For new postgresql user(people who are new to it.)
    
    #####USER: "postgres"
    
    #####PASSWORD: ""

7. Create an empty postgres database and run database migration.

    ```
    createdb wye
    python manage.py migrate
    python manage.py sample_data
    ```

8. That's it. Now you can run development server and open the site admin at http://localhost:8000/django-admin/ (initial creds: admin / 123123)

    ```
    python manage.py runserver
    ```


[git]: https://git-scm.com/downloads
[virtualenv]: https://virtualenv.pypa.io/
[postgresql]: http://www.postgresql.org/download/
