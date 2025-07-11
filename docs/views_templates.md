# Vues et Templates Django

## Introduction
Ce document explique comment les vues et les templates sont utilisés dans ce projet Django. Il est destiné aux débutants qui souhaitent comprendre comment Django gère l'affichage des données et l'interaction avec l'utilisateur.

## Vues Django

Dans Django, une vue est une fonction ou une classe qui prend une requête web et renvoie une réponse. Les vues sont responsables de:
- Récupérer les données depuis les modèles
- Traiter les formulaires
- Appliquer la logique métier
- Rendre les templates avec les données

## Types de vues dans le projet

### Vues basées sur des fonctions

Le projet utilise principalement des vues basées sur des fonctions. Voici un exemple de la vue `job_list` dans l'application Jobs:

```python
def job_list(request):
    """View function for listing all jobs."""
    # Get search and sort parameters from request
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', '-salary_in_usd')  # Default sort by salary (high to low)
    page = request.GET.get('page', 1)  # Get the page parameter, default to 1

    # Start with all jobs
    jobs = JobRecord.objects.all()

    # Apply search filter if provided
    if search_query:
        jobs = jobs.filter(job_title__name__icontains=search_query)

    # Apply sorting
    jobs = jobs.order_by(sort_by)

    # Apply pagination
    paginator = Paginator(jobs, 10)  # Show 10 jobs per page
    try:
        jobs_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        jobs_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        jobs_page = paginator.page(paginator.num_pages)

    context = {
        'jobs': jobs_page,
        'search_query': search_query,
        'sort_by': sort_by,
    }

    return render(request, 'jobs/job_list.html', context)
```

Cette vue:
1. Récupère les paramètres de recherche, de tri et de pagination
2. Récupère tous les jobs et applique les filtres
3. Applique la pagination
4. Prépare un dictionnaire de contexte avec les données
5. Rend le template avec le contexte

### Vues pour les opérations CRUD

Le projet implémente des vues pour les opérations CRUD (Create, Read, Update, Delete) sur les modèles:

#### Création (Create)

```python
def job_create(request):
    """View function for creating a new job."""
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save()
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm()

    return render(request, 'jobs/job_form.html', {'form': form})
```

#### Lecture (Read)

```python
def job_detail(request, pk):
    """View function for displaying details of a specific job."""
    job = get_object_or_404(JobRecord, pk=pk)
    return render(request, 'jobs/job_detail.html', {'job': job})
```

#### Mise à jour (Update)

```python
def job_update(request, pk):
    """View function for updating an existing job."""
    job = get_object_or_404(JobRecord, pk=pk)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            job = form.save()
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/job_form.html', {'form': form})
```

#### Suppression (Delete)

```python
def job_delete(request, pk):
    """View function for deleting an existing job."""
    job = get_object_or_404(JobRecord, pk=pk)
    if request.method == 'POST':
        # Handle form submission
        # Delete the job
        job.delete()
        # Redirect to the job list page
        return redirect('job_list')
    else:
        # Display the confirmation page
        return render(request, 'jobs/job_confirm_delete.html', {'object': job})
```

### Vues API

Le projet inclut également des vues spécifiques pour l'API:

```python
def job_list_api(request):
    """View function for listing all jobs using API."""
    return render(request, 'jobs/job_list_api.html')

def job_detail_api(request, pk):
    """View function for displaying details of a specific job using API."""
    return render(request, 'jobs/job_detail_api.html')
```

Ces vues ne font que rendre des templates qui utilisent JavaScript pour interagir avec l'API REST.

### Vues spéciales

Le projet inclut également des vues spéciales comme le tableau de bord:

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

def dashboard(request):
    """View function for displaying the dashboard page."""
    return render(request, 'jobs/dashboard.html')
```

## Templates Django

Les templates sont des fichiers HTML qui peuvent contenir des variables, des filtres, des tags et des blocs pour générer du HTML dynamique.

### Structure des templates

Le projet utilise une structure de templates hiérarchique:

1. **Template de base** (`templates/base.html`): Contient la structure HTML commune à toutes les pages
2. **Templates d'application**: Étendent le template de base et ajoutent du contenu spécifique
3. **Templates de détail**: Pour afficher les détails d'un objet spécifique
4. **Templates de formulaire**: Pour créer et modifier des objets
5. **Templates de confirmation**: Pour confirmer la suppression d'objets

### Template de base

Le template de base définit la structure commune et les blocs que les templates enfants peuvent remplacer:

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Django Jobs{% endblock %}</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <!-- Navigation -->
    </nav>

    <div class="container mt-4">
        {% block content %}{% endblock %}
    </div>

    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### Template de liste

Voici un exemple simplifié de template de liste (`jobs/job_list.html`):

```html
{% extends 'base.html' %}

