from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

#スコアモデル
class Score(models.Model):
    #多対一のリレーションを持つ
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
     
#ユーザープロフィールモデル       
class UserProfile(models.Model):
    #一対一のリレーションを持つ
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    target_score = models.IntegerField(default=3000, verbose_name="目標スコア")
    comminity = models.CharField(max_length=100, blank=True, null=True, verbose_name="コミュニティ")



#ユーザー作成時にユーザープロフィールも作成
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
