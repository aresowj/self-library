import os
from django.core.servers.basehttp import FileWrapper
from django.views.generic.base import View
from django.http import HttpResponse, Http404


class DownloadFileWithWrapper(View):
    """Based on Django 1.8.6"""
    FILE_SAMPLES = {
        'test': 'test.csv',
    }
    
    def __init__(self):
        self.file_type = ''
        self.file_absolute_path = ''
        self.file_base_name = ''
        self.file_extension = ''
        self.file_content_type = ''
    
    def get(self, request):
        try:
            self.file_type = request.GET['file_type']
        except KeyError:
            raise Http404
        return self.return_file()
        
    def parse_file_information(self):
        self.file_absolute_path = os.path.join(os.path.dirname(__file__), self.FILE_SAMPLES[self.file_type])
        self.file_base_name = os.path.basename(self.file_absolute_path)
        self.file_extension = self.file_base_name.split('.')[-1]
        # you can extend this line to dynamically assign content types for different files
        self.file_content_type = 'text/csv'
        
    def return_file(self):
        self.parse_file_information()
        wrapper = FileWrapper(open(self.file_absolute_path, 'rb'))
        response = HttpResponse(wrapper, content_type=self.file_content_type)
        response['Content-Disposition'] = 'attachment; filename="%s"' % self.file_base_name
        response['Content-Length'] = os.path.getsize(self.file_absolute_path)