{% block title %}Liste des offres d'emploi{% endblock %}

{% block content %}
    <h1>Offres d'emploi</h1>
    
    <form method="get" class="mb-4">
        <div class="input-group">
            <input type="text" name="search" class="form-control" placeholder="Rechercher..." value="{{ search_query }}">
            <div class="input-group-append">
                <button class="btn btn-outline-secondary" type="submit">Rechercher</button>
            </div>
        </div>
    </form>
    
    <table class="table table-striped">
        <thead>
            <tr>
                <th>Titre</th>
                <th>Année</th>
                <th>Salaire (USD)</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for job in jobs %}
            <tr>
                <td>{{ job.job_title }}</td>
                <td>{{ job.work_year }}</td>
                <td>{{ job.salary_in_usd }}</td>
                <td>
                    <a href="{% url 'job_detail' job.id %}" class="btn btn-sm btn-info">Détails</a>
                    <a href="{% url 'job_update' job.id %}" class="btn btn-sm btn-warning">Modifier</a>
                    <a href="{% url 'job_delete' job.id %}" class="btn btn-sm btn-danger">Supprimer</a>
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="4">Aucune offre d'emploi trouvée.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    
    <!-- Pagination -->
    <nav>
        <ul class="pagination">
            {% if jobs.has_previous %}
            <li class="page-item">
                <a class="page-link" href="?page=1&search={{ search_query }}&sort={{ sort_by }}">Première</a>
            </li>
            <li class="page-item">
                <a class="page-link" href="?page={{ jobs.previous_page_number }}&search={{ search_query }}&sort={{ sort_by }}">Précédente</a>
            </li>
            {% endif %}
            
            <li class="page-item active">
                <span class="page-link">Page {{ jobs.number }} sur {{ jobs.paginator.num_pages }}</span>
            </li>
            
            {% if jobs.has_next %}
            <li class="page-item">
                <a class="page-link" href="?page={{ jobs.next_page_number }}&search={{ search_query }}&sort={{ sort_by }}">Suivante</a>
            </li>
            <li class="page-item">
                <a class="page-link" href="?page={{ jobs.paginator.num_pages }}&search={{ search_query }}&sort={{ sort_by }}">Dernière</a>
            </li>
            {% endif %}
        </ul>
    </nav>
    
    <a href="{% url 'job_create' %}" class="btn btn-success">Ajouter une offre d'emploi</a>
{% endblock %}
```

Ce template:
1. Étend le template de base
2. Définit un titre spécifique
3. Affiche un formulaire de recherche
4. Affiche une table avec les offres d'emploi
5. Inclut des liens pour les actions CRUD
6. Affiche une pagination
7. Inclut un bouton pour créer une nouvelle offre

### Template de détail

Voici un exemple simplifié de template de détail (`jobs/job_detail.html`):

```html
{% extends 'base.html' %}

{% block title %}Détail de l'offre d'emploi{% endblock %}

{% block content %}
    <h1>{{ job.job_title }}</h1>
    
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Informations générales</h5>
            <p><strong>Année:</strong> {{ job.work_year }}</p>
            <p><strong>Niveau d'expérience:</strong> {{ job.experience_level }}</p>
            <p><strong>Type d'emploi:</strong> {{ job.employment_type }}</p>
            <p><strong>Salaire:</strong> {{ job.salary }} {{ job.salary_currency }} ({{ job.salary_in_usd }} USD)</p>
            <p><strong>Lieu de résidence de l'employé:</strong> {{ job.employee_residence }}</p>
            <p><strong>Ratio de télétravail:</strong> {{ job.remote_ratio }}%</p>
            <p><strong>Localisation de l'entreprise:</strong> {{ job.company_location }}</p>
            <p><strong>Taille de l'entreprise:</strong> {{ job.get_company_size_display }}</p>
            
            {% if job.industry %}
            <p><strong>Industrie:</strong> {{ job.industry }}</p>
            {% endif %}
            
            {% if job.candidate %}
            <p><strong>Candidat:</strong> {{ job.candidate }}</p>
            {% endif %}
            
            {% if job.skills.all %}
            <h5 class="mt-3">Compétences requises</h5>
            <ul>
                {% for skill in job.skills.all %}
                <li>{{ skill.name }}</li>
                {% endfor %}
            </ul>
            {% endif %}
        </div>
    </div>
    
    <div class="mt-3">
        <a href="{% url 'job_update' job.id %}" class="btn btn-warning">Modifier</a>
        <a href="{% url 'job_delete' job.id %}" class="btn btn-danger">Supprimer</a>
        <a href="{% url 'job_list' %}" class="btn btn-secondary">Retour à la liste</a>
    </div>
{% endblock %}
```

### Template de formulaire

Voici un exemple simplifié de template de formulaire (`jobs/job_form.html`):

```html
{% extends 'base.html' %}

