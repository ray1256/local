from django.contrib import admin
from .models import Author,Genre,Books,BookInstance

# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(BookInstance)

class BookInline(admin.TabularInline):
    # 因為ForeignKey
    # Book裡面 外鍵 Author
    model = Books

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name','first_name','date_of_birth','date_of_death')
    fields = ['first_name','last_name',('date_of_birth','date_of_death')]

    inline = [BookInline]


admin.site.register(Author,AuthorAdmin)

class BooksInstanceInline(admin.TabularInline):
    # 因為有ForeignKey
    # BookInstance裡面 外鍵 Book
    model = BookInstance




@admin.register(Books)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','author','display_genre')
    # 很不幸地，我們無法直接在 list_display 中指定「書籍類別」(genre field)字段，
    # 因為它是一個 ManyToManyField (多對多字段)，因為如果這樣做會造成很大的資料庫讀寫「成本」
    # 所以 Django 會預防這樣的狀況發生，因此
    # 取而代之，我們將定義一個 display_genre 函式以「字串」形式得到書籍類別。
    inlines = [BooksInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    # list_display:是用來overwrite Author類別的__str__(self)函式的
    # 原本__str__(self)只是用來顯示lastname + firstname而已
    # 現在改寫成lastname, firstname, date_of_birth, date_of_death
    list_diplay = ('books','status','borrower','due_back')
    list_filter = ('status','due_back')
    # fields:
    # 用來基本客製化顯示的欄位的順序（編輯資料時）
    # 預設的系統排列方式，是垂直的一個一個欄位顯示
    # 以下的方式，就可以把date_of_birth, date_of_death放在同一列
    fieldsets = (
        ('Basic Info',{'fields':('books','imprint','borrower','id')}),
        ('Availability',{'fields':('status','due_back')}),
    )
