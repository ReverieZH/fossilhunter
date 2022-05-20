from django.contrib import admin
from app import models
# Register your models here.

class SpeciesGuideAdmin(admin.ModelAdmin):
    list_display = ["id", "speciesname", "specieslocation", "epoch", "describe"]

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ["id", "nickname", "status", "institution"]

class NewsListAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "content", "time"]

class MyFossilAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "fossil", "time"]

class FossilFamilyAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "fossil"]

class ReconstrucationModelAdmin(admin.ModelAdmin):
    list_display = ["id", "specie", "modelpath"]

class FossilPictureAdmin(admin.ModelAdmin):
    list_display = ["id", "species", "picturetime", "picturelocation", "document"]

class StudyAdverstationAdmin(admin.ModelAdmin):
    list_display = ["id", "picture", "path"]

class AdverstationAdmin(admin.ModelAdmin):
    list_display = ["id", "picture", "path"]


# 注册Model类
admin.site.register(models.SpeciesGuide, SpeciesGuideAdmin)
admin.site.register(models.FossilPicture, FossilPictureAdmin)
admin.site.register(models.UserInfo, UserInfoAdmin)
admin.site.register(models.NewsList, NewsListAdmin)
admin.site.register(models.MyFossil, MyFossilAdmin)
admin.site.register(models.FossilFamily, FossilFamilyAdmin)
admin.site.register(models.ReconstrucationModel, ReconstrucationModelAdmin)
admin.site.register(models.StudyAdverstation, StudyAdverstationAdmin)
admin.site.register(models.Adverstation, AdverstationAdmin)