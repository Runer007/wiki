from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:statia>/", views.statia, name='statia'),
    path("wiki/<str:statiaHead>/edit/", views.edit_page, name='edit_page'),
    path("new_statia/", views.new_statia, name='new_statia'),
    path("search/", views.search, name='search'),
    path("random/", views.random, name='random')
]
