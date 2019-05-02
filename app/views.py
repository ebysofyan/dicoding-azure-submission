"""
app.views
"""
import os
import time

import requests
from azure.storage.blob import PublicAccess
from azure.storage.blob.blockblobservice import BlockBlobService
from django.contrib import messages
from django.core.files.temp import NamedTemporaryFile
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, FormView

from .forms import FileUplaodForm, ProgrammingForm
from .models import Programming

# Create your views here.


class ProgrammingView(FormView):
    """ProgrammingView"""
    template_name = 'index.html'
    form_class = ProgrammingForm

    def get_context_data(self, **kwargs):
        ctx = super(ProgrammingView, self).get_context_data(**kwargs)
        ctx['list'] = Programming.objects.all()
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "New Programming language added", extra_tags='success')
        form.save()
        return redirect('index:view')

    def form_invalid(self, form):
        err = {}
        for k, val in form.errors.items():
            err[k] = ', '.join(val)

        messages.error(self.request, err, extra_tags='danger')
        return redirect('index:view')


class ProgrammingDeleteView(DeleteView):
    """
    ProgrammingDeletView
    """
    model = Programming
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('index:view')

    def get(self, *args, **kwargs):
        """get request"""
        return self.post(*args, **kwargs)


class FileUploadPageView(FormView):
    template_name = 'blob_storage.html'
    form_class = FileUplaodForm
    container_name = 'dicodingsubcontainer'
    vision_url = 'https://southeastasia.api.cognitive.microsoft.com/vision/v2.0/analyze'

    @property
    def block_blob_service(self):
        ACCOUNT_NAME = os.environ['ACCOUNT_NAME']
        ACCOUNT_KEY = os.environ['ACCOUNT_KEY']

        block_blob_service = BlockBlobService(account_name=ACCOUNT_NAME, account_key=ACCOUNT_KEY)

        block_blob_service.create_container(self.container_name)

        block_blob_service.set_container_acl(self.container_name, public_access=PublicAccess.Container)
        return block_blob_service

    def create_blob_url(self, blob_name):
        return {
            'name': blob_name,
            'url': self.block_blob_service.make_blob_url(self.container_name, blob_name)
        }

    def analyze_image(self, blob_name):
        headers = {
            'Ocp-Apim-Subscription-Key': os.environ['COGNITIVE_VISION_API']
        }
        params = {
            "visualFeatures": "Categories,Description,Color",
            "details": "",
            "language": "en",
        }
        data = {
            'url': self.create_blob_url(blob_name)['url']
        }
        req = requests.post(self.vision_url, headers=headers, params=params, json=data)
        return req

    def send_analyze_result_as_message(self, blobname):
        res = self.analyze_image(blobname)
        messages.info(self.request, message=res.json())

    def get_context_data(self, *args, **kwargs):
        context = super(FileUploadPageView, self).get_context_data(*args, **kwargs)
        generator = self.block_blob_service.list_blobs(self.container_name)
        context['blobs'] = [self.create_blob_url(blob.name) for blob in generator]

        if 'blobname' in self.request.GET:
            blobname = self.request.GET['blobname']
            self.send_analyze_result_as_message(blobname)

        return context

    def form_valid(self, form):
        in_memory_file = self.request.FILES['file']

        image_temp_file = NamedTemporaryFile(delete=True)
        image_temp_file.write(in_memory_file.read())
        image_temp_file.flush()

        blobname = f"{time.time()}_{in_memory_file.name.lower()}"
        self.block_blob_service.create_blob_from_path(self.container_name, blobname, image_temp_file.name)
        image_temp_file.close()

        self.send_analyze_result_as_message(blobname)

        return redirect('')
