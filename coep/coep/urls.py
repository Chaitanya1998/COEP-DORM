from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from app1 import views
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Home,name="home"),
    path('admin_g/', views.admin_g, name='admin_g'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('fe_pdf_boys/', views.fe_pdf_boys, name='fe_pdf_boys'),
    path('se_pdf_boys/', views.se_pdf_boys, name='se_pdf_boys'),
    path('te_pdf_boys/', views.te_pdf_boys, name='te_pdf_boys'),
    path('be_pdf_boys/', views.be_pdf_boys, name='be_pdf_boys'),
    path('fe_pdf_girls/', views.fe_pdf_girls, name='fe_pdf_girls'),
    path('se_pdf_girls/', views.se_pdf_girls, name='se_pdf_girls'),
    path('te_pdf_girls/', views.te_pdf_girls, name='te_pdf_bgirls'),
    path('be_pdf_girls/', views.be_pdf_girls, name='be_pdf_girls'),
    path('fe_pdf_w_boys/', views.fe_pdf_w_boys, name='fe_pdf_w_boys'),
    path('se_pdf_w_boys/', views.se_pdf_w_boys, name='se_pdf_w_boys'),
    path('te_pdf_w_boys/', views.te_pdf_w_boys, name='te_pdf_w_boys'),
    path('be_pdf_w_boys/', views.be_pdf_w_boys, name='be_pdf_w_boys'),
    path('fe_pdf_w_girls/', views.fe_pdf_w_girls, name='fe_pdf_w_girls'),
    path('se_pdf_w_girls/', views.se_pdf_w_girls, name='se_pdf_w_girls'),
    path('te_pdf_w_girls/', views.te_pdf_w_girls, name='te_pdf_w_bgirls'),
    path('be_pdf_w_girls/', views.be_pdf_w_girls, name='be_pdf_w_girls'),
    path('fe_pdf_f_boys/', views.fe_pdf_f_boys, name='fe_pdf_f_boys'),
    path('se_pdf_f_boys/', views.se_pdf_f_boys, name='se_pdf_f_boys'),
    path('te_pdf_f_boys/', views.te_pdf_f_boys, name='te_pdf_f_boys'),
    path('be_pdf_f_boys/', views.be_pdf_f_boys, name='be_pdf_f_boys'),
    path('fe_pdf_f_girls/', views.fe_pdf_f_girls, name='fe_pdf_f_girls'),
    path('se_pdf_f_girls/', views.se_pdf_f_girls, name='se_pdf_f_girls'),
    path('te_pdf_f_girls/', views.te_pdf_f_girls, name='te_pdf_f_bgirls'),
    path('be_pdf_f_girls/', views.be_pdf_f_girls, name='be_pdf_f_girls'),
    path('fe_room_boys/',views.fe_room_boys,name='fe_room_boys'),
    path('fe_room_girls/',views.fe_room_girls,name='fe_room_girls'),
    path('se_room_boys/',views.se_room_boys,name='se_room_boys'),
    path('se_room_girls/',views.se_room_girls,name='se_room_girls'),
    path('te_room_boys/',views.te_room_boys,name='te_room_boys'),
    path('te_room_girls/',views.te_room_girls,name='te_room_girls'),
    path('be_room_boys/',views.be_room_boys,name='be_room_boys'),
    path('be_room_girls/',views.be_room_girls,name='be_room_girls'),
    path('profile/preference/',views.PreferenceClass.as_view(),name='preference'),
    path('profile/preference/',views.SearchAjaxSubmitView.as_view(),name='search-ajax-submit'),
    path('submitpreference/',views.prefer,name='save'),
    path('cancel/',views.cancellation,name='delete'),
    path('profile/',views.profile,name="profile"),
    path('profile/settings',views.ProSet,name="settings"),
    path('profile/transaction',views.transaction,name="transaction"),
    path('signup/', views.signup, name='signup'),
    path('edit/',views.edit,name="edit"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
]



if settings.DEBUG :
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
