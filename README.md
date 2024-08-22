# Mentor App Backend

## How to Setup

## Test
Run all tests.
```
coverage run manage.py test
```

Run a specefic Tests File.
```
python manage.py test myapp.tests.test_views
```

Run a Specific Tests class
```
python manage.py test path.to.your.test_module.TestClassName
```

For example, if you want to run a specific test class named MyViewTest in myapp/tests/test_views.py, you can run:
```
python manage.py test myapp.tests.test_views.MyViewTest
```

Get the Tests coverage Report.
```
coverage report
```

Get the TestS Coverage in HTML
```
coverage html
```