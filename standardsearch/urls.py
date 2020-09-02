from django.conf.urls import url

from standardsearch.webapp import views

urlpatterns = [
    url("^v1/search$", views.search_v1, name="search_v1"),
    url("^v1/index_ocds$", views.index_ocds, name="index_ocds"),
]
