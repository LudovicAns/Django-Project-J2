# Configuration et Paramètres Django

## Introduction
Ce document explique comment Django est configuré dans ce projet à travers le fichier `settings.py`. Il est destiné aux débutants qui souhaitent comprendre comment les différents paramètres affectent le comportement de l'application.

## Le fichier settings.py

Dans Django, le fichier `settings.py` est le centre de configuration de votre projet. Il contient des paramètres qui déterminent:
- Comment Django interagit avec la base de données
- Quelles applications sont activées
- Comment les URLs sont traitées
- Comment les templates sont rendus
- Et bien plus encore

## Structure du fichier settings.py

Le fichier `settings.py` de ce projet est organisé en plusieurs sections:

### Paramètres de base

```python
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6d9#iscz(-&rc#-2nn6x#933#c9wngh!*01#myjwa2&7$tv4#w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
```

- `BASE_DIR`: Chemin absolu vers le répertoire du projet
- `SECRET_KEY`: Clé secrète utilisée pour la sécurité (signatures, tokens, etc.)
- `DEBUG`: Mode de débogage (à désactiver en production)
- `ALLOWED_HOSTS`: Liste des noms d'hôtes autorisés à servir l'application

### Applications installées

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'jobs.apps.JobsConfig',
    'feedbacks.apps.FeedbacksConfig',
    'rest_framework',
    'rest_framework.authtoken',
]
```

Cette section liste toutes les applications activées dans le projet:
- Applications Django intégrées (`admin`, `auth`, etc.)
- Applications personnalisées (`jobs`, `feedbacks`)
- Applications tierces (`rest_framework`, `rest_framework.authtoken`)

### Middleware

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

Les middlewares sont des composants qui traitent les requêtes et les réponses:
- `SecurityMiddleware`: Ajoute des en-têtes de sécurité
- `SessionMiddleware`: Gère les sessions utilisateur
- `CsrfViewMiddleware`: Protection contre les attaques CSRF
- `AuthenticationMiddleware`: Gère l'authentification des utilisateurs
- `MessageMiddleware`: Gère les messages flash
- `XFrameOptionsMiddleware`: Protection contre le clickjacking

### Configuration de REST Framework

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

Cette section configure Django REST Framework:
- Authentification par token
- Permissions par défaut (authentification requise)
- Pagination (10 éléments par page)

### URLs racine

```python
ROOT_URLCONF = 'asite.urls'
```

Ce paramètre indique quel module contient les configurations d'URL racine.

### Templates

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

Cette section configure le système de templates:
- `BACKEND`: Moteur de templates utilisé
- `DIRS`: Répertoires où chercher les templates
- `APP_DIRS`: Chercher les templates dans les répertoires `templates` des applications
- `OPTIONS`: Options supplémentaires, comme les processeurs de contexte

### WSGI

```python
WSGI_APPLICATION = 'asite.wsgi.application'
```

Ce paramètre indique quel module contient l'application WSGI pour le déploiement.

### Base de données

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

Cette section configure la connexion à la base de données:
- `ENGINE`: Type de base de données (SQLite, PostgreSQL, MySQL, etc.)
- `NAME`: Nom ou chemin de la base de données

### Validation des mots de passe

```python
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

Ces validateurs garantissent que les mots de passe sont suffisamment sécurisés:
- Pas trop similaires aux informations de l'utilisateur
- Longueur minimale
- Pas de mots de passe courants
- Pas uniquement numérique

### Internationalisation

```python
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
```

Ces paramètres configurent l'internationalisation et la localisation:
- `LANGUAGE_CODE`: Langue par défaut
- `TIME_ZONE`: Fuseau horaire
- `USE_I18N`: Activer la traduction
- `USE_TZ`: Utiliser des dates et heures conscientes du fuseau horaire

### Fichiers statiques

```python
STATIC_URL = 'static/'
```

Ce paramètre définit l'URL de base pour les fichiers statiques (CSS, JavaScript, images).

### Clé primaire par défaut

```python
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

Ce paramètre définit le type de champ à utiliser pour les clés primaires auto-incrémentées.

## Paramètres spécifiques à l'environnement

Dans un projet Django bien structuré, les paramètres peuvent varier selon l'environnement (développement, test, production). Voici comment cela pourrait être géré:

### Paramètres de développement

```python
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

### Paramètres de production

```python
DEBUG = False
ALLOWED_HOSTS = ['example.com', 'www.example.com']
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
```

## Bonnes pratiques

### Sécurité

Pour la sécurité, certains paramètres devraient être différents en production:

```python
# En production
DEBUG = False
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Variables d'environnement

Il est recommandé d'utiliser des variables d'environnement pour les informations sensibles:

```python
import os
from dotenv import load_dotenv

load_dotenv()  # Charger les variables depuis .env

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
DATABASE_URL = os.environ.get('DATABASE_URL')
```

### Fichiers de paramètres multiples

Pour gérer différents environnements, vous pouvez utiliser plusieurs fichiers de paramètres:

```
settings/
    __init__.py
    base.py      # Paramètres communs
    dev.py       # Paramètres de développement
    prod.py      # Paramètres de production
    test.py      # Paramètres de test
```

## Configuration des applications

Chaque application Django peut avoir sa propre configuration dans le fichier `apps.py`:

```python
from django.apps import AppConfig

class JobsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jobs'
    verbose_name = 'Gestion des offres d\'emploi'
```

Cette configuration permet de:
- Définir un nom lisible pour l'application
- Configurer des signaux
- Initialiser des ressources

## Paramètres personnalisés

Vous pouvez ajouter vos propres paramètres dans `settings.py`:

```python
# Paramètres personnalisés
MAX_JOBS_PER_USER = 10
DEFAULT_FROM_EMAIL = 'noreply@example.com'
```

Ces paramètres peuvent ensuite être utilisés dans votre code:

```python
from django.conf import settings

if user.jobs.count() >= settings.MAX_JOBS_PER_USER:
    # Limiter le nombre d'offres d'emploi par utilisateur
```

## Accès aux paramètres

Pour accéder aux paramètres dans votre code:

```python
from django.conf import settings

debug_mode = settings.DEBUG
database_name = settings.DATABASES['default']['NAME']
```

## Conclusion

Le fichier `settings.py` est le cœur de la configuration de votre projet Django. Il permet de:
- Configurer les composants de base (base de données, URLs, templates)
- Activer et configurer des applications
- Définir des paramètres de sécurité
- Personnaliser le comportement de Django

Dans ce projet, la configuration est adaptée à un environnement de développement avec SQLite et REST Framework, mais elle devrait être modifiée pour la production avec des paramètres de sécurité renforcés et potentiellement une base de données plus robuste.