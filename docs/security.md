# Sécurité dans Django

## Introduction
Ce document explique les fonctionnalités de sécurité utilisées dans ce projet Django. Il est destiné aux débutants qui souhaitent comprendre comment Django protège l'application contre les vulnérabilités courantes.

## Authentification et Autorisation

### Système d'authentification intégré

Django fournit un système d'authentification complet qui est utilisé dans ce projet:

```python
INSTALLED_APPS = [
    'django.contrib.auth',  # Système d'authentification
    # ...
]

MIDDLEWARE = [
    # ...
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Middleware d'authentification
    # ...
]
```

Ce système gère:
- Les utilisateurs et les groupes
- Les permissions
- Les sessions utilisateur
- L'interface d'administration sécurisée

### REST Framework Authentication

Pour l'API REST, le projet utilise l'authentification par token:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

Cela signifie que:
- Chaque utilisateur reçoit un token unique
- Ce token doit être inclus dans l'en-tête HTTP pour accéder à l'API
- Par défaut, l'authentification est requise pour tous les endpoints API

### Permissions

Dans les vues API, le projet utilise `IsAuthenticatedOrReadOnly`:

```python
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class JobRecordViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    # ...
```

Cette permission permet:
- À tous les utilisateurs (même non authentifiés) de lire les données (GET)
- Uniquement aux utilisateurs authentifiés de modifier les données (POST, PUT, DELETE)

## Protection contre les attaques courantes

### Protection CSRF

Django inclut une protection contre les attaques CSRF (Cross-Site Request Forgery):

```python
MIDDLEWARE = [
    # ...
    'django.middleware.csrf.CsrfViewMiddleware',
    # ...
]
```

Dans les templates, le tag `{% csrf_token %}` est utilisé dans tous les formulaires:

```html
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Envoyer</button>
</form>
```

### Protection XSS

Django se protège contre les attaques XSS (Cross-Site Scripting) par:
- L'échappement automatique des variables dans les templates
- L'utilisation du système de templates qui échappe automatiquement le HTML

### Protection contre l'injection SQL

Django utilise un ORM (Object-Relational Mapping) qui:
- Paramétrise automatiquement les requêtes SQL
- Évite les injections SQL en séparant les données des requêtes

### Clickjacking Protection

Le middleware XFrameOptionsMiddleware protège contre le clickjacking:

```python
MIDDLEWARE = [
    # ...
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # ...
]
```

Cela ajoute l'en-tête HTTP `X-Frame-Options` qui empêche le site d'être affiché dans un iframe.

## Validation des données

### Validation des formulaires

Les formulaires Django valident automatiquement les données:

```python
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedbacks
        fields = ['job', 'author', 'comment', 'rating']
        
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating
```

### Validation des modèles

Les modèles utilisent des validateurs pour garantir l'intégrité des données:

```python
from django.core.validators import MinValueValidator, MaxValueValidator

class Feedbacks(models.Model):
    # ...
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    # ...
```

## Sécurité des mots de passe

Django utilise des algorithmes de hachage sécurisés pour les mots de passe:

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

Ces validateurs garantissent que:
- Les mots de passe ne sont pas trop similaires aux informations de l'utilisateur
- Les mots de passe ont une longueur minimale
- Les mots de passe courants sont rejetés
- Les mots de passe ne sont pas entièrement numériques

## Bonnes pratiques de sécurité

### Clé secrète

La clé secrète est utilisée pour signer les cookies et d'autres données sensibles:

```python
SECRET_KEY = 'django-insecure-6d9#iscz(-&rc#-2nn6x#933#c9wngh!*01#myjwa2&7$tv4#w'
```

**Note importante**: Dans un environnement de production, cette clé devrait être:
- Gardée secrète
- Stockée en dehors du code source (variables d'environnement)
- Différente entre les environnements de développement et de production

### Mode DEBUG

Le mode DEBUG est activé dans ce projet:

```python
DEBUG = True
```

**Note importante**: En production, DEBUG devrait être désactivé (False) car il peut exposer des informations sensibles.

## Conclusion

Django fournit de nombreuses fonctionnalités de sécurité par défaut, mais il est important de:
- Comprendre ces mécanismes
- Suivre les bonnes pratiques
- Rester à jour avec les dernières versions de Django
- Configurer correctement l'application pour la production