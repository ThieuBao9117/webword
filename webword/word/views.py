from django.shortcuts import render
from django.http import HttpResponse, FileResponse,Http404
from docx import Document
import os
from django.conf import settings


def home(request):
    return render(request, 'word/home.html')


def process_document(request):


    if request.method == 'POST' and request.FILES.get('document'):
        # Load tài liệu từ request
        uploaded_file = request.FILES['document']
        doc = Document(uploaded_file)

        # Danh sách các vị trí chỗ trống cố định trong văn bản
        placeholders = ['[tham_so_1]','[tham_so_2]']

        # Biến replacements để lưu trữ các văn bản thay thế
        replacements = {}

        # Lặp qua các vị trí chỗ trống và yêu cầu người dùng nhập văn bản thay thế
        for placeholder in placeholders:
            replacement = request.POST.get(placeholder, '')
            replacements[placeholder] = replacement

        # Duyệt qua các đoạn văn của tài liệu
        for paragraph in doc.paragraphs:
            # Duyệt qua các vị trí chỗ trống và thực hiện thay thế
            for placeholder in placeholders:
                if placeholder in paragraph.text:
                    paragraph.text = paragraph.text.replace(placeholder, replacements[placeholder])

        # Lưu tài liệu đã được chỉnh sửa vào một tệp mới
        output_folder = os.path.join(settings.MEDIA_ROOT, 'processed_documents')  # Đường dẫn tới thư mục lưu trữ tệp mới
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)  # Tạo thư mục nếu nó không tồn tại
        output_file_path = os.path.join(output_folder, 'new_file.docx')  # Đường dẫn tới tệp mới
        doc.save(output_file_path)
        # Trả về file word đã được chỉnh sửa
        return FileResponse(open(output_file_path, 'rb'), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    return HttpResponse("Yêu cầu không hợp lệ.")


def download(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response
    else:
        raise Http404

