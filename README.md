# BDS_group_27

## Installation
First run `pip install -r ./requirements.txt`\
Next go to the `app.py` and run the python file to start a test server.


## General Structure
This project is a flask web application with multiple endpoints.


All endpoints are present in the `app.py` file. 
Any API settings are present in the `settings.py` file and the `.env` file

### Data gathering
In the data gathering folder, all usages of external datasources are bundled. 
This project mainly supports on `Tweepy` for the Twitter API bindings. 
The custom functions to fetch these resources are thus placed in this directory. 

Currently, there are a couple of files with classes and methods. 
The most important class for the Tweepy bindings is the `FetchBuilder`. 
This class uses the builder pattern to compile a `/search` request to Twitter's API. 
Using this pattern, its easy to keep adding parameters in different methods until the entire query has been
planned out. After that, one can build the model creating a function that can be called with the api or 
run it instantly with an api instance. It was chosen to do it this way, as for example, the Prominent Person model
will augment the fetchers with their own information.

## Models
Currently the API builds on 2 models. These models are stored in the `models` directory.
 
The first is a `TwitterUser`. This object has a handle which can be used to search
the correct Twitter user. Other properties will probably be added in the future. These properties will probably be proxies to
the Tweepy API.

The second model is the `ProminentPerson` model. This model is also a `TwitterUser`, so has a handle, but also
contains a list of associated tags and keywords. These can be used to augment the information we have on a given
handle and will return better results due to this. For example, 'president of the united states' might also refer
to the Twitter user with handle `@POTUS`. This will make our analysis more accurate.

Lastly, the `GeoCode` and `ResultTypes` both mirror the values as used by the `/search` endpoint such 
that we can reason about them more easily in our code.

## Processing
This directory will include the processing steps we do within our API. Sentiment analysis, aggregation 
and other processing steps will be defined here.

The current API uses Pipelines. Pipelines can be linked to eachother as to create one uniform flow
of data. These pipelines are then collected in the pipeline zoo where developers can either create new pipelines
or consume the most general pipelines. This will make it easy to return different kinds of data rapidly by
containing the functionality of one step to as little as possible. 

## Resources
In the resource folder, all static resources are summed up. This folder was added to include the prominent people
in an easy to change format (such as JSON). This will allow other people to more easily add their tags and keywords.

## Visualisations
This API is part of an analysis. All visualisation code is present under the `visualisation` directory and will
probably include `matplotlib` plots, `D3` visualisations and other derivatives of this API.