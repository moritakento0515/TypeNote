from django.db import models
from django.contrib.auth.models import User

#///////////////////////////////////////////////////////////////////////////////////////////////////
#スコアの種類モデル
class ScoreType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="スコア種類")
    description = models.TextField(blank=True, null=True, verbose_name="説明")  

    def __str__(self):
        return self.name
    
#スコアモデル
class Score(models.Model):
    #多対一のリレーションを持つ
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    score_type = models.ForeignKey(ScoreType, on_delete=models.CASCADE, verbose_name="スコア種類")

    class Meta:
        ordering = ['-timestamp']
     
#目標スコアモデル
class TargetScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score_type = models.ForeignKey(ScoreType, on_delete=models.CASCADE)
    target_score = models.IntegerField(default=3000)

    class Meta:
        unique_together = (("user", "score_type"),)

    def __str__(self):
        return f"{self.user} - {self.score_type.name}: {self.target_score}"
    



#///////////////////////////////////////////////////////////////////////////////////////////////////   
#コミュニティモデル 
class Community(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="コミュニティ名")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_communities", verbose_name="オーナー")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

#コミュニティメンバーモデル
class CommunityMember(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="communities")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("community", "user"),)

    def __str__(self):
        return f"{self.user.username} - {self.community.name}"
    




#///////////////////////////////////////////////////////////////////////////////////////////////////
#ユーザー作成時にユーザープロフィールも作成
#def user_profile_picture_path(instance, filename):
    #""" ユーザーごとのプロフィール画像の保存パス """
    #return f'profile_pictures/{instance.user.id}/{filename}'

#ユーザープロフィールモデル
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100, blank=True, null=True, verbose_name="表示名")
    #profile_picture = models.ImageField(upload_to=user_profile_picture_path, blank=True, null=True, verbose_name="プロフィール画像")
    grade = models.CharField(max_length=100, blank=True, null=True, verbose_name="学年")#3/28追加
    bio = models.TextField(blank=True, null=True, verbose_name="自己紹介")

    def __str__(self):
        return self.nickname or self.user.username
    
