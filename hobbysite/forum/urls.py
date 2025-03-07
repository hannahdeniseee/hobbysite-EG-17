from django.urls import path
from .views import threads_list, thread_detail

urlpatterns = [
    path('threads', threads_list, name='threads-list'),
    path('thread/<int:pk>', thread_detail, name='thread-detail')
]

app_name = "forum"
