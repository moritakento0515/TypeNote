from django.contrib import admin
from .models import Score, UserProfile, ScoreType, TargetScore, Community, CommunityMember

# Register your models here.



@admin.register(ScoreType)
class ScoreTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    search_fields = ('name',)

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'score_type', 'timestamp',)
    list_filter = ('score_type', 'user',)
    search_fields = ('user__username',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # 'get_communities' はユーザーが所属するコミュニティの名前をカンマ区切りで返す
    list_display = ('user', 'get_communities',)
    search_fields = ('user__username',)

    def get_communities(self, obj):
        # ユーザーの関連名 'communities' は CommunityMember オブジェクトのリストを返すので、
        # そこから各コミュニティの名前を取り出して結合します。
        return ", ".join([member.community.name for member in obj.user.communities.all()])
    get_communities.short_description = "コミュニティ"

@admin.register(TargetScore)
class TargetScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'score_type', 'target_score',)
    list_filter = ('score_type', 'user',)
    search_fields = ('user__username',)


# CommunityMember を Community 管理画面で inline 編集できるようにする
class CommunityMemberInline(admin.TabularInline):
    model = CommunityMember
    extra = 1  # 新規追加用にフォームを1件表示

@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at',)
    search_fields = ('name',)
    inlines = [CommunityMemberInline]

@admin.register(CommunityMember)
class CommunityMemberAdmin(admin.ModelAdmin):
    list_display = ('community', 'user', 'joined_at',)
    list_filter = ('community', 'user',)
    search_fields = ('community__name', 'user__username',)
