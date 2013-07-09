# Digboi

Digboi helps you with analyzing failing tests one-by-one in a series of builds
with ease.

Inspecting why a particular test is failing in different builds in Jenkins can
be irritating since you have to check every test's failure result in every
build one-by-one. Digboi helps you with this by compiling failure results for
a test in one page with stacktraces and other useful information like the
count of failures and the builds in which tests failed.

## Installation

```
pip install -r requirements.txt
```

## Running

```
python server.py
```

In browser, go to `http://localhost:5000`. 
