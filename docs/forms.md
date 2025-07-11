# Formulaires Django

## Introduction
Ce document explique comment les formulaires sont utilisés dans ce projet Django. Il est destiné aux débutants qui souhaitent comprendre comment Django gère la validation et le traitement des données soumises par les utilisateurs.

## Qu'est-ce qu'un formulaire Django?

Dans Django, un formulaire est une classe Python qui:
- Définit les champs à afficher
- Valide les données soumises
- Convertit les données en types Python appropriés
- Peut être lié à un modèle pour faciliter la création et la mise à jour d'objets

## Types de formulaires dans Django

Django propose deux types principaux de formulaires:

1. **Form**: Formulaire standard, non lié à un modèle
2. **ModelForm**: Formulaire généré automatiquement à partir d'un modèle

Ce projet utilise principalement des `ModelForm` pour simplifier la création et la mise à jour d'objets.

## Formulaires dans l'application Jobs

### JobForm

Le formulaire principal de l'application Jobs est `JobForm`:

```python
from django import forms
from .models import JobRecord

class JobForm(forms.ModelForm):
    class Meta:
        model = JobRecord
        fields = [
            'work_year', 'experience_level', 'employment_type', 'job_title',
            'salary', 'salary_currency', 'salary_in_usd', 'employee_residence',
            'remote_ratio', 'company_location', 'company_size', 'skills',
            'industry', 'candidate'
        ]
```

Ce formulaire:
- Est basé sur le modèle `JobRecord`
- Inclut tous les champs du modèle
- Génère automatiquement les widgets appropriés pour chaque type de champ

## Formulaires dans l'application Feedbacks

### FeedbackForm

Le formulaire principal de l'application Feedbacks est `FeedbackForm`:

```python
from django import forms
from .models import Feedbacks

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

Ce formulaire:
- Est basé sur le modèle `Feedbacks`
- Inclut tous les champs du modèle
- Ajoute une validation personnalisée pour le champ `rating`

## Classe Meta dans les ModelForm

La classe `Meta` dans un `ModelForm` définit les métadonnées du formulaire:

```python
class Meta:
    model = JobRecord  # Le modèle sur lequel le formulaire est basé
    fields = [...]     # Les champs à inclure dans le formulaire
    # Autres options possibles:
    # exclude = [...]  # Les champs à exclure du formulaire
    # widgets = {...}  # Widgets personnalisés pour certains champs
    # labels = {...}   # Étiquettes personnalisées pour certains champs
    # help_texts = {...}  # Textes d'aide pour certains champs
    # error_messages = {...}  # Messages d'erreur personnalisés
```

## Validation des formulaires

Django valide automatiquement les formulaires en fonction des contraintes définies dans les modèles. Vous pouvez également ajouter des validations personnalisées:

### Validation au niveau du champ

```python
def clean_rating(self):
    rating = self.cleaned_data.get('rating')
    if rating < 1 or rating > 5:
        raise forms.ValidationError("Rating must be between 1 and 5.")
    return rating
```

Cette méthode:
- Est appelée lors de la validation du formulaire
- Vérifie que la valeur du champ `rating` est entre 1 et 5
- Lève une exception `ValidationError` si la validation échoue
- Retourne la valeur validée

### Validation au niveau du formulaire

```python
def clean(self):
    cleaned_data = super().clean()
    start_date = cleaned_data.get('start_date')
    end_date = cleaned_data.get('end_date')
    
    if start_date and end_date and start_date > end_date:
        raise forms.ValidationError("La date de début ne peut pas être postérieure à la date de fin.")
    
    return cleaned_data
```

Cette méthode:
- Est appelée après la validation de chaque champ
- Permet de valider plusieurs champs ensemble
- Lève une exception `ValidationError` si la validation échoue
- Retourne les données validées

## Utilisation des formulaires dans les vues

### Affichage d'un formulaire

```python
def job_create(request):
    if request.method == 'POST':
        # Traitement du formulaire soumis
        # ...
    else:
        form = JobForm()  # Création d'un formulaire vide
    
    return render(request, 'jobs/job_form.html', {'form': form})
