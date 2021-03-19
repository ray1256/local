from django.test import TestCase

from catalog.models import Author
from django.urls import reverse

class AuthorListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_authors = 13
        for author_num in range(number_of_authors):
            Author.objects.create(first_name = 'Christian %s' % author_num, last_name = 'Surname %s' % author_num,)

    def test_view_url_exists_at_desired_location(self):
        # 所有使用的client 都是使用 TestCase自帶產生的class 去模擬GET到的request and response
        # resp 就是 response
        # 可以使用url內的路徑 或是 他的name
        resp = self.client.get('/catalog/authors/')
        self.assertEquals(resp.status_code,200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('authors'))
        self.assertEquals(resp.status_code,200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('authors'))
        self.assertEquals(resp.status_code,200)

    def test_pagination_is_ten(self):
        resp = self.client.get(reverse('authors'))
        self.assertEquals(resp.status_code,200)
        self.assertTrue('is_paginated'in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['author_list']) == 10)

    def test_lists_all_authors(self):
        # Second Page
        resp = self.client.get(reverse('authors')+'?page=2')
        self.assertEquals(resp.status_code,200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['author_list']) == 3)

import datetime
from django.utils import timezone
from catalog.models import BookInstance,Books,Genre#,Language
from django.contrib.auth.models import User

class LoanBookInstancesByUserListViewTest(TestCase):

    def SetUp(self):
        # 創造兩個 測試用的user(test_user1,test_user2)
        test_user1 = User.objects.create_user(username = 'testuser1',password = '12345')
        test_user1.save()
        test_user2 = User.objects.create_user(username = 'testuser2',password = '12345')
        test_user2.save()

        # 創造做SetUp的屬性
        ## 創造在Author內的屬性
        test_author = Author.objects.create(first_name = 'John',last_name = 'Smith')
        ## 創造在Genre內的屬性
        test_genre = Genre.objects.create(name = 'Fantasy')

        ## 創造在Language內的屬性  ！！還沒弄
        #test_language = Language.objects.create(name = 'English')

        ## 創造在 Book內的屬性
        test_book = Books.objects.create(title = 'Book Title',summary = 'My Book Summary',isbn = 'ABCDEFG',author = test_author)#,language = test_language)

        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book)
        test_book.save()

        # 創造 30本的BookInstance Objects
        number_of_book_copies = 30
        for book_copy in range(number_of_book_copies):
            return_date = timezone.now()+datetime.timedelta(days = book_copy%5)
            # 偶數本
            if book_copy%2:
                the_borrower = test_user1
            # 奇數本
            else:
                the_borrower = test_user2
            status = 'm'
            # 真正創造 30本BookInstance
            BookInstance.objects.create(books = test_book,imprint = 'Unlikely Imprint,2016',due_back = return_date,borrower = the_borrower,status = status)

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('my-borrowed'))
        self.assertRedirects(resp,'/accounts/login/?next=/catalog/mybooks/')

    def test_logged_in_user_correct_template(self):
        login = self.client.login(username = 'testuser1',password = '12345')
        resp = self.client.get(reverse('my-borrowered'))
        # 確認是否有登入
        self.assertEquals(str(resp.context['user']),'testuser1')
        # 確認是否拿到的resp是200
        self.assertEquals(resp.status_code,200)
        # 確認是否使用的是 正確的template
        self.assertTemplateUsered(resp,'catalog/bookinstance_list_borrowed_user.html')

    def test_only_borrowed_books_in_list(self):
        login = self.client.login(username = 'testuser1',password = '12345')
        resp = self.client.get(reverse('my-borrowed'))

        self.assertEquals(str(resp.context['user']),'testuser1')
        self.assertEquals(resp.status_code,200)

        self.assertTrue('bookinstance_list' in resp.context)
        self.assertEquals(len(resp.context['bookinstance_list']),0)

        get_ten_books = BookInstance.objects.all()[:10]

        for copy in get_ten_books:
            copy.status = 'o'
            copy.save()

        resp = self.client.get(reverse('my-borrowed'))

        self.assertEquals(str(resp.context['user']),'textuser1')
        self.assertEquals(resp.status_code,200)

        for bookitem in resp.context['bookinstance_list']:
            self.assertEquals(resp.context['user'],bookitem.borrower)
            self.assertEquals('o',bookitem.status)

    def test_pages_ordered_by_due_date(self):

        for copy in BookInstance.objects.all():
            copy.status = 'o'
            copy.save()

        login = self.client.login(username = 'testuser1',password = '12345')
        resp = self.client.get(reverse('my-borrowed'))

        self.assertEquals(str(resp.context['user']),'testuser1')
        self.assertEquals(resp.status_code,200)

        # 確認只有10本書在展示在分頁
        self.assertEquals(len(resp.contex['bookinstance_list'],10))
        last_date = 0
        for copy in resp.context['bookinstance_list']:
            if last_date == 0:
                last_date = copy.due_back
            else:
                self.assertTrue(last_date <= copy.due_back)

# 用表單測試view

from django.contrib.auth.models import Permission

