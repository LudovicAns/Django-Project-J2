# Modèles Django

## Introduction
Ce document explique comment les modèles Django sont utilisés dans ce projet. Il est destiné aux débutants qui souhaitent comprendre comment Django gère les données et les relations entre elles.

## Qu'est-ce qu'un modèle Django?

Dans Django, un modèle est une classe Python qui représente une table dans la base de données. Chaque attribut de la classe correspond à une colonne dans la table. Django utilise ces modèles pour:
- Créer automatiquement les tables dans la base de données
- Fournir une API Python pour accéder aux données
- Gérer les relations entre les tables

## Modèles de l'application Jobs

L'application Jobs contient plusieurs modèles qui représentent différentes entités liées aux offres d'emploi.

### Modèle JobRecord

Le modèle principal est `JobRecord`, qui représente une offre d'emploi:

```python
class JobRecord(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
    ]

    COMPANY_SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    ]

    # Fields from CSV
    work_year = models.IntegerField()
    experience_level = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='experience_jobs')
    employment_type = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='employment_jobs')
    job_title = models.ForeignKey(JobTitle, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=12, decimal_places=2)
    salary_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    salary_in_usd = models.DecimalField(max_digits=12, decimal_places=2)
    employee_residence = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='employee_jobs')
    remote_ratio = models.IntegerField()
    company_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='company_jobs')
    company_size = models.CharField(max_length=1, choices=COMPANY_SIZE_CHOICES)

    # Relationships
    skills = models.ManyToManyField(Skill, blank=True)
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True, blank=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        # Ensure uniqueness for job_title + work_year + company_location combination
        unique_together = ('job_title', 'work_year', 'company_location')

    def __str__(self):
        return f"{self.job_title} ({self.work_year}) - {self.salary_in_usd} USD"
```

Points importants:
- `CURRENCY_CHOICES` et `COMPANY_SIZE_CHOICES` définissent des choix pour certains champs
- Le modèle utilise plusieurs relations avec d'autres modèles
- `class Meta` définit des métadonnées comme l'unicité de certaines combinaisons de champs
- `__str__` définit comment l'objet sera représenté sous forme de chaîne

### Modèles de référence

Plusieurs modèles plus simples sont utilisés comme références:

```python
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Contract(models.Model):
    type_code = models.CharField(max_length=10, primary_key=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.type_code} - {self.description}"

class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Industry(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class JobTitle(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Location(models.Model):
    country_code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.country_code

class Candidate(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name
```

Ces modèles sont utilisés pour:
- Normaliser la base de données
- Éviter la duplication de données
- Faciliter les recherches et les filtres

## Modèle de l'application Feedbacks

L'application Feedbacks contient un seul modèle:

```python
class Feedbacks(models.Model):
    job = models.ForeignKey(JobRecord, on_delete=models.CASCADE, related_name='feedbacks')
    author = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='feedbacks')
    comment = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.job} by {self.author.name}"
```

Points importants:
- `job` est une clé étrangère vers `JobRecord`
- `author` est une clé étrangère vers `Candidate`
- `rating` utilise des validateurs pour garantir une valeur entre 1 et 5
- `created_at` est automatiquement défini lors de la création

## Types de champs courants

Django propose de nombreux types de champs pour les modèles:

- `CharField`: Pour les chaînes de caractères de longueur limitée
- `TextField`: Pour les textes longs
- `IntegerField`: Pour les nombres entiers
- `DecimalField`: Pour les nombres décimaux précis (comme les montants)
- `BooleanField`: Pour les valeurs booléennes (vrai/faux)
- `DateField`, `TimeField`, `DateTimeField`: Pour les dates et heures
- `EmailField`: Pour les adresses email (avec validation)
- `ForeignKey`: Pour les relations un-à-plusieurs
- `ManyToManyField`: Pour les relations plusieurs-à-plusieurs
- `OneToOneField`: Pour les relations un-à-un

## Types de relations

### ForeignKey (Relation un-à-plusieurs)

```python
experience_level = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='experience_jobs')
```

