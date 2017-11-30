# Update in this branch

1. in `app.py`, we use `jinja2` to load the template and render it. Please note that it is coupled with `webapp2`.
2. Since we used `jinja2`, we have to update `app.yaml` to include `jinja2`. The list of 3rd party python library can be found in [here](https://cloud.google.com/appengine/docs/standard/python/tools/built-in-libraries-27)

## Using `jinja2` without `webapp2`

Try this

```
def jinja(self):
  import jinja2
  JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                       extensions=['jinja2.ext.autoescape', 'jinja2.ext.with_', ],
                                       autoescape=True)

  return JINJA_ENVIRONMENT
```

Then, you can do something like this:

```
jinja().get_template('some_template.html').render(**data)
```

## Can I use newer `jinja2`?

Yes. The 3rd party libraries sometimes too old. Use `pip` to install new version or other libraries. As long as the library does not entirely rely on c-modules, it should work. The detail way is listed in [this doc](https://cloud.google.com/appengine/docs/standard/python/tools/using-libraries-python-27)

Here is a summary

1. `mkdir lib` - create a new folder called `lib`. We will install libraries into this folder.
2. `pip install --upgrade jinja2 -t lib` - this will install the latest version of jinja2 into `lib`.
3. Create a file named `appengine_config.py` with the following content
    ```
	from google.appengine.ext import vendor

	# Add any libraries install in the "lib" folder.
	vendor.add('lib')
	```
4. Remove the conflicting library in `app.yaml`.


It is *HIGHLY* recommended to use a `requirements.txt` file to store all the dependencies. E.g.

```
Flask==0.10
Markdown==2.5.2
google-api-python-client
```

The new command to install the libraries: `pip install -t lib -r requirements.txt --upgrade`

# Next step

The next branch is `features/add-js-css`.

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

