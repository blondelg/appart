from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.TextChoices):
    ATTENTE = 'ATTENTE', _('En attente')
    VALIDE = 'VALIDE', _('Valide')
    ERREUR = 'ERREUR', _('En erreur')


class Sources(models.TextChoices):
    LEBONCOIN = 'LEBONCOIN', _('Leboncoin')
    PAP = 'PAP', _('Particuliers à particuliers')

class Annonce(models.Model):
    source = models.CharField(max_length=10, choices=Sources.choices, null=True)
    lien = models.URLField(max_length=200)
    titre = models.CharField(max_length=100, null=True)
    prix = models.IntegerField(null=True)
    surface = models.IntegerField(null=True)
    description = models.TextField(null=True)
    code_postal = models.CharField(max_length=5, null=True)
    date_publication = models.DateField(null=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ATTENTE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['lien']