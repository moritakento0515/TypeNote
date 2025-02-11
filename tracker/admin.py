from django.contrib import admin
from .models import Score, UserProfile

# Register your models here.
@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'timestamp')
    list_filter = ('user',)
    search_fields = ('user__username',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'target_score', 'comminity')
    list_filter = ('target_score',)
    search_fields = ('user__username', 'comminity')