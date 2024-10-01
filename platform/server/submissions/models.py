from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Submission(models.Model):
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    content_file = models.FileField(upload_to='submission_files/', null=True, blank=True)
    submission_date = models.DateField(auto_now_add=True)
    authors = models.ManyToManyField(User, related_name='authored_papers')
    reviewers = models.ManyToManyField(User, related_name='assigned_reviews', blank=True)
    review_status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('reviewed', 'Reviewed')], default='pending')
    categories = models.JSONField(blank=True, default=list)  # Store predicted topical categories here

    def __str__(self):
        return self.title

class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    submission = models.ForeignKey('Submission', on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField() 
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.reviewer} on {self.submission}'

class ReviewRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_requests')
    submission = models.ForeignKey('Submission', on_delete=models.CASCADE, related_name='review_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"ReviewRequest for {self.submission.title} to {self.reviewer.username}"