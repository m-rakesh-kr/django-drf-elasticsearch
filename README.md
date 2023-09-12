# Django DRF Elasticsearch

# If you Want to use this project?

1. Fork/Clone this project using https https://github.com/m-rakesh-kr/django-drf-elasticsearch.git

2. [Install Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html) if you haven't already and make sure it is running on port `9200`.

3. Create and activate a virtual environment:

    ```sh
    $ python3 -m venv venv && source venv/bin/activate
    ```

4. Install the requirements:

    ```sh
    (venv)$ pip install -r requirements.txt
    ```

5. Apply the migrations:

    ```sh
    (venv)$ python manage.py migrate
    ```

6. Populate the database with some test data by running the following command:

    ```sh
    (venv)$ python manage.py populate_db
    ```

7. Create and populate the Elasticsearch index and mapping:

    ```sh
    (venv)$ python manage.py search_index --rebuild
    ```

8. Run the server

    ```sh
    (venv)$ python manage.py runserver
    ```
