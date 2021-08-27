from servicios.api.views import OperView, RecargaView, TransferView, ServiciosView, InternetView, JovenClubView, EmbyView, FileZillaView 
from django.urls import path

app_name='servicios'


urlpatterns = [
    path('<str:pk>/', ServiciosView.as_view(), name="servicios"),
    path('<str:pk>/compra_internet/', InternetView.as_view(), name="internet"),    
    path('jovenclub/<str:pk>/', JovenClubView.as_view(), name="jovenclub"),    
    path('emby/<str:pk>/', EmbyView.as_view(), name="emby"),    
    path('filezilla/<str:pk>/', FileZillaView.as_view(), name="filezilla"),    
    path('operaciones/<str:pk>/', OperView.as_view(), name="opers"),
    path('recarga/<str:pk>/', RecargaView.as_view(), name="recarga"),
    path('transfer/<str:pk>/', TransferView.as_view(), name="transfer"),
]
