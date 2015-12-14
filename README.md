[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

[![Build Status](https://travis-ci.org/pythonindia/wye.svg)](https://travis-ci.org/pythonindia/wye) [![Coverage Status](https://coveralls.io/repos/pythonindia/wye/badge.svg?branch=master&service=github)](https://coveralls.io/github/pythonindia/wye?branch=master)
[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/pythonindia/wye_chat_room?utm_source=share-link&utm_medium=link&utm_campaign=share-link)

[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/pythonindia/wye/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/pythonindia/wye/?branch=master)

[![Code Health](https://landscape.io/github/pythonindia/wye/master/landscape.svg?style=flat)](https://landscape.io/github/pythonindia/wye/master)
wye is the platform to help organisations(Colleges/FOSS) connect to experienced tutors which will benefit number of students to learn Python and real time use of Python in different domains.

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

## Testing

It's highly encouraged that you write test for any new feature/bug fixes. Find all the existing test inside `tests/` folder. To run the test locally, run the following command:

```
py.test
```

You can invoke `py.test` with various commandline arguements, that can drastily improve your test writing/running experience. Read useful tip/tricks at [docs/testing.md].

#### Login Details

Email: admin@pythonexpress.in
Password: 123123


### Making Frontend Changes

Make sure you have [nodejs][node] & [npm][npm] installed

```
$ npm install
$ gulp   // This starts a watcher to watch for file changes
```

[node]: https://nodejs.org/en/
[npm]: https://www.npmjs.com/

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
[docs/testing.md]: docs/testing.md

# License

This software is licensed under The MIT License(MIT). See the LICENSE file in the top distribution directory for the full license text.

[Mailing List]: http://lists.pssi.org.in/cgi-bin/mailman/listinfo/pythonexpress
