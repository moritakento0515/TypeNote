from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

#スコアの種類モデル
class ScoreType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="スコア種類")
    description = models.TextField(blank=True, null=True, verbose_name="説明")  # 必要なら

    def __str__(self):
        return self.name
    
#スコアモデル
class Score(models.Model):
    #多対一のリレーションを持つ
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    score_type = models.ForeignKey(ScoreType, on_delete=models.CASCADE, null=True, blank=True, verbose_name="スコア種類")

    class Meta:
        ordering = ['-timestamp']
     
#ユーザープロフィールモデル       
class UserProfile(models.Model):
    #一対一のリレーションを持つ
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    comminity = models.CharField(max_length=100, blank=True, null=True, verbose_name="コミュニティ")


#ユーザー作成時にユーザープロフィールも作成
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


class TargetScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score_type = models.ForeignKey(ScoreType, on_delete=models.CASCADE)
    target_score = models.IntegerField(default=3000)

    class Meta:
        unique_together = (("user", "score_type"),)

    def __str__(self):
        return f"{self.user} - {self.score_type.name}: {self.target_score}"