```

### Traitement d'un formulaire soumis

```python
def job_create(request):
    if request.method == 'POST':
        form = JobForm(request.POST)  # Création d'un formulaire avec les données soumises
        if form.is_valid():  # Validation du formulaire
            job = form.save()  # Sauvegarde des données dans la base de données
            return redirect('job_detail', pk=job.pk)  # Redirection vers la page de détail
    else:
        form = JobForm()
    
    return render(request, 'jobs/job_form.html', {'form': form})
```

### Mise à jour d'un objet existant

```python
def job_update(request, pk):
    job = get_object_or_404(JobRecord, pk=pk)  # Récupération de l'objet à mettre à jour
    
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)  # Création d'un formulaire avec les données soumises et l'instance existante
        if form.is_valid():
            job = form.save()
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm(instance=job)  # Création d'un formulaire pré-rempli avec les données de l'instance
    
    return render(request, 'jobs/job_form.html', {'form': form})
```

## Affichage des formulaires dans les templates

### Affichage simple

```html
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Enregistrer</button>
</form>
```

Cette méthode:
- Affiche tous les champs du formulaire
- Utilise des balises `<p>` pour chaque champ
- Inclut les étiquettes, les widgets et les messages d'erreur

### Affichage personnalisé

```html
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
</form>
```

Cette méthode:
- Permet un contrôle total sur l'affichage de chaque champ
- Permet d'ajouter des classes CSS et d'autres attributs
- Permet de personnaliser l'affichage des erreurs

## Widgets

Les widgets sont les éléments HTML utilisés pour afficher les champs du formulaire. Django choisit automatiquement le widget approprié en fonction du type de champ, mais vous pouvez les personnaliser:

```python
class JobForm(forms.ModelForm):
    class Meta:
        model = JobRecord
        fields = [...]
        widgets = {
            'work_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'job_title': forms.Select(attrs={'class': 'form-control'}),
            'skills': forms.CheckboxSelectMultiple(),
            'comment': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        }
```

## Formulaires avec fichiers

Pour les formulaires qui incluent des fichiers (comme des images), vous devez:

1. Ajouter `enctype="multipart/form-data"` à la balise `<form>`
2. Passer `request.FILES` au formulaire

```html
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Enregistrer</button>
</form>
```

```python
def profile_update(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    
    return render(request, 'profile_form.html', {'form': form})
```

## Bonnes pratiques

### Validation côté client et côté serveur

Django effectue la validation côté serveur, mais il est recommandé d'ajouter également une validation côté client pour une meilleure expérience utilisateur:

```html
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const ratingInput = document.getElementById('id_rating');
        
        ratingInput.addEventListener('input', function() {
            const value = parseInt(this.value);
            if (value < 1 || value > 5) {
                this.setCustomValidity('La note doit être entre 1 et 5.');
            } else {
                this.setCustomValidity('');
            }
        });
    });
</script>
```

### Messages de réussite

Il est recommandé d'afficher des messages de réussite après le traitement d'un formulaire:

```python
from django.contrib import messages

def job_create(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save()
            messages.success(request, "L'offre d'emploi a été créée avec succès.")
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm()
    
    return render(request, 'jobs/job_form.html', {'form': form})
```

```html
{% if messages %}
<div class="messages">
    {% for message in messages %}
    <div class="alert alert-{{ message.tags }}">
        {{ message }}
    </div>
    {% endfor %}
</div>
{% endif %}
```

## Conclusion

Les formulaires Django sont un outil puissant pour:
- Collecter des données auprès des utilisateurs
- Valider ces données
- Créer ou mettre à jour des objets dans la base de données

Ce projet utilise des `ModelForm` pour simplifier la création et la mise à jour d'offres d'emploi et d'avis, avec des validations personnalisées pour garantir l'intégrité des données.