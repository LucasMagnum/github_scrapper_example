# Github Scrapper Data
![CI](https://github.com/LucasMagnum/github_scrapper_example/workflows/CI/badge.svg)

This is an example application used to consume Github API.
This project is splitted up in 2 components: API and Scrapper.

### API
Responsible for exposing a query service through an API.


### Scrapper
Responsible for consuming downloading and saving Github Repo and User data.


## Quick Start

0. Install `docker` and `docker-compose`
1. Clone this project
2. Run `make install`
    * This command will build the images and initialize the database
3. Start the API with `make start-api` or the Scrapper with `make start-scrapper`
4. Open `http://localhost:8002/` in your browser
5. Open `http://localhost:8002/users/_search` to search users
    * Search by `name`. Ex: `http://localhost:8002/users/_search?name=Lucas`
6. Open `http://localhost:8002/repositories/_search` to search users
    * Search by `name`. Ex: `http://localhost:8002/repositories/_search?name=Git`
    * Search by `languages`. Ex: `http://localhost:8002/repositories/_search?languages=Python`
    * Search by `author`. Ex: `http://localhost:8002/repositories/_search?author=Lucas`


## Improvements points
* Better management of connections with SQLAlchemy / Better async configuration for database queries
* Use postgres / docker
* Add contract tests to the API
* Add tests to the Scrapper
* Use ElasticSearch as a database and enable a better search query system
* Remove the coupling between the repository and the db query system
