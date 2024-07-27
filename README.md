# RESTCountries Example

This is a simple FastAPI project to consume the [RESTCountries](https://restcountries.com/) API.

## Usage

I tried to make this project as easy to test as I can. Just clone the project, cd into `restcountries-example` directory and if you have Podman installed run this command to build the container image

```bash
podman build -f ./Containerfile -t fastapi_env:v1
```
Then to run the project you can run

```bash
podman run --rm --name FastAPI_dev -p 8080:8080 fastapi_env:v1
```
In case you use docker instead of podman, just replace the `podman` command word for `docker`, and it works the same. (`docker build -f ...`)

Then go to [this Local URL](http://localhost:8080/docs) to interact with the API.

## Live demo
A live demo can be found [here](https://restcountries-example.vercel.app/docs). Hosted in Vercel.

## Approach

I used the FastAPI python framework even when my 'most dominant' language is PHP just because it's a simpler framework than the ones I know for PHP, and also as I needed to deploy it somewhere, Vercel is one provider that integrates well with it. I started calling the RESTCountries API directly, but then I realized that some of the other requirements are a little more complex and the API doesn't account for those use cases, so I imported the API data into a SQLite database for easy query.

I didn't use SQLAlchemy (famous Python ORM) because I wanted to use the SQLite JSON built-in functions and to do that I needed to run raw SQL queries, so it was pointless to add that. This decision also meant that I have to implement pagination manually, but for this small exercise I thing it was a fair trade off. I also use an async library (httpx) to ensure about concurrent requests and implemented a router, so it can scale better in the future, I also thought it was a little too much... but as the objective of the exercise is to overengineering a bit, I thought it was fair to add this.

I wanted to add tests, but if I have to be completely honest, I was not sure about the strategy to do so since it's an external API and I haven't had enough time to investigate about it. I think it would be cool to refine the code a little bit more as surely I have a lot of room for improvement, for example I would like to fine tunning the languages endpoint as of right now it looks into collections of languages instead of looking for individual languages spoken in every country. I liked to use SQLite as a data source, because I only load the data in the beginning if it's not yet setted, and after that first time the performance is pretty good and the queries run almost without timeouts. It was pretty interesting to look for different libraries to fetch the external API data, and to evaluate what was the best to use for this exercise.

Also, as a negative note, I have a problem with Vercel because even if the code is running perfectly locally (you can test the code with podman/docker) I found a problem when deploying to Vercel, I investigate and found that it can be caused for a version of the dependencies I used (in requirements.txt I didnt ask for a specific version) but I cant fix it in time. Over all, it was a pretty cool and fun project to work on!
