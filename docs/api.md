# API REST avec Django REST Framework

## Introduction
Ce document explique comment l'API REST est implémentée dans ce projet Django à l'aide de Django REST Framework (DRF). Il est destiné aux débutants qui souhaitent comprendre comment créer et utiliser des API REST avec Django.

## Qu'est-ce que Django REST Framework?

Django REST Framework est une puissante bibliothèque qui facilite la création d'API Web. Elle fournit:
- Des sérialiseurs pour convertir les objets Django en JSON/XML et vice-versa
- Des vues spécifiques pour l'API
- Un système d'authentification et de permissions
- Une documentation interactive de l'API
- Et bien plus encore

## Configuration de base

Dans ce projet, DRF est configuré dans `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'rest_framework.authtoken',
]

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

Cette configuration:
- Active l'authentification par token
- Exige l'authentification par défaut
- Configure la pagination avec 10 éléments par page

## Sérialiseurs

Les sérialiseurs convertissent les modèles Django en formats que l'API peut renvoyer (JSON, XML, etc.).

### Exemple de sérialiseur simple (feedbacks/serializer.py)

```python
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedbacks
        fields = ['id', 'job', 'author', 'comment', 'rating', 'created_at']
```

### Exemple de sérialiseur complexe avec relations imbriquées (jobs/serializer.py)

```python
class JobRecordSerializer(serializers.ModelSerializer):
    # Sérialiseurs imbriqués pour les opérations de lecture
    contract_experience = ContractSerializer(read_only=True, source='experience_level')
    job_title_detail = JobTitleSerializer(read_only=True, source='job_title')
    # ...

    class Meta:
        model = JobRecord
        fields = [
            'id', 'job_title', 'job_title_detail', 'work_year',
            # ... autres champs
        ]
```

Les points clés:
- `ModelSerializer` génère automatiquement les champs basés sur le modèle
- `source='experience_level'` indique d'où proviennent les données
- `read_only=True` signifie que ces champs ne sont pas utilisés lors de la création/mise à jour

## ViewSets

Les ViewSets combinent la logique pour un ensemble d'opérations liées. Ils simplifient la création d'API CRUD complètes.

### Exemple de ViewSet simple

```python
class FeedbackViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Feedbacks.objects.all()
    serializer_class = FeedbackSerializer

    search_fields = ['comment']
    ordering_fields = ['created_at', 'rating']
```

### Exemple de ViewSet avec filtrage

```python
class JobRecordViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = JobRecord.objects.all()
    serializer_class = JobRecordSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['job_title__name', 'employee_residence__country_code']
    ordering_fields = ['salary_in_usd', 'created_at']
```

Les points clés:
- `ModelViewSet` fournit automatiquement les opérations CRUD (list, create, retrieve, update, destroy)
- `permission_classes` définit qui peut accéder à l'API
- `filter_backends` permet de filtrer et trier les résultats
- `search_fields` et `ordering_fields` définissent les champs utilisables pour la recherche et le tri

## Routeurs

Les routeurs génèrent automatiquement les URLs pour les ViewSets.

```python
# API router for JobRecord
jobs_router = DefaultRouter()
jobs_router.register('jobs', views.JobRecordViewSet)

# API router for related entities
entities_router = DefaultRouter()
entities_router.register('category', views.CategoryViewSet)
entities_router.register('contract', views.ContractViewSet)
# ...

# URL patterns
urlpatterns = [
    # ...
    # API endpoints
    path('jobs/', include(jobs_router.urls)),
    path('', include(entities_router.urls)),
]
```

Les routeurs créent automatiquement des URLs pour:
- `GET /jobs/` - Liste tous les jobs
- `POST /jobs/` - Crée un nouveau job
- `GET /jobs/{id}/` - Récupère un job spécifique
- `PUT /jobs/{id}/` - Met à jour un job
- `DELETE /jobs/{id}/` - Supprime un job

## API personnalisées

En plus des ViewSets, le projet utilise des vues d'API personnalisées:

```python
@api_view(['GET'])
def dashboard_api(request):
    """API endpoint for dashboard data with job statistics."""
    # Group by job_title__name and calculate aggregated statistics for each group
    job_stats = JobRecord.objects.values('job_title__name').annotate(
        avg_rating=Avg('feedbacks__rating'),
        feedback_count=Count('feedbacks')
    ).filter(feedback_count__gt=0)

    # Prepare data for serialization
    data = []
    for stat in job_stats:
        data.append({
            'job_title': stat['job_title__name'],
            'avg_rating': stat['avg_rating'] if stat['avg_rating'] is not None else 0,
            'feedback_count': stat['feedback_count']
        })

    serializer = DashboardSerializer(data, many=True)
    return Response(serializer.data)
```

Cette vue:
- Est décorée avec `@api_view` pour indiquer qu'elle fait partie de l'API
- Effectue des agrégations complexes sur les données
- Utilise un sérialiseur pour formater la réponse
- Renvoie une `Response` qui sera automatiquement convertie en JSON

## Authentification et permissions

L'API utilise l'authentification par token et des permissions pour contrôler l'accès:

```python
class JobRecordViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    # ...
```

`IsAuthenticatedOrReadOnly` permet:
- À tous les utilisateurs de lire les données (GET)
- Uniquement aux utilisateurs authentifiés de modifier les données (POST, PUT, DELETE)

## Pagination

La pagination est configurée globalement:

```python
REST_FRAMEWORK = {
    # ...
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

Cela limite les résultats à 10 par page et ajoute des liens de pagination dans la réponse:

```json
{
    "count": 100,
    "next": "http://example.com/api/jobs/?page=2",
    "previous": null,
    "results": [
        // 10 items here
    ]
}
```

## Utilisation de l'API

### Exemple de requête avec curl

Pour obtenir la liste des jobs:
```bash
curl -H "Authorization: Token YOUR_TOKEN_HERE" http://localhost:8000/api/jobs/
```

Pour créer un nouveau job:
```bash
curl -X POST -H "Authorization: Token YOUR_TOKEN_HERE" -H "Content-Type: application/json" -d '{"field": "value", ...}' http://localhost:8000/api/jobs/
```

### Exemple d'utilisation avec JavaScript

```javascript
// Récupérer la liste des jobs
fetch('/api/jobs/', {
    headers: {
        'Authorization': 'Token YOUR_TOKEN_HERE'
    }
})
.then(response => response.json())
.then(data => {
    console.log(data);
    // Traiter les données
});

// Créer un nouveau job
fetch('/api/jobs/', {
    method: 'POST',
    headers: {
        'Authorization': 'Token YOUR_TOKEN_HERE',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        // Données du job
    })
})
.then(response => response.json())
.then(data => {
    console.log('Job créé:', data);
});
```

## Conclusion

Django REST Framework simplifie considérablement la création d'API REST en fournissant:
- Des sérialiseurs pour la conversion de données
- Des ViewSets pour les opérations CRUD
- Des routeurs pour la génération d'URLs
- Un système d'authentification et de permissions
- Et bien d'autres fonctionnalités

Ce projet utilise ces fonctionnalités pour créer une API complète et sécurisée pour les jobs et les feedbacks.