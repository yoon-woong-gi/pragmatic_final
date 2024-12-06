from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View  # Use View instead of RedirectView

from articleapp.models import Article
from likeapp.models import LikeRecord


@transaction.atomic
def toggle_like(user, article):
    # Check if the user has already liked the article
    like_record = LikeRecord.objects.filter(user=user, article=article)
    if like_record.exists():
        # User has already liked the article, so un-like it
        article.like -= 1
        article.save()
        like_record.delete()
        return 'unliked'
    else:
        # User has not liked the article, so like it
        article.like += 1
        article.save()
        LikeRecord(user=user, article=article).save()
        return 'liked'


@method_decorator(login_required, 'get')
class LikeArticleView(View):  # Changed to View
    def get(self, request, *args, **kwargs):  # Use 'request' here
        user = request.user  # Access user from request object
        article = get_object_or_404(Article, pk=kwargs['pk'])

        # Toggle like functionality
        result = toggle_like(user, article)

        # Prepare the response data
        if result == 'liked':
            message = '좋아요가 반영되었습니다.'
        else:
            message = '좋아요가 취소되었습니다.'

        # Return the updated like count and message as JSON
        return JsonResponse({
            'status': result,
            'like_count': article.like,
            'message': message
        })
