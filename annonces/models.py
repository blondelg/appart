from django.db import models


class Annonce(models.Model):
    STATUS_CHOIX = [
        ('ATTENTE', 'ATTENTE'),
        ('VALIDE', 'VALIDE'),
        ('ERREUR', 'ERREUR'),
    ]
    lien = models.URLField(max_length=200)
    titre = models.CharField(max_length=100, null=True)
    prix = models.IntegerField(null=True)
    surface = models.IntegerField(null=True)
    description = models.TextField(null=True)
    code_postal = models.CharField(max_length=5, null=True)
    date_publication = models.DateField(null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOIX, default='ATTENTE',)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['lien']