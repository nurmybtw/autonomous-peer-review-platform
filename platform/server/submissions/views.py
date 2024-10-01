import requests
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models import Count, Q, Prefetch
from .models import Submission, Review, ReviewRequest
from users.models import Publication
from .serializers import SubmissionSerializer, ReviewSerializer, ReviewRequestSerializer

User = get_user_model()

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        # Automatically add the current user as an author
        data['authors'] = request.user.id
        serializer = self.get_serializer(data=data)
        
        if serializer.is_valid():
            submission = serializer.save()

            # Step 1: Classify the paper abstract
            classify_response = requests.post(
                url=settings.ML_CLASSIFICATION, 
                json={
                    'abstract': submission.abstract
                }
            )
            
            if classify_response.status_code == 200:
                categories = classify_response.json().get('categories')
                submission.categories = categories  # Save the predicted categories
                submission.save()

                # Step 2: Select potential reviewers based on their 
                # past publications in the predicted categories
                reviewers = User.objects.filter(
                    is_reviewer=True,
                ).distinct().prefetch_related(
                    Prefetch('past_publications')
                )

                filtered_reviewers = []
                for reviewer in reviewers:
                    for publication in reviewer.past_publications.all():
                        if set(publication.categories).intersection(set(categories)):  # Check for overlap
                            filtered_reviewers.append(reviewer)
                            break
                print(len(filtered_reviewers))
                # Step 3: Send selected reviewers to the ranking API
                corpus = [
                    {
                        'author_id': reviewer.id,
                        'papers': [publication.abstract for publication in reviewer.past_publications.all()]
                    } for reviewer in filtered_reviewers
                ]

                ranking_response = requests.post(
                    url=settings.ML_RANKING, 
                    json={
                        'abstract': submission.abstract,
                        'corpus': corpus
                    }
                )

                if ranking_response.status_code == 200:
                    ranked_reviewers = ranking_response.json().get('ranking')

                    # Step 4: Assign top-k reviewers to the submission
                    top_k_reviewers = ranked_reviewers[:settings.MAX_REVIEWER_NUMBER]

                    for reviewer_data in top_k_reviewers:
                        reviewer = User.objects.get(id=reviewer_data['author_id'])
                        ReviewRequest.objects.create(
                            reviewer=reviewer,
                            submission=submission,
                            status='pending'
                        )
                        # submission.reviewers.add(reviewer)
                    
                    submission.save()
                    return Response(self.get_serializer(submission).data)

            return Response({'error': 'Classification or reviewer ranking failed'}, status=400)
        return Response(serializer.errors, status=400)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def new_reviewer_request(self, request, pk=None):
        submission = self.get_object()

        # Check if the current user is the author of the submission
        if request.user not in submission.authors.all():
            return Response({'error': 'You are not authorized to request new reviewers for this submission.'}, status=403)

        reviewers = User.objects.filter(
            is_reviewer=True,
            # past_publications__categories__overlap=categories
        ).exclude(
            review_requests__submission=submission,
        ).distinct().prefetch_related(
            Prefetch('past_publications')
        )
        corpus = [
            {
                'author_id': reviewer.id,
                'papers': [publication.abstract for publication in reviewer.past_publications.all()]
            } for reviewer in reviewers
        ]

        ranking_response = requests.post(
            url=settings.ML_RANKING, 
            json={
                'abstract': submission.abstract,
                'corpus': corpus
            }
        )

        if ranking_response.status_code == 200:
            ranked_reviewers = ranking_response.json().get('ranking')

            reviewer = User.objects.get(id=ranked_reviewers[0]['author_id'])
            ReviewRequest.objects.create(
                reviewer=reviewer,
                submission=submission,
                status='pending'
            )
            return Response({'message': 'New review request has been sent.'})
        return Response({'error': 'Probably reviewer ranking failed'}, status=400)

        

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_submissions(self, request):
        submissions = Submission.objects.filter(authors__id=request.user.id)
        
        status = request.query_params.get('status')
        if status == 'pending':
            submissions = submissions.filter(review_status='pending')
        
        serializer = self.get_serializer(submissions, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_reviews(self, request):
        assigned_submissions = Submission.objects.filter(reviewers__id=request.user.id)

        status = request.query_params.get('status')
        if status == 'pending':
            assigned_submissions = assigned_submissions.exclude(
                reviews__reviewer=request.user  # This excludes submissions where the current reviewer has already submitted a review
            )

        serializer = self.get_serializer(assigned_submissions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def submit_review(self, request, pk=None):
        submission = self.get_object()

        # Check if the user is one of the assigned reviewers
        if request.user not in submission.reviewers.all():
            return Response({'error': 'You are not assigned as a reviewer for this submission.'}, status=403)

        # Check if a review has already been submitted
        if Review.objects.filter(reviewer=request.user, submission=submission).exists():
            return Response({'error': 'You have already submitted a review for this submission.'}, status=400)

        # Create a new review
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(reviewer=request.user, submission=submission)

            # Update the submission's review status
            completed_reviews = Review.objects.filter(submission=submission).count()

            if completed_reviews == settings.MAX_REVIEWER_NUMBER:
                submission.review_status = 'reviewed'
                submission.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def reviews(self, request, pk=None):
        submission = self.get_object()
        reviews = Review.objects.filter(submission=submission)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def review_requests(self, request, pk=None):
        submission = self.get_object()

        review_requests = ReviewRequest.objects.filter(submission=submission)
        serializer = ReviewRequestSerializer(review_requests, many=True)
        return Response(serializer.data)

class ReviewRequestViewSet(viewsets.ModelViewSet):
    queryset = ReviewRequest.objects.all()
    serializer_class = ReviewRequestSerializer
    permission_classes = [IsAuthenticated]

    # Custom action for accepting a review request
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def accept(self, request, pk=None):
        review_request = self.get_object()

        # Check if the current user is the reviewer for this request
        if review_request.reviewer != request.user:
            return Response({'error': 'You are not authorized to accept this review request.'}, status=403)

        # Update the review request status to accepted and mark the reviewer as assigned
        review_request.status = 'accepted'
        review_request.save()

        submission = review_request.submission
        submission.reviewers.add(review_request.reviewer)
        submission.save()

        return Response({'message': 'Review request accepted, you are now assigned to the submission.'})

    # Custom action for rejecting a review request
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def reject(self, request, pk=None):
        review_request = self.get_object()

        # Check if the current user is the reviewer for this request
        if review_request.reviewer != request.user:
            return Response({'error': 'You are not authorized to reject this review request.'}, status=403)

        # Update the review request status to rejected
        review_request.status = 'rejected'
        review_request.save()

        submission = review_request.submission

        reviewers = User.objects.filter(
            is_reviewer=True,
            # past_publications__categories__overlap=categories
        ).exclude(
            review_requests__submission=submission,
        ).distinct().prefetch_related(
            Prefetch('past_publications')
        )
        corpus = [
            {
                'author_id': reviewer.id,
                'papers': [publication.abstract for publication in reviewer.past_publications.all()]
            } for reviewer in reviewers
        ]

        ranking_response = requests.post(
            url=settings.ML_RANKING, 
            json={
                'abstract': submission.abstract,
                'corpus': corpus
            }
        )

        if ranking_response.status_code == 200:
            ranked_reviewers = ranking_response.json().get('ranking')

            reviewer = User.objects.get(id=ranked_reviewers[0]['author_id'])
            ReviewRequest.objects.create(
                reviewer=reviewer,
                submission=submission,
                status='pending'
            )
            return Response({'message': 'Review request rejected, you will not be assigned to this submission.'})
        return Response({'error': 'Probably reviewer ranking failed'}, status=400)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_requests(self, request):
        # Get review requests for the current user
        review_requests = ReviewRequest.objects.filter(reviewer=request.user, status='pending').prefetch_related('submission')
        serializer = self.get_serializer(review_requests, many=True)
        return Response(serializer.data)