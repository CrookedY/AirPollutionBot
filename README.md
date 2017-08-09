# AirPollutionBot
tweets air pollution data for sheffield city centre

# Development
hack on the python, make it do what you want

# Deployment
Step 1 - setup your secret env variables to run the code
  + `cp env.list.example env.list`

Step 2 - Use docker to build and run the code.
  + Note: you will need to pass in the env secrets so the bot can auth with twitter.

```
 docker build -t airpollutantbot:latest .
 docker run --env-file ./env.list airpollutantbot

 # run this cmd to get a bash prompt in the docker image (useful for debugging)
 docker run -it --env-file ./env.list airpollutantbot /bin/bash
```

Note: you must rebuild the image if you have made code changes!

Step 3 - Host the code at https://hub.docker.com/r/hannahs662/airpollutionbot/
  + use the docker image to run the code
  + pull it from docker `docker pull hannahs662/airpollutionbot`

# TODO:
Step 4 - set the docker image up to run on a schedule
