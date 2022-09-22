# Django Template

[**CUANDO SE CREE UN REPOSITORIO NUEVO CON ESTE TEMPLATE, SE DEBERA GENERAR UNA SECRET KEY Y PONERLA EN SECRET_KEY DE .env.example Y DESCOMENTARLO**](#setup-djangos-secret-key)

## Setup Django's Secret Key
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

[**DESPUES ELEGIR QUE BASE DE DATOS SE USARA EN docker-compose.yml, CAMBIAR EL NOMBRE DEL CONTENEDOR (AHI DIRA) Y ELIMINAR LAS LINEAS COMENTADAS**](#)

[**SI ES NECESARIO, EN LA CARPETA local_dev_db/ TAMBIEN CAMBIAR EL NOMBRE DEL CONTENEDOR AL QUE SE USARA**](#)

**y por ultimo borrar del README.md estas lineas xd (borrar la 1 hasta la 19)**

---
---
---

# ** Nombre del repositorio **
# First time steps

Clone **.env.example** file and rename it as **.env**

## Setup Virtual Enviroment
```bash
#If you have Conda, use "conda deactivate"
python -m venv venv
./venv/Scripts/Activate.ps1 #If you use Linux, use ". ./venv/bin/activate"
pip install -r requirements.txt
```

## Setup development database using Docker (in case of)
```bash
docker-compose up -d
./local_dev_db/import_test_db.ps1 #If you use Linux, use "bash . ./local_dev_db/import_test_db.ps1"
** At this point, MySQL should be running **
```

After doing these steps, see [Run Server](#run-server) and [Development User Login Credentails](#development-user-login-credentails)

# Runtime commands

You'll need these commands in the specified order, to execute the project you'll need to activate the virtual enviroment first, and then start the dockerized database.

## Switch to Virtual Enviroment
```bash
./venv/Scripts/Activate.ps1 #If you use Linux, use ". ./venv/bin/activate"
```

## Start Docker database
```bash
docker-compose start -d
```

## Stop Docker database
```bash
docker-compose stop
```

## Run Django Server
First time run: you should [Run the initial migrations](#run-migrations)
```bash
python manage.py runserver
```

## Create a super-user
```bash
python manage.py createsuperuser
```

## User Login Credentials on Development
This only applies in case there's a database provided with this repository
```bash
Username: --insert here--
Password: --insert here--
```

## Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Create an App

```bash
python manage.py startapp nombreApp
```

----

## To create a working app

1. Create the app and **add its path to the general [*urls.py*](./djangoproject/urls.py) file.** *REMEMBER!* Add it to both **the import & the urlpattern**
2. Add the **app name** to the [*djangoproject/settings.py* file](./djangoproject/settings.py) inside the **INSTALLED_APPS** variable (after the comment in line 37, #Django Project Apps)
3. Copy the [*urls.py*](./exampleApp/urls.py) of the example app into your new one and **change the *app_name* variable** that is written after the imports
4. Copy the [*models.py*](./exampleApp/models.py) and [*forms.py*](./exampleApp/forms.py) of the **exampleApp** and adequate their logic to fit your new app.
5. You'll most probably need to change the [*views.py*](./exampleApp/views.py) logic
6. Finally, change all of the urls from exampleApp (**eg. *exampleApp:index***) for the **app name** that you set.

----

## Create your Virtual Env and install requirements

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Create a superuser for the Django admin

```bash
python manage.py createsuperuser
```

Remember that you have to add your current model into the app's admin.py in order for it to list the entity in the Django Admin


## Create a requirements.txt file

```bash
pip freeze > requirements.txt
```

----

## To preview this markdown file in VSCode

1. Download the Markdown Preview Github Extension
2. Hit **Ctrl + Shift + V**
