# chr1sBot
A Discord bot that does stuff.

# Running it
I have no clue why you'd want to run this (it's generally used by me for testing things), but the information here is provided anyway.  
You'll need the Docker Engine and `docker-compose` installed.

First off, clone this repository and `cd` into it.  
Next, set up a `config.py` file with the necessary variables (`config.example.py` coming soon)  
Edit the `docker-compose.yml` and `Dockerfile` as you see fit.  
You'll also need to make a `application.yml` in order to use the bundled Lavalink server.  
Once all of that is set up, use `docker-compose up` to get everything started. (`-d` flag to run detached)
