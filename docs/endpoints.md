# Django Endpoints Documentation

## Introduction
Ce document explique comment les URLs et le routage fonctionnent dans ce projet Django. Il est destiné aux débutants qui souhaitent comprendre comment les requêtes HTTP sont dirigées vers les vues appropriées.

## Structure des URLs dans Django

Dans Django, le routage des URLs est géré par des fichiers `urls.py` qui définissent des "patterns" d'URL. Chaque pattern associe une URL à une vue spécifique qui traitera la requête.

### Fichier URLs principal (asite/urls.py)

Le fichier URLs principal du projet définit les points d'entrée de haut niveau :

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('jobs.urls')),
    path('api/', include('feedbacks.urls')),
    path('jobs/', include('jobs.urls')),
    path('feedbacks/', include('feedbacks.urls')),
]
```

Ce fichier:
- Dirige `/admin/` vers l'interface d'administration Django
- Inclut les URLs de l'application `jobs` sous les préfixes `/api/` et `/jobs/`
- Inclut les URLs de l'application `feedbacks` sous les préfixes `/api/` et `/feedbacks/`

### URLs de l'application Jobs (jobs/urls.py)

L'application Jobs utilise deux types de routage:

1. **Routage API avec DefaultRouter** - Pour les endpoints REST API
```python
jobs_router = DefaultRouter()
jobs_router.register('jobs', views.JobRecordViewSet)

entities_router = DefaultRouter()
entities_router.register('category', views.CategoryViewSet)
entities_router.register('contract', views.ContractViewSet)
# ... autres entités
```

2. **Routage traditionnel avec path()** - Pour les vues basées sur des templates
```python
urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('<int:pk>/', views.job_detail, name='job_detail'),
    path('create/', views.job_create, name='job_create'),
    path('<int:pk>/update/', views.job_update, name='job_update'),
    path('<int:pk>/delete/', views.job_delete, name='job_delete'),
    # ... autres URLs
]
```

### URLs de l'application Feedbacks (feedbacks/urls.py)

L'application Feedbacks suit une structure similaire:

1. **Routage API avec DefaultRouter**
```python
feedbacks_router = DefaultRouter()
feedbacks_router.register('feedbacks', views.FeedbackViewSet)
```

2. **Routage traditionnel**
```python
urlpatterns = [
    path('', views.feedback_list, name='feedback_list'),
    path('<int:pk>/', views.feedback_detail, name='feedback_detail'),
    path('create/', views.feedback_create, name='feedback_create'),
    # ... autres URLs
]
```

## Paramètres d'URL

Django permet de capturer des parties de l'URL comme paramètres:

- `<int:pk>` capture un nombre entier et le passe à la vue sous le nom `pk`
- D'autres convertisseurs incluent `str`, `slug`, `uuid`, etc.

## Nommage des URLs

Chaque URL a un nom unique (`name='job_list'`) qui permet de générer des URLs dans les templates et les vues avec la fonction `reverse()` ou le tag template `{% url %}`.

## Exemple d'utilisation dans les templates

```html
<a href="{% url 'job_detail' job.id %}">Voir le détail</a>
```

## Exemple d'utilisation dans les vues

```python
from django.urls import reverse
redirect(reverse('job_detail', args=[job.id]))
# ou plus simplement
redirect('job_detail', pk=job.id)
```

## Résumé des endpoints principaux

### Interface Web
- `/jobs/` - Liste des offres d'emploi
- `/jobs/<id>/` - Détail d'une offre d'emploi
- `/jobs/create/` - Création d'une offre d'emploi
- `/jobs/<id>/update/` - Modification d'une offre d'emploi
- `/jobs/<id>/delete/` - Suppression d'une offre d'emploi
- `/jobs/dashboard/` - Tableau de bord des offres d'emploi

- `/feedbacks/` - Liste des avis
- `/feedbacks/<id>/` - Détail d'un avis
- `/feedbacks/create/` - Création d'un avis
- `/feedbacks/<id>/update/` - Modification d'un avis
- `/feedbacks/<id>/delete/` - Suppression d'un avis

### API REST
- `/api/jobs/` - API des offres d'emploi
- `/api/category/` - API des catégories
- `/api/contract/` - API des contrats
- `/api/skill/` - API des compétences
- `/api/industry/` - API des industries
- `/api/job-title/` - API des titres d'emploi
- `/api/location/` - API des localisations
- `/api/candidate/` - API des candidats
- `/api/feedbacks/` - API des avis