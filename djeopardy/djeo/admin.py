from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from djeo.models import FinalJeopardy, Contestant

class FinalJeopardyAdmin(admin.ModelAdmin):
	list_display = ('air_date','category', 'clue_text', 'correct_answer','game_number','game_id')    
	list_filter = ('air_date',)
	ordering = ('air_date',)

class ContestantInline(admin.StackedInline):
	model = Contestant
	can_delete = False
	verbose_name_plural = 'contestant'

class UserAdmin(UserAdmin):
	inlines = (ContestantInline, )

admin.site.register(FinalJeopardy, FinalJeopardyAdmin)
admin.site.register(Contestant)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
