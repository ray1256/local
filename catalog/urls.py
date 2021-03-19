#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name = 'index'),
    path('books/',views.BookListView.as_view(),name = 'books'),
    path('book/<int:pk>',views.BookDetailView.as_view(),name = 'book-detail'),
    path('authors/',views.AuthorListView.as_view(),name = "authors"),
    path('author/<int:pk>',views.AuthorDetailView.as_view(),name = 'author-detail'),
]

urlpatterns +=  [
    path('mybooks/',views.LoanedBooksByUserListView.as_view(),name = 'my-borrowed'),
]

urlpatterns += [
    path('book/<uuid:pk>/renew/',views.renew_book_librarian,name = 'renewal-book-librarian'),
]

urlpatterns +=[
    path('author/create/',views.AuthorCreate.as_view(),name = 'author_create'),
    path('author/<int:pk>/update/',views.AuthorUpdate.as_view(),name = 'author_update'),
    path('author/<int:pk>/delete/',views.AuthorDelete.as_view(),name = 'author_delete'),
]
# path()函數定義以下內容：
# URL模式，它是一個空字符串：''。 處理其他視圖時，我們將詳細討論URL模式。
# 如果檢測到URL模式，將調用一個視圖函數：views.index,
# 它是views.py文件中名為index() 的函數。
