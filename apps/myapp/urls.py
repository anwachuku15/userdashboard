from django.urls import path
from . import views

urlpatterns = [
	path('', views.index),
    path('signin', views.home),
    path('sign', views.signin),
    path('register', views.regpage),
    path('reg', views.register),
    path('dashboard', views.dashboard),
    path('users/new', views.addpage),
    path('adduser', views.adduser),
    path('logout', views.logout),

    path('users/edit', views.editprofile),
    path('editinfo', views.editinfo),
    path('changepw', views.changepw),
    path('postmessage/<id>', views.postmessage),
    # path('editdesc', views.editdesc),

    path('users/show/<id>', views.profile, name = 'viewprofile'),

    path('dashboard/admin', views.admin),
    # path('users/new', views.new),
    # path('users/edit/<id>', views.edituser),

    # path('post', views.post),

	# path('logout', views.logout)
]