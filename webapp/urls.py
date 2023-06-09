"""
URL configuration for webapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from scholars import views
from scholars.views import Members
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Dashboard.as_view(), name='dashboard'),

    path('members', views.MembersView.as_view(), name='members'),
    path('members-add', views.MembersAdd, name='members-add'),
    path('profile/memberID=<int:memberID>/', views.ProfileView.as_view(), name='profile'),
    path('profile-edit/memberID=<pk>', views.ProfileEdit.as_view(), name='profile-edit'),
    path('profile-edit/memberID=<int:memberID>', views.ProfileEdit.as_view(), name='profile-edit'),
    path('profile-delete/<int:memberID>', views.ProfileDelete, name='profile-delete'),

    path('grades-page', views.GradesPageView.as_view(), name='grades-page'),
    path('grades/memberID=<int:memberID>/', views.MemberGradesView.as_view(), name='grades'),
    path('grades-add/memberID=<int:memberID>', views.MemberGradesAdd, name='grades-add'),
    path('grades-edit/memberID=<int:memberID>/gradeID=<pk>/', views.GradesEdit.as_view(), name='grades-edit'),
    path('grades-edit/memberID=<int:memberID>/gradeID=<int:gradeID>/', views.GradesEdit.as_view(), name='grades-edit'),
    path('grades-delete/memberID=<int:memberID>/gradeID=<int:gradeID>/', views.GradesDelete, name='grades-delete'),

    path('reqs-page', views.ReqsPageView.as_view(), name='reqs-page'),
    path('reqs/memberID=<int:memberID>', views.MemberRequirementsView.as_view(), name='requirements'),
    path('reqs-add/memberID=<int:memberID>', views.MemberReqsAdd, name='reqs-add'),
    path('reqs-delete/memberID=<int:memberID>/reqsID=<int:reqsID>', views.ReqsDelete, name='reqs-delete'),
    path('reqs_list-add', views.ReqListAdd, name='reqs_list-add'),
    path('reqs_list-edit/reqs_listID=<pk>', views.ReqsListEdit.as_view(), name='reqs_list-edit'),
    path('reqs_list-edit/reqs_listID=<int:reqs_listID>', views.ReqsListEdit.as_view(), name='reqs_list-edit'),
    path('reqs_list-delete/<int:reqs_listID>', views.ReqsListDelete, name='reqs_list-delete'),

    path('allowance-page', views.AllowancePageView.as_view(), name='allowance-page'),
    path('allowance/memberID=<int:memberID>', views.MemberAllowancesView.as_view(), name='allowances'),
    path('allowance-add/memberID=<int:memberID>', views.MemberAllowanceAdd, name='allowance-add'),
    path('allowance-edit/memberID=<int:memberID>/allowanceID=<pk>/', views.AllowanceEdit.as_view(), name='allowance-edit'),
    path('allowance-edit/memberID=<int:memberID>/allowanceID=<int:allowanceID>/', views.AllowanceEdit.as_view(), name='allowance-edit'),
    path('allowance-delete/memberID=<int:memberID>/allowanceID=<int:allowanceID>', views.AllowanceDelete, name='allowance-delete'),

]
