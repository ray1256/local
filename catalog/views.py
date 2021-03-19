from django.shortcuts import render
from .models import Books, Author, BookInstance, Genre

def index(request):
    # 視圖函數的第一部分使用模型類上的 objects.all() 屬性獲取記錄數
    num_books = Books.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status__exact = 'a').count()

    num_authors = Author.objects.count()
    # 首先獲取 'num_visits'session的密鑰值，如果之前未設置的話那麼就都會是0
    # 每次收到請求後，我們都將增加該值並將其儲存回Session中
    num_visits = request.session.get('num_visits',0)
    request.session['num_visits'] = num_visits+1

    context = {
        'num_books': num_books,
        'num_authors':num_authors,
        'num_instances':num_instances,
        'num_instances_available':num_instances_available,
        'num_visits':num_visits,
    }

    return render(request,'index.html',context = context)
    # 它以原始 request 物件 (一個 HttpRequest), 帶有數據佔位符的HTML模板以及
    # 上下文 context 變量包含將插入到這些佔位符中的數據的Python字典）
    # 為參數。

from django.views import generic
# 我們使用基於類的 通用列表視圖（ListView) 一個繼承自 現有視圖的類
# 因為通用視圖，已經實現了我們需要的大部分功能
class BookListView(generic.ListView):
    # 透過view查詢數據庫，以獲取指定模型(Book)的所有紀錄，呈現在template/catalog/book_list.html
    model = Books
    painate_by = 10
    # context_object_name = 'my_book_list'
    # queryset = Book.objects.filter(title__icontains = "war")[:5]
    # template_name = 'book/my_arbitrary_template_name_list.html'
    '''
    # 因為下面使用的filter 挑選要用的內容
    def get_queryset(self):
        return Book.objects.filter(title__icontains = "tech")[:5]

    def get_context_data(self, **kwargs):
        context = super(BookListView,self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context
    '''
class BookDetailView(generic.DetailView):
    model = Books

    def book_detail_view(request,primary_key):
        try:
            mook = Books.objects.get(pk = primary_key)
        except Book.DoesNotExist:
            raise Http404('Book does not exist')
    # 使用render 配合template_name去顯示 context參數
    ## 後面的context 接 book:Book上的內容
        return render(request,'catalog/book_detail.html',context = {'book':mook})
class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.ListView):
    model = Books

from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name = "catalog/bookinstance_list_borrowed_user.html"
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower = self.request.user).filter(status__exact = 'o').order_by('due_back')


from django.contrib.auth.decorators import permission_required
'''
@permission_required('catalog.can_mark_returned')
@permission_required('catalog.can_edit')

def my_view(request)
'''



from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .forms import RenewBookForm

@permission_required('catalog.can_mark_returned)')
def renew_book_librarian(request,pk):
    # 回傳一個object form 從 (model based) its primary key value
    # 如果沒有則回傳一個Http404 的例外(exception)
    book_inst = get_object_or_404(BookInstance, pk  = pk)


    # 驗證是否為POST
    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renewal_date']
            # 存進 9Model)BookInstance 物件
            book_inst.save()
            # reverse('all-borrowed') 代表使用'all-borrowed' -> url configuration name
            # 就相當等於url tag 之前用模板上的
            return HttpResponseRedirect(reverse('/'))

    # 如果不是POST 就傳遞初始值
    else:
        proposed_renewal_date = datetime.date.today()+datetime.timedelta(weeks = 3)
        # RenewBookForm 原始資料輸入就是(renewal_date)
        # 如果上面的驗證(is_valid)失敗，則預設為初始值
        # 原始參數：{renewal_date:proposed_renewal_date(今天日期加三週)}
        form = RenewBookForm(initial = {'renewal_date':proposed_renewal_date,})

    return render(request,'catalog/book_renew_librarian.html',{'form':form,'bookinst':book_inst})


from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
# from .models import Author

class AuthorCreate(CreateView):
    model = Author
    # Same syntax as for ModelForm
    # Show them Individually
    fields = '__all__'
    # 可以設定初值
    # 以字典的方式填入
    initial = {'first_name':'lee','date_of_death':'03/10/2021',}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['last_name','first_name','date_of_birth','date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
'''
# 基於類的視圖需要權限的混合
from django.contrib.auth.mixins import PermissionRequiredMixin

class MyView(PermissionRequiredMixin,View):
    permission_required = 'catalog.can_mark_returned'
    # Multiple Permissions
    # permission_required = ('catalog.can_mark_returned','catalog.can_edit')
'''


'''
# 能夠使用 @login_required 跟 LoginRequirMixin
from django.contrib.auth.decorators import login_required
@login_required
def my_view(request):
'''

'''
from django.contrib.auth.mixins import LoginRequiredMixin
# 具有很login_required裝飾器完權相同的定向行為。
# 可以指定其他位置來重新定向用戶(login_url)
# 或是使用URL參數名稱 代替"next"來插入當前的絕對路徑(redirect_field_name)
class MyView(LoginRequiredMixin,View):
    login_url = '/login/'
    # ???
    redirect_field_name = 'redirect_to'
'''
