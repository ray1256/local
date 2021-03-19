from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

class Genre(models.Model):
    name = models.CharField(max_length = 200,help_text='Enter a book genre')

    def __str__(self):
        return self.name

class Books (models.Model):
    title = models.CharField(max_length=200)

    # 作者(author)被宣告為外鍵(ForeignKey)，因此每本書只會有一名作者，但一名作者可能會有多本書(實際上，一本書可能會有多名作者，不過這個案例不會有，所以在別的例子這種作法可能會有問題
    # null = True 表示如果沒有作者的話可以存入Null值
    # on_delete=models.SET_NULL 表示如果某筆作者紀錄被刪除的話，與該作者相關連的欄位都會被設成 Null
    author = models.ForeignKey('Author',on_delete = models.SET_NULL,null = True)
    summary = models.TextField(max_length=1000,help_text='Enter description')
    isbn = models.CharField('ISBN',max_length=13,help_text="Enter ISBN")

    # 「書籍類別」(genre)是一個 ManyToManyField ，因此一本書可以有很多書籍類別，而一個書結類別也能夠對應到很多本書。
    genre = models.ManyToManyField(Genre,help_text = 'Select a genre for this book')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail',args = [str(self.id)])

    # 將顯示利用for 迴圈做出來
    # 回傳用', '作為連接
    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'


import uuid

class BookInstance(models.Model):
    # UUIDField 被用來將 id 字段再這個模型中設定為 primary_key
    # 這類別的字段會分配一個全域唯一的值給每一個實例(instance)
    # 任何一本你能在圖書館找到的書。
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,help_text="Unique ID for")
    books = models.ForeignKey('Books',on_delete=models.SET_NULL,null = True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null = True,blank = True)

    # status 是一個 CharField 字段，用來定義一個選項列表。你可以看到，我們定義了一個包含「鍵-值對元組」的元組(tuple)
    # 並使其成為選項的參數
    LOAN_STATUS = (
        ('m','Maintenance'),
        ('o','On loan'),
        ('a','Available'),
        ('r','Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices = LOAN_STATUS,
        blank = True,
        default = 'm',
        help_text = "Book availability",
    )

    borrower = models.ForeignKey(User, on_delete = models.SET_NULL,null = True,blank = True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        ordering = ['due_back']
        # 之後會被用在templeate內使用 {{ perms.catalog.can_mark_returned }}
        permissions = (("can_mark_returned","Set book as returned"),)

    def __str__(self):
        return f'{self.id}({self.books.title})'

class Author(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null = True,blank = True)
    date_of_death = models.DateField('Died',null = True,blank = True)

    class Meta:
        ordering = ['last_name','first_name']

    def get_absolute_url(self):
        return reverse('author-detail',args = [str(self.id)])

    def __str__(self):
        return f'{self.last_name},{self.first_name}'
