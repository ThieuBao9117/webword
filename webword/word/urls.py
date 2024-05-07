

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Định nghĩa URLpattern cho trang chủ
    path('save/', views.process_document, name='process_document'),  # Định nghĩa URLpattern cho xử lý tài liệu
    path('download/<str:file_name>/', views.download, name='download'),  # Định nghĩa URLpattern cho tải xuống tệp
    
]
