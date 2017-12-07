# Update in this branch

In this branch, I will demo how to use the `urlfetch` library from Google. This library is usable in GAE only. AFAIK, This is the only way to make HTTP(s) requests from GAE instance. The document said it utilizes Google's internal HTTP request proxy. There are some restrictions such as you cannot change the `user-agent` in the request headers. But they are not so important to us in this demo. You can use other libraries such as `Requests`. The *details* are in [here](https://cloud.google.com/appengine/docs/standard/python/issue-requests)

## Before we go to the changes...
\* This based on the result of the previous step.
It is expected that you are using `jinja2==2.10` and `flask-restplus` which are installed using `pip`. `appengine_config.py` is properly configurated too.

So if you just clone and switch to this branch, you have to:

```
mkdir lib
pip install -r requirements.txt -t lib --upgrade
```

then make sure `appengine_config.py` is:

```
from google.appengine.ext import vendor

# Add any libraries install in the "lib" folder.
# uncomment to use `lib` which install the custom jinja2.10
vendor.add('lib')
```

## Changes

1. Add `util/ig.py` to handle IG stuffs...
2. Add new API `/users/<username>/fetch` to trigger the fetch.

IG really hates AppEngine. It will return HTTP 429 error sometimes.

# Next step

The next branch is `features/memcache-homepage`.

---
# Introduction

This is a demo application of Google AppEngine for [the meetup](https://www.eventbrite.com/e/gcpug-meetup-2017nov-tickets-39642814726) of [Google Cloud Platform User Group Hong Kong](https://www.facebook.com/groups/gcpughk/) on 30-Nov-2017.

The intention of this application is to demonstrate how to build a _toy_ application on AppEngine standard environment in step-to-step manner.


# Prerequisite

You need to install the *Google Cloud SDK* first. Then after proper configuration, you can run the command `gcloud app deploy app.yaml` to deploy to GAE.

Besides, the code is written in Python2.7. And `pip` is needed to install the required python library. I test and run the code in MacOS. I have no idea how to set up the development server on Windows. But for Linux user, there should be no technical difficulty at all.

# Steps

Each step is in differnt git branch

1. master branch - The starting point. Basically, it is the sample code Google gave me when I start this project a few days ago (around 2017-11-28)
1. features/add-html - Add jinja2 support. Demo how to use built-in library
1. features/add-js-css - Add static assets. Demo how to leverage Google's CDN... Well basically just a few lines of config in app.yaml.
1. features/add-api - Add API endpoints. The API is built with Flask-restplus. It kind of demonstrates that you can use different frameworks in one single GAE project.
1. features/add-ndb - Use ndb to store the IG user info.
1. features/fetch-from-ig - demo how to use `urlfetch` library from Google. You can use it to call 3rd party APIs like FB graph...
1. features/memcache-homepage - demo how to use memcache to store hardly fetched IG homepage...
1. features/add-gcs - demo how to store images or whatever file with Google Cloud Storage (GCS)
1. features/add-tq - demo how to use task queue to do a bunch of tasks in the background.
1. features/add-cron-fetch - demo how to use `cron.yaml` to define a cronjob in appengine.

