# Interface d'administration Django

## Introduction
Ce document explique comment l'interface d'administration Django est configurée et utilisée dans ce projet. Il est destiné aux débutants qui souhaitent comprendre comment Django fournit une interface puissante pour gérer les données de l'application.

## Qu'est-ce que l'interface d'administration Django?

L'interface d'administration Django est une application intégrée qui fournit une interface utilisateur pour gérer les données de votre site. Elle est:
- Générée automatiquement à partir de vos modèles
- Entièrement personnalisable
- Sécurisée par le système d'authentification de Django
- Prête à l'emploi sans configuration supplémentaire

## Configuration de base

L'interface d'administration est activée par défaut dans le fichier `settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',  # Interface d'administration
    # ...
]
```

Et elle est incluse dans les URLs principales dans `urls.py`:

```python
urlpatterns = [
    path('admin/', admin.site.urls),  # URL de l'interface d'administration
    # ...
]
```

## Enregistrement des modèles

Pour qu'un modèle apparaisse dans l'interface d'administration, il doit être enregistré dans le fichier `admin.py` de son application.

### Enregistrement simple

La façon la plus simple d'enregistrer un modèle est:

```python
from django.contrib import admin
from .models import MyModel

admin.site.register(MyModel)
```

### Enregistrement avec une classe d'administration

Pour personnaliser l'affichage et le comportement d'un modèle dans l'interface d'administration, on utilise une classe d'administration:

```python
from django.contrib import admin
from .models import MyModel

@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):
    # Options de personnalisation
    pass
```

## Configuration de l'administration dans l'application Jobs

L'application Jobs personnalise l'interface d'administration pour tous ses modèles:

```python
from django.contrib import admin
from .models import JobRecord, Contract, Skill, Industry, Candidate, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('type_code', 'description')
    search_fields = ('type_code', 'description')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'location')
    search_fields = ('name', 'email', 'location')
    list_filter = ('location',)

@admin.register(JobRecord)
class JobRecordAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'work_year', 'salary_in_usd', 'experience_level', 
                   'employment_type', 'company_location', 'company_size', 'remote_ratio')
    list_filter = ('work_year', 'experience_level', 'employment_type', 
                  'company_size', 'remote_ratio', 'company_location')
    search_fields = ('job_title', 'candidate__name', 'skills__name', 'industry__name')
    filter_horizontal = ('skills',)
    fieldsets = (
        ('Job Information', {
            'fields': ('job_title', 'work_year', 'experience_level', 'employment_type')
        }),
        ('Salary Information', {
            'fields': ('salary', 'salary_currency', 'salary_in_usd')
        }),
        ('Company Information', {
            'fields': ('company_location', 'company_size', 'remote_ratio', 'industry')
        }),
        ('Candidate Information', {
            'fields': ('candidate', 'employee_residence')
        }),
        ('Skills', {
            'fields': ('skills',)
        }),
    )
```

## Configuration de l'administration dans l'application Feedbacks

L'application Feedbacks personnalise également son modèle dans l'interface d'administration:

```python
from django.contrib import admin
from .models import Feedbacks

@admin.register(Feedbacks)
class FeedbacksAdmin(admin.ModelAdmin):
    list_display = ('job', 'author', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('comment', 'job__job_title__name', 'author__name')
```

## Options de personnalisation

### list_display

Définit les colonnes à afficher dans la liste des objets:

```python
list_display = ('job_title', 'work_year', 'salary_in_usd')
```

### list_filter

Ajoute des filtres dans la barre latérale:

```python
list_filter = ('work_year', 'experience_level', 'employment_type')
```

### search_fields

Ajoute une barre de recherche et définit les champs à rechercher:

```python
search_fields = ('job_title', 'candidate__name', 'skills__name')
```

### filter_horizontal

Améliore l'interface pour les champs ManyToMany:

```python
filter_horizontal = ('skills',)
```

### fieldsets

Organise les champs en sections dans le formulaire d'édition:

```python
fieldsets = (
    ('Job Information', {
        'fields': ('job_title', 'work_year', 'experience_level', 'employment_type')
    }),
    ('Salary Information', {
        'fields': ('salary', 'salary_currency', 'salary_in_usd')
    }),
    # ...
)
```

### readonly_fields

Définit les champs qui ne peuvent pas être modifiés:

```python
readonly_fields = ('created_at',)
```

### inlines

Permet d'éditer des modèles liés sur la même page:

```python
class FeedbackInline(admin.TabularInline):
    model = Feedbacks
    extra = 1

class JobRecordAdmin(admin.ModelAdmin):
    inlines = [FeedbackInline]
    # ...
```

