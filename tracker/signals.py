from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Community, CommunityMember, UserProfile

# ユーザー作成時にユーザープロフィールを自動生成
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        #print(f"Creating UserProfile for {instance.username}")

# 全ユーザーを「Global」コミュニティに追加
@receiver(post_save, sender=User)
def add_user_to_global_community(sender, instance, created, **kwargs):
    if created:
        #print(f"Adding {instance.username} to Global community")
        # スーパーユーザーがいるか確認し、いなければ作成
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.create_superuser(username="admin", password="xyz80666")
            #print("管理者ユーザー 'admin' を作成しました")

        # Global コミュニティを作成（オーナーはスーパーユーザー）
        global_community, _ = Community.objects.get_or_create(
            name="Global",
            owner=admin_user
        )

        # ユーザーを Global コミュニティに追加
        CommunityMember.objects.get_or_create(community=global_community, user=instance)
        
        