from django.contrib import admin
from .models import Score, UserProfile, ScoreType, TargetScore

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
    list_display = ('user', 'comminity',)
    search_fields = ('user__username', 'comminity',)

@admin.register(TargetScore)
class TargetScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'score_type', 'target_score',)
    list_filter = ('score_type', 'user',)
    search_fields = ('user__username',)