- `Contract` est le modèle cible
- `on_delete=models.CASCADE` signifie que si le Contract est supprimé, tous les JobRecords associés seront également supprimés
- `related_name='experience_jobs'` permet d'accéder aux JobRecords depuis un Contract avec `contract.experience_jobs.all()`

### ManyToManyField (Relation plusieurs-à-plusieurs)

```python
skills = models.ManyToManyField(Skill, blank=True)
```

- Un JobRecord peut avoir plusieurs Skills
- Une Skill peut être associée à plusieurs JobRecords
- `blank=True` signifie que ce champ est optionnel

## Options de suppression pour les relations

Django propose plusieurs options pour gérer la suppression d'objets liés:

- `CASCADE`: Supprime les objets liés
- `PROTECT`: Empêche la suppression si des objets sont liés
- `SET_NULL`: Met la référence à NULL (nécessite `null=True`)
- `SET_DEFAULT`: Met la référence à la valeur par défaut
- `DO_NOTHING`: Ne fait rien (peut causer des erreurs d'intégrité)

## Métadonnées des modèles

La classe `Meta` permet de définir des métadonnées pour un modèle:

```python
class Meta:
    unique_together = ('job_title', 'work_year', 'company_location')
```

Options courantes:
- `ordering`: Définit l'ordre par défaut des objets
- `verbose_name`, `verbose_name_plural`: Noms pour l'interface d'administration
- `unique_together`: Contraintes d'unicité sur plusieurs champs
- `indexes`: Définit des index pour améliorer les performances

## Méthodes de modèle

Les modèles peuvent avoir des méthodes personnalisées:

```python
def __str__(self):
    return f"{self.job_title} ({self.work_year}) - {self.salary_in_usd} USD"
```

La méthode `__str__` est particulièrement importante car elle définit comment l'objet sera représenté sous forme de chaîne dans:
- L'interface d'administration
- Les shells interactifs
- Les templates Django

## Utilisation des modèles

### Création d'objets

```python
# Création d'un objet
job = JobRecord(
    work_year=2023,
    job_title=job_title,
    salary=100000,
    # ...
)
job.save()

# Ou en une seule étape
job = JobRecord.objects.create(
    work_year=2023,
    job_title=job_title,
    salary=100000,
    # ...
)
```

### Requêtes

```python
# Récupérer tous les objets
all_jobs = JobRecord.objects.all()

# Filtrer les objets
jobs_2023 = JobRecord.objects.filter(work_year=2023)

# Exclure des objets
non_remote_jobs = JobRecord.objects.exclude(remote_ratio=100)

# Récupérer un seul objet
job = JobRecord.objects.get(id=1)

# Ordonner les résultats
high_salary_jobs = JobRecord.objects.order_by('-salary_in_usd')

# Limiter les résultats
top_five_jobs = JobRecord.objects.order_by('-salary_in_usd')[:5]

# Requêtes complexes
jobs = JobRecord.objects.filter(
    work_year=2023,
    company_size='L',
    salary_in_usd__gt=100000
).order_by('-salary_in_usd')
```

### Relations

```python
# Accéder aux objets liés
job = JobRecord.objects.get(id=1)
job_title_name = job.job_title.name
job_skills = job.skills.all()

# Requêtes à travers les relations
jobs_with_python = JobRecord.objects.filter(skills__name='Python')
```

## Migrations

Django utilise des migrations pour gérer les changements de schéma de base de données:

1. Modifier les modèles dans `models.py`
2. Créer une migration: `python manage.py makemigrations`
3. Appliquer la migration: `python manage.py migrate`

Les fichiers de migration sont stockés dans le dossier `migrations/` de chaque application.

## Conclusion

Les modèles Django sont au cœur de toute application Django. Ils:
- Définissent la structure des données
- Gèrent les relations entre les entités
- Fournissent une API pour interagir avec la base de données
- Permettent de valider les données

Ce projet utilise des modèles pour représenter des offres d'emploi, des compétences, des candidats et des avis, avec diverses relations entre eux.