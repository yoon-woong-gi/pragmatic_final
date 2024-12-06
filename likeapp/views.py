from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import RedirectView

from articleapp.models import Article
from likeapp.models import LikeRecord

@transaction.atomic
def toggle_like(user, article):
    # user가 article에 대해 이미 좋아요한 기록이 있는지 확인
    like_record = LikeRecord.objects.filter(user=user, article=article)
    if like_record.exists():
        # 이미 좋아요를 눌렀으므로 이번에는 "좋아요 취소"
        article.like -= 1
        article.save()
        like_record.delete()
        return 'unliked'
    else:
        # 아직 좋아요가 없으므로 "좋아요 추가"
        article.like += 1
        article.save()
        LikeRecord(user=user, article=article).save()
        return 'liked'


@method_decorator(login_required, 'get')
class LikeArticleView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('articleapp:detail', kwargs={'pk': kwargs['pk']})

    def get(self, *args, **kwargs):
        user = self.request.user
        article = get_object_or_404(Article, pk=kwargs['pk'])

        # toggle_like 함수 호출로 좋아요 상태 토글
        result = toggle_like(user, article)
        if result == 'liked':
            messages.add_message(self.request, messages.SUCCESS, '좋아요가 반영되었습니다.')
        else:
            messages.add_message(self.request, messages.SUCCESS, '좋아요가 취소되었습니다.')

        return super(LikeArticleView, self).get(self.request, *args, **kwargs)

