wye is the platform to help organisations(Colleges/FOSS) connect to expereinced tutors which will benefit number of students to learn Python and real time use of Python in different domains. 

wye is pronounced as #Y

How to setup
============

(If you need detailed step-by-step guide, read the documentation [here](docs/setup.md))

 - Create a PostgreSQL 9.3 database
 - It is advised to install all the requirements inside virtualenv, use virtualenvwrapper to manage virtualenvs.

``` 
cp settings/dev.sample.py settings/dev.py
createdb wye
pip install -r requirements/dev.txt
python manage.py migrate
python manage.py sample_data
python manage.py runserver
```

Initial auth (admin / 123123)

# Community

- [Mailing List]

Contributing
------------

1. Choose an [issue][issue-list] and ask any doubts in the issue thread.
2. Report any bugs/feature request as github [new issue][new-issue], if it's already not present.
3. If you are starting to work on an issue, please leave a comment saying "I am working on it".
4. Once you are done with feature/bug fix, send a pull request according to the [guidelines].

[issue-list]: https://github.com/pythonindia/wye/issues/
[new-issue]: https://github.com/pythonindia/wye/issues/new
[guidelines]: https://github.com/pythonindia/wye/blob/master/CONTRIBUTING.md
# License

This software is licensed under The MIT License(MIT). See the LICENSE file in the top distribution directory for the full license text.

[Mailing List]: http://lists.pssi.org.in/cgi-bin/mailman/listinfo/pythonexpress