class RenewBookInstanceVIewTest(TestCase):

    def setUp(self):
        # 創造兩個 測試用的user(test_user1,test_user2)
        test_user1 = User.objects.create_user(username = 'testuser1',password = '12345')
        test_user1.save()
        test_user2 = User.objects.create_user(username = 'testuser2',password = '12345')
        test_user2.save()

        permission = Permission.objects.get(name = 'Set book as returned')
        test_user2.user_permissions.add(permission)
        test_user2.save()

        test_author = Author.objects.create(first_name = 'John',last_name = 'Smith')
        ## 創造在Genre內的屬性
        test_genre = Genre.objects.create(name = 'Fantasy')

        ## 創造在Language內的屬性  ！！還沒弄
        #test_language = Language.objects.create(name = 'English')

        ## 創造在 Book內的屬性
        test_book = Books.objects.create(title = 'Book Title',summary = 'My Book Summary',isbn = 'ABCDEFG',author = test_author)#,language = test_language)

        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book)
        test_book.save()

        return_date = datetime.date.today()+datetime.timedelta(days = 5)
        self.test_bookinstance1 = BookInstance.objects.create(books = test_book,imprint = 'Unlikely Imprint,2016',due_back = return_date,borrower = test_user1 ,status = 'o')

        return_date = datetime.date.today()+datetime.timedelta(days = 5)
        self.test_bookinstance2 = BookInstance.objects.create(books = test_book,imprint = 'Unlikely Imprint,2016',due_back = return_date,borrower = test_user2,status = 'o')

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('renewal-book-librarian',kwargs = {'pk':self.test_bookinstance1.pk,}))

        self.assertEquals(resp.status_code,302)
        self.assertTrue(resp.url.startswith('/accounts/login/'))

    def test_redirect_if_logged_in_but_not_correct_premission(self):
        login = self.client.login(username = 'testuser1',password = '12345')
        resp = self.client.get(reverse('renewal-book-librarian',kwargs = {'pk':self.test_bookinstance1.pk},))

        self.assertTrue(resp.status_code,302)
        self.assertTrue(resp.url.startswith('/accounts/login/'))

    # 如果是持有權限的人
    def test_logged_in_with_permission_borrowed_book(self):
        login = self.client.login(username='testuser2', password='12345')
        resp = self.client.get(reverse('renewal-book-librarian', kwargs={'pk':self.test_bookinstance2.pk,}) )


        self.assertEquals(resp.status_code,200)

    # 如果是圖書館員
    def test_logged_in_with_permission_another_users_borrowed_book(self):
        login = self.client.login(username='testuser2', password='12345')
        resp = self.client.get(reverse('renewal-book-librarian', kwargs={'pk':self.test_bookinstance1.pk,}) )

        # bug
        self.assertEquals(resp.status_code,200)

    def test_HTTP404_for_invalid_book_if_logged_in(self):
        import uuid
        test_uid = uuid.uuid4()
        login = self.client.login(username = 'testuser2',password = '12345')
        resp = self.client.get(reverse('renewal-book-librarian',kwargs = {'pk':test_uid,}))
        self.assertEquals(resp.status_code,404)

    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='12345')
        resp = self.client.get(reverse('renewal-book-librarian', kwargs={'pk':self.test_bookinstance1.pk,}) )
        # bug
        self.assertEquals(resp.status_code,200)

        #self.assertTemplateUsered(resp,'catalog/book_renew_librarian.html')

    def test_form_renewal_date_initially_has_date_three_weeks_in_future(self):
        login = self.client.login(username='testuser2', password='12345')
        resp = self.client.get(reverse('renewal-book-librarian', kwargs={'pk':self.test_bookinstance1.pk,}) )
        # bug
        self.assertEqual(resp.status_code,200)

        date_3_weeks_in_future = datetime.date.today() + datetime.timedelta(weeks = 3)
        self.assertEquals(resp.context['form'].initial['renewal_date'],date_3_weeks_in_future)

    def test_redirects_to_all_borrowed_book_list_on_success(self):
        login = self.client.login(username = 'testuser2',password = '12345')
        valid_date_in_future = datetime.date.today()+datetime.timedelta(weeks = 2)
        resp = self.client.post(reverse('renewal-book-librarian',kwargs = {'pk':self.test_bookinstance1.pk}),{'renewal_date':valid_date_in_future})

        #self.assertRedirects(resp,reverse('all-borrowed'))
        self.assertRedirects(resp,reverse('/'))

    def test_form_invalid_renewal_date_past(self):
        login = self.client.login(username = 'testuser2',password = '12345')
        date_in_past = datetime.date.today()-datetime.timedelta(weeks =1)
        resp = self.client.post(reverse('renewal-book-librarian',kwargs = {'pk':self.test_bookinstance1.pk}),{'renewal_date':date_in_past})
        self.assertEquals( resp.status_code,200)

        self.assertFormError(resp,'form','renewal_date','Invalid date - renewal in past')

    def test_form_invalid_renewal_date_future(self):
        login = self.client.login(username = 'testuser2',password = '12345')
        invalid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=5)
        date_in_past = datetime.date.today() - datetime.timedelta(weeks =1)
        resp = self.client.post(reverse('renewal-book-librarian',kwargs = {'pk':test_bookinstance1.pk}),{'renewal_date':invalid_date_in_future})
        self.assertEquals(resp.status_code,200)
        self.asssetFormError(resp,'form','renewal_date','Invalid date - renewal more than 4 weeks ahead')
