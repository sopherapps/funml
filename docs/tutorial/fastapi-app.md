# FastAPI App

Then let's set up the FastAPI app which will help our users interact with our bank.

We open the `funml_scdb_tutorial/api.py` module in a suitable text editor.

## Create an instance of FastAPI

Initialize a FastAPI app

```Python hl_lines="6"
{!../docs_src/tutorial/fastapi-app-api.py!}
```

## Create the Route for Creating New Songs

Next, we add a route that will be used to create new songs.
It should handle only POST requests according to the RESTful
API convention.

!!! warning
    We will later replace the `Any` type annotation of `song` with
    an appropriate pydantic so that the request body is automatically
    passed as the argument `song` to
    the handler, thanks to FastAPI. For more details, Check out the 
    [FastAPI docs](https://fastapi.tiangolo.com/tutorial/body/)

```Python hl_lines="9-12"
{!../docs_src/tutorial/fastapi-app-api.py!}
```

## Create the Route for Removing a Given Song

Let's also add a route that will be used to remove songs by title.
It should handle only DELETE requests according to the RESTful
API convention.

!!! note
    There is a path parameter `title` that is automatically passed to the handler
    as the `title` argument. For more details, Check out the 
    [FastAPI docs](https://fastapi.tiangolo.com/tutorial/path-params/)

```Python hl_lines="15-18"
{!../docs_src/tutorial/fastapi-app-api.py!}
```

## Create the Route for Updating a Given Song

Add a route that will be used to update songs.
It should handle only PUT requests according to the RESTful
API convention.

!!! note
    There is a path parameter `title` that is automatically passed to the handler
    as the `title` argument. For more details, Check out the 
    [FastAPI docs](https://fastapi.tiangolo.com/tutorial/path-params/)

!!! warning
    We will later replace the `Any` type annotation of `song` with
    an appropriate pydantic so that the request body is automatically
    passed as the argument `song` to
    the handler, thanks to FastAPI. For more details, Check out the 
    [FastAPI docs](https://fastapi.tiangolo.com/tutorial/body/)

```Python hl_lines="21-24"
{!../docs_src/tutorial/fastapi-app-api.py!}
```

## Create the Route for Getting a Given Song

We add another route. This time, this one will be used to get a song by title.
It should handle only GET requests according to the RESTful
API convention.

!!! note
    There is a path parameter `title` that is automatically passed to the handler
    as the `title` argument. For more details, Check out the 
    [FastAPI docs](https://fastapi.tiangolo.com/tutorial/path-params/)

```Python hl_lines="27-30"
{!../docs_src/tutorial/fastapi-app-api.py!}
```

## Create the Route for Searching for Songs By Title

Finally, we should add a route that will be used to search for songs whose title
begins with the passed query parameter `q`.

It should also handle GET requests according to the RESTful
API convention.

However, this time, there is no title path parameter added.

!!! note
    The query params `q`, `skip` and `limit` are automatically set for us by 
    FastAPI as extracted from the URL. For more details, Check out the 
    [FastAPI docs](https://fastapi.tiangolo.com/tutorial/query-params/)

```Python hl_lines="33-36"
{!../docs_src/tutorial/fastapi-app-api.py!}
```
