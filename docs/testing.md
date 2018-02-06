# Testing

- Read existing tests inside `/tests/` folder to get an idea of how the tests are organized.
- Get yourself familiar with [`fixtures`] & [`factories`]. They are your friend.
- Read https://splinter.readthedocs.org/en/latest/api/driver-and-element-api.html to get your self with all the methods available with `browser` fixture. You must include `base_url` fixture, in your test cases to start a Live Test Server.

[`fixtures`]: https://pytest.org/latest/fixture.html
[`factories`]: https://factoryboy.readthedocs.org

## Run tests partially

```shell
py.test tests/unit # Will only the tests inside tests/unit folder
py.test tests/unit/tests/app_model.py # Will only test inside app_model.py
```

This approach will reduce your testing time, while you are writing a new feature or fixing a bug. Once your sure, the test in a particular section is passing you can run all the test with `py.test`.


## Run test with html coverage report

```
py.test --cov-report=html --cov
```

Open `htmlcov/index.html` in your browser to see all the lines that are not getting covered during testing. Try to increase the overall percentage of test coverage in the project.

## Faster browser test with headless browser

```
py.test --splinter-webdriver=phantomjs
```

Functional test with selenium using Firefox can be quiet time consuming. You can install [phantomjs](http://phantomjs.org/download.html) and use `--splinter-webdriver=phantomjs` parameter with `py.test`. Checkout all the parameters available at https://github.com/pytest-dev/pytest-splinter#command-line-options


## Use `pdb` while testing

```
py.test --pdb
```

Whenever a test fails, it will drop you into into a interactive python debugger where you can inspect the local variable and step into codebase.

Always obey the testing goat!
