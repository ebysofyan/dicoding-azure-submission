"""
app.urls
"""
from django.urls import path

from . import views

urlpatterns = [
    # path('', views.ProgrammingView.as_view(), name='view'),
    # path('delete/<int:pk>', views.ProgrammingDeleteView.as_view(), name='delete'),

    path('analyze', views.FileUploadPageView.as_view(), name='uload_view'),
]
