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
Using this pattern, its easy to keep adding parameters in different methods/PipelineSteps until the entire query has been
planned out. After that, one can build the model creating a function that can be called with the api or 
run it instantly with an api instance. It was chosen to do it this way, as for example, the Prominent Person model
will augment the fetchers with their own stored information.

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

The current API uses Pipelines. Pipelines can be linked to each other as to create one uniform flow
of data. These pipelines are then collected in the pipeline zoo where developers can either create new pipelines
or consume the most general pipelines. This will make it easy to return different kinds of data rapidly by
containing the functionality of one step to as little as possible. Another **great advantage is the possibility of, like spark,
distributing the load over multiple microservices**. Due to the scope of the project, this was not implemented,
but applications can easily be connected with RPCPipelines for example, pushing the data to other microservices
that run on, for example, a kubernetes cluster. This is the main advantage of using these pipelines.

Some pipelines support checkpointing by setting the `checkpointed` flag to true during initialisation.
What this does is caching all runs' results based on the input hash. 
This will make it easy to debug certain steps that are based on expensive previous steps. The `pipelines.py` file contains an example.

The true value of this checkpointing is in debugging speed. For example, the pipeline is something like this:
Input -> Expensive step -> Failed step -> Output. Now we can transform the pipeline to debug the failed step as follows:
Input -> Expensive step (checkpointed) -> Failed step -> Output. The expensive step will now not be calculated, but its result
will come from the cache.

Of course, its also possible that the exact input data cannot be reused. In this case, there are two possibilities.
If the object still exists, the last computed input hash is still present on the object as `last_checkpoint`. 
Then the `InputPipeline` object exposes a function `continue_last_checkpoint` that reuses the last computed data.
If this is not possible, it's also possible to rerun the pipeline with a given input hash with the function 
`continue_last_checkpoint_for_hash`. It is required that some checkpoint in the pipeline exists with the given hash,
a `ValueError` is raised otherwise.

To have a deterministic way of representing the input data, we use the `pickle.dumps(value)` function as
this represents the input data (all kinds of input) in a binary way.

## Resources
In the resource folder, all static resources are summed up. This folder was added to include the prominent people
in an easy to change format (such as JSON). This will allow other people to more easily add their tags and keywords.

## Visualisations
This API is part of an analysis. All visualisation code is present under the `visualisation` directory and will
probably include `matplotlib` plots, `D3` visualisations and other derivatives of this API.

The preferred way to create such a visualisation is to go through 3 steps.

- Create the pipeline (preferably using the same name for shared steps with other pipelines)
- Run the pipeline with the input

To allow visualisations to be a `PipelineStep`, the `Visualiser` class has
all methods a visualisation needs to extend. This will also allow a `Visualiser` to
be ran during other pipelines (for example to visualise API usage or API latency?)

Offline visualisations are visualisation for which we do not need a pipeline step. These visualisations are mostly
over either a lot of data such that we cannot compute them in real time,
or data comes from multiple non-streaming sources, for example a running cron job.

## Data trove
We included a data trove that contains all our ran cron tasks. A normal project would not add these to the git
repository, but as this is a school project, we wanted to add all necessary resources.

The data trove contains the sentiment distribution for each handle over a couple of datetimes.
The `raw` folder contains the raw tweet data. The `tweetlength` folder contains the tweet length per tweet.
These can be extended by adding extra output pipelines, but we leave this up to the business needs of each user.