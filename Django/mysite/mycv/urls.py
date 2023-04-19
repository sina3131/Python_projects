from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import contact

urlpatterns = [
    # path('', views.cv, name='cover_letter'),
    path('', views.port, name='port'),
    path('website/', views.website, name= "website"),
    path('<int:pk>/', views.project_detail, name="detail"),
    path('contacct/', views.data_contact, name='data'),
    path('contact/', views.contact, name='contact'),
    path('thanks/', views.thanks, name='thanks')

   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

