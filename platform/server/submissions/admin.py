from django.contrib import admin
from .models import Submission, Review, ReviewRequest

admin.site.register(Submission)
admin.site.register(Review)
admin.site.register(ReviewRequest)