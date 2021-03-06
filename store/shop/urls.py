from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('author/<slug:author_slug>/', views.AuthorDetailView.as_view(), name='author_detail'),

    path('genre/<slug:genre_slug>/', views.book_list, name='book_list_by_genre'),
    path('book/<slug:book_slug>/', views.book_detail, name='book_detail'),
    path('search-res/',
         views.search,
         name='search_results'),
    path('login/', views.signin, name="login"),

]

urlpatterns += [
    path('process/', views.payment_process, name='process'),
    path('done/', views.payment_done, name='done'),
    path('canceled/', views.payment_canceled, name='canceled'),
]
