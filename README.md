1. Install Docker and docker-compose.
   
For Debian, Ubuntu:

```
su
apt update; apt upgrade -y; apt install -y curl; curl -sSL https://get.docker.com/ | sh; curl -L https://github.com/docker/compose/releases/download/1.28.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose
```

2. Apply environment variables:

```
cp example.env .env
```

3. Change a random string for `SECRET_KEY` and `POSTGRES_PASSWORD` in `.env`.

4. Install dependencies:

```
pipenv install
pipenv shell
```

5. Up docker-compose, migrate database and create super user:

```
docker-compose up -d
python3 app/manage.py makemigrations
python3 app/manage.py migrate
python3 app/manage.py createsuperuser
```

6. Run script (params: "-c" clear database, "-p" 
pass the full path to the file, by default it is taken from .env PATH_CSV )
```
python app/manage.py parse_image_csv -c 
```

7. Run the server:

```
python3 app/manage.py runserver 8080
```