## Personnalisation avancée

### Actions personnalisées

Vous pouvez ajouter des actions personnalisées dans l'interface d'administration:

```python
@admin.register(JobRecord)
class JobRecordAdmin(admin.ModelAdmin):
    actions = ['mark_as_featured']

    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
    mark_as_featured.short_description = "Marquer comme mis en avant"
```

### Méthodes d'affichage personnalisées

Vous pouvez ajouter des colonnes calculées dans la liste des objets:

```python
@admin.register(JobRecord)
class JobRecordAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'work_year', 'salary_in_usd', 'get_skills_count')

    def get_skills_count(self, obj):
        return obj.skills.count()
    get_skills_count.short_description = 'Nombre de compétences'
```

### Personnalisation des formulaires

Vous pouvez personnaliser les formulaires utilisés dans l'interface d'administration:

```python
from django import forms

class JobRecordAdminForm(forms.ModelForm):
    class Meta:
        model = JobRecord
        fields = '__all__'
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 5}),
        }

@admin.register(JobRecord)
class JobRecordAdmin(admin.ModelAdmin):
    form = JobRecordAdminForm
    # ...
```

## Sécurité de l'interface d'administration

L'interface d'administration est protégée par le système d'authentification de Django:

- Seuls les utilisateurs avec `is_staff=True` peuvent accéder à l'interface d'administration
- Les permissions déterminent quelles actions un utilisateur peut effectuer
- Les groupes permettent de gérer les permissions pour plusieurs utilisateurs

### Permissions

Django crée automatiquement des permissions pour chaque modèle:

- `add_modelname`: Peut ajouter un objet
- `change_modelname`: Peut modifier un objet
- `delete_modelname`: Peut supprimer un objet
- `view_modelname`: Peut voir un objet

Vous pouvez restreindre l'accès à certaines actions dans l'interface d'administration:

```python
@admin.register(JobRecord)
class JobRecordAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        # Seuls les superutilisateurs peuvent supprimer des objets
        return request.user.is_superuser
```

## Utilisation de l'interface d'administration

### Accès à l'interface d'administration

L'interface d'administration est accessible à l'URL `/admin/` (par défaut). Vous devez vous connecter avec un compte utilisateur ayant `is_staff=True`.

### Création d'un superutilisateur

Pour créer un superutilisateur (qui a accès à toutes les fonctionnalités de l'interface d'administration), utilisez la commande:

```bash
python manage.py createsuperuser
```

### Navigation dans l'interface d'administration

L'interface d'administration est organisée par application et par modèle:

1. **Page d'accueil**: Liste toutes les applications et leurs modèles
2. **Page de liste**: Affiche tous les objets d'un modèle avec des filtres et une barre de recherche
3. **Page de détail**: Permet d'ajouter ou de modifier un objet

### Fonctionnalités principales

- **Ajout d'objets**: Formulaires générés automatiquement avec validation
- **Modification d'objets**: Formulaires pré-remplis avec les données existantes
- **Suppression d'objets**: Confirmation avant suppression
- **Actions en masse**: Appliquer une action à plusieurs objets sélectionnés
- **Historique**: Suivi des modifications apportées aux objets

## Bonnes pratiques

### Personnalisation de l'en-tête et du titre

Vous pouvez personnaliser l'en-tête et le titre de l'interface d'administration:

```python
# Dans admin.py
admin.site.site_header = "Administration du projet Jobs"
admin.site.site_title = "Portail d'administration"
admin.site.index_title = "Bienvenue dans l'administration du projet Jobs"
```

### Organisation des modèles

Pour une meilleure organisation, vous pouvez regrouper les modèles liés:

```python
# Dans apps.py
class JobsConfig(AppConfig):
    name = 'jobs'
    verbose_name = 'Gestion des offres d'emploi'
```

### Optimisation des requêtes

Pour améliorer les performances, utilisez `list_select_related` et `list_prefetch_related`:

```python
@admin.register(JobRecord)
class JobRecordAdmin(admin.ModelAdmin):
    list_select_related = ('job_title', 'experience_level', 'employment_type')
    # ...
```

## Conclusion

L'interface d'administration Django est un outil puissant qui permet de:
- Gérer facilement les données de votre application
- Personnaliser l'affichage et le comportement de chaque modèle
- Contrôler l'accès aux fonctionnalités administratives
- Effectuer des opérations en masse sur les données

Ce projet utilise l'interface d'administration pour gérer les offres d'emploi, les compétences, les candidats et les avis, avec une personnalisation adaptée à chaque modèle.