{% block title %}
    {% if form.instance.id %}Modifier l'offre d'emploi{% else %}Créer une offre d'emploi{% endif %}
{% endblock %}

{% block content %}
    <h1>
        {% if form.instance.id %}Modifier l'offre d'emploi{% else %}Créer une offre d'emploi{% endif %}
    </h1>
    
    <form method="post">
        {% csrf_token %}
        
        <div class="form-group">
            {{ form.job_title.label_tag }}
            {{ form.job_title }}
            {% if form.job_title.errors %}
            <div class="text-danger">
                {{ form.job_title.errors }}
            </div>
            {% endif %}
        </div>
        
        <!-- Autres champs du formulaire -->
        
        <button type="submit" class="btn btn-primary">Enregistrer</button>
        <a href="{% url 'job_list' %}" class="btn btn-secondary">Annuler</a>
    </form>
{% endblock %}
```

### Template API

Le projet inclut également des templates qui utilisent JavaScript pour interagir avec l'API REST:

```html
{% extends 'base.html' %}

{% block title %}Liste des offres d'emploi (API){% endblock %}

{% block content %}
    <h1>Offres d'emploi (API)</h1>
    
    <div id="job-list">
        <p>Chargement des données...</p>
    </div>
    
    <template id="job-template">
        <div class="card mb-3">
            <div class="card-body">
                <h5 class="card-title job-title"></h5>
                <p class="card-text">
                    <strong>Année:</strong> <span class="job-year"></span><br>
                    <strong>Salaire:</strong> <span class="job-salary"></span> USD
                </p>
                <a href="#" class="btn btn-info job-detail">Détails</a>
            </div>
        </div>
    </template>
{% endblock %}

{% block extra_js %}
<script>
    // Fonction pour charger les offres d'emploi depuis l'API
    function loadJobs() {
        fetch('/api/jobs/')
            .then(response => response.json())
            .then(data => {
                const jobList = document.getElementById('job-list');
                jobList.innerHTML = '';
                
                if (data.results.length === 0) {
                    jobList.innerHTML = '<p>Aucune offre d'emploi trouvée.</p>';
                    return;
                }
                
                const template = document.getElementById('job-template');
                
                data.results.forEach(job => {
                    const clone = document.importNode(template.content, true);
                    
                    clone.querySelector('.job-title').textContent = job.job_title_detail.name;
                    clone.querySelector('.job-year').textContent = job.work_year;
                    clone.querySelector('.job-salary').textContent = job.salary_in_usd;
                    
                    const detailLink = clone.querySelector('.job-detail');
                    detailLink.href = `/api/${job.id}/`;
                    
                    jobList.appendChild(clone);
                });
            })
            .catch(error => {
                console.error('Erreur lors du chargement des données:', error);
                document.getElementById('job-list').innerHTML = '<p>Erreur lors du chargement des données.</p>';
            });
    }
    
    // Charger les offres d'emploi au chargement de la page
    document.addEventListener('DOMContentLoaded', loadJobs);
</script>
{% endblock %}
```

## Fonctionnalités des templates Django

### Variables

Les templates Django peuvent afficher des variables avec la syntaxe `{{ variable }}`:

```html
<h1>{{ job.job_title }}</h1>
<p>Salaire: {{ job.salary_in_usd }} USD</p>
```

### Filtres

Les filtres permettent de modifier l'affichage des variables:

```html
<p>Date de création: {{ feedback.created_at|date:"d/m/Y H:i" }}</p>
<p>Commentaire: {{ feedback.comment|truncatewords:50 }}</p>
```

### Tags

Les tags permettent d'ajouter de la logique dans les templates:

```html
{% if user.is_authenticated %}
    <p>Bienvenue, {{ user.username }}!</p>
{% else %}
    <p>Veuillez vous connecter.</p>
{% endif %}

{% for job in jobs %}
    <p>{{ job.job_title }}</p>
{% empty %}
    <p>Aucune offre d'emploi trouvée.</p>
{% endfor %}
```

### Inclusion de templates

Les templates peuvent inclure d'autres templates:

```html
{% include 'jobs/pagination.html' with page=jobs %}
```

### Héritage de templates

L'héritage permet de créer une hiérarchie de templates:

```html
{% extends 'base.html' %}

{% block content %}
    <!-- Contenu spécifique à cette page -->
{% endblock %}
```

## Conclusion

Les vues et les templates Django travaillent ensemble pour:
- Récupérer et traiter les données
- Générer des pages HTML dynamiques
- Gérer les formulaires et les interactions utilisateur
- Afficher les données de manière structurée et cohérente

Ce projet utilise une combinaison de vues basées sur des fonctions et de templates hiérarchiques pour créer une interface utilisateur complète pour la gestion des offres d'emploi et des avis.