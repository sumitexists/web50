from django.urls import path

from . import views
app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.topic , name = "topic"),
    path("NewPage/", views.NewPage, name = 'NewPage'),
    path("EditPage/<str:title>/", views.EditPage, name = 'EditPage'),
    path("RandomPage/", views.RandomPage , name = "RandomPage"),
    path("Search/", views.Search , name = "search"),
    path("result/<str:title>", views.Result, name = 'result')
]
