from django.urls import path, re_path
from . import views

# path('', views.index, name='index'),

urlpatterns = [
   path('', views.HomePageView.as_view(), name='home'),
   path('about/', views.AboutPageView.as_view(), name='about'),
   path('book/', views.BookListView.as_view(), name='books'),
   path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail')
   # path('country_areas', views.CountryAreaListView.as_view(), name='country_areas'),
   # path('country_areas/<int:pk>', views.CountryAreaDetailView.as_view(), name='country_area_detail'),
   # path('sites/filter', views.SiteFilterView.as_view(), kwargs=None, name='sites_filter'),
   # path('sites/new/', views.SiteCreateView.as_view(), name='site_new'),
   # path('sites/<int:pk>/delete', views.SiteDeleteView.as_view(), name='site_delete'),
   # path('sites/<int:pk>/update/', views.SiteUpdateView.as_view(), name='site_update'),
]
