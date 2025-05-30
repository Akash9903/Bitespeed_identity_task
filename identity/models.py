from django.db import models

class Contact(models.Model):
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    linked_id = models.IntegerField(null=True, blank=True)  # Points to primary contact
    link_precedence = models.CharField(
        max_length=10,
        choices=[('primary', 'primary'), ('secondary', 'secondary')],
        default='primary'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
