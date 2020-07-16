
[![transpiron_logo](https://i.imgur.com/87CVVqX.png "Transpiron Logo")](https://transpiron.com)

### Django-React-App-Boilerplate ```v.1.0.0```
This boilerplate project is about integrating Django with React. The main purpose of this project is to help setup a development environment for building powerful websites with solid Django-based backend, coupled with the flexibility and impressive UI-centric features of React for frontend implementations.

A project of [```Transpiron```](http://transpiron.com), initially designed by [```maikeruji```](http://maikeruji.com).

## Implementations

**1. Python & Django**
This project uses ```Python``` for the entirety of its backend logic and is using the Python-based web framework ```Django``` for development speed and security.

**2. RESTful API** [source](https://www.django-rest-framework.org/)
This project is designed to process and serve resources using ```Web APIs``` thru ```Django REST Framework (DRF)```.

**3. Cross Origin Resource Sharing (CORS)** [source](https://pypi.org/project/django-cors-headers/)
Since the project implements RESTful API and to allow your resources to get shared across other domains, the project implements ```Django CORS Headers```. Although the library is defined in ```requirements.txt```, you still have the option not to install it in your own project if it is not designed for such purpose.

**4. Role-Based Access Control (RBAC)**
This boilerplate project also comes with a predefined, simple ```RBAC``` models (situated in ```account_app``` app in the ```backend``` hierarchy) for implementing access controls on your modules. You may opt not to use this feature if you don't require it, or design your own RBAC. The ```account_app``` Django application that comes with this project can be totally unimplemented and removed from your own project as to your liking.

**5. Knox Authentication** [source](https://james1345.github.io/django-rest-knox/)
By default, Django uses [```CSRF Tokens```]([https://docs.djangoproject.com/en/3.0/ref/templates/builtins/#std:templatetag-csrf_token](https://docs.djangoproject.com/en/3.0/ref/templates/builtins/#std:templatetag-csrf_token)) for authenticating server requests. While this is great, it has been realized and is believed that it is way better to use token authentication with ```Knox``` for the purpose of this project. The ```django-rest-knox``` library used in this project extends from [```DRF token authentication```]([https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)) with added features that resolve some known setbacks of the default implementations of DRF token authentication system.

**6. Django Channels** [source](https://channels.readthedocs.io/en/latest)
```Channels```, built on a Python specification called [```ASGI```]([https://channels.readthedocs.io/en/latest/asgi.html](https://channels.readthedocs.io/en/latest/asgi.html)), is a Django library that provides extended capabilities such as handling *WebSockets*, *chat protocols*, *IoT protocols*, and more. You may choose not to install this library if you don't require it.

**7. Psycopg2** [source](https://pypi.org/project/psycopg2/)
```Psycopg``` library comes predefined in this boilerplate project in case you decide to integrate ```PostgreSQL```. The decision to use ```psycopg2-binary``` library instead of just ```psycopg``` in this project is based upon [this discussion](https://www.postgresql.org/message-id/CA%2Bmi_8bd6kJHLTGkuyHSnqcgDrJ1uHgQWvXCKQFD3tPQBUa2Bw%40mail.gmail.com) and [this explanation](https://www.psycopg.org/articles/2018/02/08/psycopg-274-released/).

**8. React.js** [source](https://reactjs.org/)
Utilizing a frontend framework in order to provide great UI and UX experiences is now a highly considered standard in web development for drawing in web visitors and making the overall experience highly satisfactory. The advantages of React is being taken advantaged by this project for its purpose of providing UI and UX-centric experiences and for huge assistance in speeding up frontend development.

**9. Babel**
```Babel``` is used in this project for handling ```JSX``` syntax (React's own JavaScript syntax) and converting them into regular JavaScript, as well as handling ```ECMAScript 2015+``` (also known as ```ES6```) syntax.

**10. Webpack**
```Webpack``` is used in this project for *transformation*, *bundling*, and/or *packaging* purposes of our frontend assets.

## Major Tools
- Python 3.7.3 (and up)
- Django 3.0.7
- Django Rest Framework 3.10.3
- Django CORS Headers 3.2.0
- Django REST Knox 4.1.0
- Channels 2.4.0
- Psycopg2 2.7.7

- React 16.13.1
- Webpack 4.43.0
- @babel/core 7.10.2
- babel-loader 8.1.0

## Directory Hierarchy
The project is made in the following directory structure:
```  
.  
+-- _backend  
|	+-- _account_app
|	+-- _config
|	+-- _staticfiles
|	+-- _static-cdn-local
|	+-- _media-cdn-local
|	+-- manage.py
|	+-- requirements.txt
+-- _frontend
|	+-- _dist-build
|	+-- _node_modules
|	+-- _src
|	|	+-- index.html
|	+-- babel.rc
|	+-- package-lock.json
|	+-- package.json
|	+-- README.md
|	+-- webpack.config.dev.js
|	+-- webpack.config.prod.js
+-- .gitignore
+-- license.txt
+-- README.md
```

#### root
The project root includes:
- **```backend```** folder
- **```frontend```** folder
- **```license.txt```** which contains the license text of this project.
- **```.gitignore```** contains the files and folders we intentionally specify to tell Git to ignore tracking for
- **```README.md```** a markdown file that briefly documents this boilerplate project.

#### backend
This folder contains all essential Django codebase with the following files and folders:
- **```config```** folder which serves as the main project folder containing main project configurations. This is where we define our ```settings.py```, main ```urls.py```, ```wsgi.py``` and ```asgi.py``` configurations, etc. 
- **```staticfiles```** folder where static files for devlopment must reside.
- **```static-cdn-local```** folder where static files for production must reside.
- **```media-cdn-local```** contains the media files such as a News post's feature image, user's profile picture, etc.
- **```account_app```** is a Django application built-in to this project for managing accounts (registration, login, authentication) and setting up a simple RBAC implementation structure. As mentioned above, you may choose not to implement this application, use it alongside your own account management application, or totally remove it from the project - it's your call.
- **```db.sqlite3```** is the db.sqlite3 file that gets created after you have interacted to your database connection running SQLite3 for the first time *(i.e. you have created a model, or inserted a record in the database)*. By default, this file is not included in this boilerplate project to allow you to create it yourself and fill it with initial data as to your needs.
- **```manage.py```** allows us to execute commands (i.e. *runserver*, *makemigrations*, *migrate*, *collectstatic*, etc.) via the terminal.
- **```requirements.txt```** is where we define our Django dependencies *(libraries or plugins)*.

#### frontend
This main folder contains all essential frontend configuration and React codebase, with the following files and folders:
- **```dist-build```** contains our build/distribution files for deployment. During production, this contains the `index.html` where your server should point to as the main entry point of your UI.
- **```node_modules```** is where the libraries we've installed from npm reside
- **```src```** contains the actual frontend codebase/source code such as your ```JSX components```, css styles that should be part of the main css bundle, etc. This also contains the `index.html` which serves as the main entry point of the UI for development.
- **```babel.rc```** file that configures our babel implementation
- **```package.json```** contains the metadata of your project and other configurations such as managing npm dependencies, scripts, etc.
- **```package-lock.json```** describes the exact tree that was generated, such that subsequent installs are able to generate identical trees, regardless of intermediate dependency updates [[source]]([https://docs.npmjs.com/configuring-npm/package-lock-json.html](https://docs.npmjs.com/configuring-npm/package-lock-json.html)).
- **```README.md```** contains the React's brief documentation of the React app, its integrations and other information. This was included in the project to add further information on the use of React.
- **```webpack.config.dev.js```** defines the webpack configuration for development.
- **```webpack.config.prod.js```** defines the webpack configuration for production.

## Serving Media and Static Files

This boilerplate project intends the static and media files to be served from Django's ```file access API``` using its ```STATIC_ROOT```, ```MEDIA_ROOT```, ```STATIC_URL```, ```MEDIA_URL```, and ```STATICFILES_DIRS``` settings .

For configuration of this setup in dev mode, please check the ```devServer``` config in ```webpack.config.dev.js```.

For production, check ```webpack.config.prod.js```.


## Recommended Start

- [x] Cloning the project
```
$ git clone
$ cd django-react-app-boilerplate
```
- [x] Removing remote ```origin``` 
```
$ git remote remove origin
```
> Purpose for removing ```origin``` is to detach your copy of this project from the main repo since this copy now belongs to you and you don't want your changes from hereon to be recorded in the main repo.
> You would want to create your own repo and log your changes in it.

- [x] Setting up ```virtual envinronment``` for your Django project and activating it. 
```
$ py -m venv your_desired_virtual_env_name
$ your_desired_virtual_env_name/Scripts/activate.bat
```
>*In this example, we use Python's built-in ```venv``` for managing our virtual environments, but you may use a different one such as ```virtualenvwrapper```*.*
>
> Note:  If you are going to be creating your virtual environment inside the project folder, consider adding the folder to ```.gitignore``` file so changes to any inner files and folders are not tracked by Git.

- [x] Install Django dependencies via ```pip```
> Note: Before you perform pip install, make sure you review
> ```backend/requirements.txt``` first and see what libraries you need to add or remove as to your application's needs
```
$ cd backend
$ pip install -r requirements.txt
```

- [x] Make migration files for ```account_app```
> If you want to implement the ```account_app``` application that is provided in this project, you will need to generate the migration files for the db tables as defined in its ```models.py``` file.
> If you don't want to implement the said app, you may skip this step.
```
$ python manage.py makemigrations
```

- [x] Execute the migration files
> There are migration files that come from some of the Django libraries we have installed. Thus, we must ```migrate``` those into our default database connection (as defined in ```settings.py```) so our project will work well inline with those libraries.
> This will also execute the migration files for ```account_app``` if you run the above ```makemigrations``` command.
```
$ python manage.py migrate
```

- [x] Perform ```collectstatic```
> There are Django libraries we have installed with corresponding assets such as ```django-summernote``` and Django's admin app. We need to perform the ```collectstatic``` command to make those files available in our ```static-cdn-local``` for development and production use.
```
$ python manage.py collectstatic
```

- [x] Run Django server
```
$ python manage.py runserver
```
> If there is no error, your Django should be running by default at ```localhost:3000```. You may change this default configuration by changing ```default_port``` in ```manage.py```

- [x] Open a separate terminal and install React dependecies
```
$ cd django-react-app-boilerplate/frontend
$ npm install
```

- [x] Run React on dev mode
```
$ npm start
```
> If there is no error, your React app should be running by default at ```localhost:3001```. You may change this default configuration in ```package.json```'s ```script``` config.

## Notes

### django-summernote
this plugin is predefined in ```requirements.txt``` in case you need to have a ```Rich Text``` field in your Django admin form. This plugin transforms a simple ```TextField``` to ```Rich Text``` field. Check [here]([https://github.com/summernote/django-summernote](https://github.com/summernote/django-summernote)) for usage.

### Database connections
The project defines ```SQLite 3``` as the default and only database connection enabled in ```settings.py```. However, there are two more connections defined but are initially disabled. These connections use PostgreSQL database engine and were predefined to give you idea on how to define multiple database connections running different database engines and configurations.

> Note: Database connection names must be unique - if you have one that is named 'default', you cannot define another connection with the same name.
> Also, PostgreSQL is dependent on psycopg2-library (as already included in ```requirements.txt```). If you need to define a connection running on other engines (i.e. MySQL), you may need to install appropriate libraries or Python wheel.

### Django Admin
You may check Django's built-in admin portal by going to ```localhost:3000/admin```.  It is required that there is at least 1 superuser created. If you have not created any superuser yet, you may create one by running ```python manage.py createsuperuser```.

### Django Admin heading and title
You may change ```site_heading```, ```site_title```, and ```index_title``` of the Django Admin portal to your liking via ```config/urls.py``` file.

