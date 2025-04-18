from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, HQDog, TpsMoshiDog, DodomaDog, IringaDog,
    HQHorse, DodomaHorse, IringaHorse, TpsMoshiHorse,
    MedicalRecord, Picture, ActivityLog
)

# Custom User admin
admin.site.register(User, UserAdmin)

# Base Animal Admin (for reuse)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed', 'origin', 'gender', 'date_of_birth')
    search_fields = ('name', 'breed', 'origin')
    list_filter = ('gender',)

# Register Dog models with shared admin
admin.site.register(HQDog, AnimalAdmin)
admin.site.register(TpsMoshiDog, AnimalAdmin)
admin.site.register(DodomaDog, AnimalAdmin)
admin.site.register(IringaDog, AnimalAdmin)

# Register Horse models with shared admin
admin.site.register(HQHorse, AnimalAdmin)
admin.site.register(DodomaHorse, AnimalAdmin)
admin.site.register(IringaHorse, AnimalAdmin)
admin.site.register(TpsMoshiHorse, AnimalAdmin)

# Custom Medical Record admin
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('date', 'doctor', 'dog', 'horse')
    search_fields = ('description',)
    list_filter = ('date', 'doctor')

admin.site.register(MedicalRecord, MedicalRecordAdmin)

# Custom Picture admin
class PictureAdmin(admin.ModelAdmin):
    list_display = ('animal_type', 'name', 'location', 'uploaded_by', 'created_at')
    search_fields = ('name', 'related_object_name')
    list_filter = ('animal_type', 'location', 'uploaded_by')

admin.site.register(Picture, PictureAdmin)

# Activity log admin
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp')
    search_fields = ('action', 'user__username')
    list_filter = ('timestamp',)

admin.site.register(ActivityLog, ActivityLogAdmin)
