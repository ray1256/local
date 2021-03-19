from django.db import models

class MyModelName(models.Model):
    # Field 字段
    # 每個字段會儲存我們在資料庫的一欄col資料
    # row將由每個字段值之一組成
    # my_field_name單一字段
    # 類型 models.CharField  代表這個字段將包含字母、數字字符串
    my_field_name = models.CharField(max_length = 20, help_text = 'Enter field documentation')

    # Metadata
    # 通過宣告 class Meta 來宣告模型級別的元數
    # 控制在查詢模型類型時返回之記錄的默認排序。
    # 如上所示。排序將依賴字段的類型
    class Meta:
        # 如上所示，你可以使用減號（-）前綴字段名稱以反轉排序順序。
        ordering = ['-my_field_name']
        # 例如，如果我們選擇依照此預設來排列書單：
        # ordering = ['title', '-pubdate']
        # 另一個常見的屬性是 verbose_name ,一個 verbose_name 說明單數和複數形式的類別。

    # Django 方法中另一個常用方法是 get_absolute_url() ，這函數返回一個在網站上顯示個人模型記錄的 URL
    # 如果你定義了該方法，那麼 Django 將自動在“管理站點”中添加“在站點中查看“按鈕在模型的記錄編輯欄
    def get_absolute_url(self):
        return reverse('model-detail-view',args = [str(self.id)])
    # 最起碼，在每個模型中，你應該定義標準的Python 類方法__str__()
    # 來為每個物件返回一個人類可讀的字符串
    # 此字符用於表示管理站點的各個記錄（以及你需要引用模型實例的任何其他位置）
    def __str__(self):
        return self.field_name
# 一旦你定義了模型類，你可以使用它們來創建，更新或刪除記錄，並運行查詢獲取所有記錄或特定的記錄子集。
