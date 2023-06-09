from django.contrib import admin
from django.conf import settings
from .models import Members, Grades, Requirements, Requirements_list, Allowances

admin.site.site_header = "Scholar Sphere System"
admin.site.site_title = "Scholar Sphere System"
admin.site.index_title = "Welcome to Scholar Sphere System Administration"


# Register your models here.

@admin.register(Members)
class ScholarsAdmin(admin.ModelAdmin):
    list_display = ("get_member_name", "school", "college",  "program", "yearlevel",  "civilstatus")
    search_fields = ("firstname", "lastname", "yearlevel", "college")
    list_filter = ("created_at",)
  
    def get_member_name(self, obj):
        return obj.firstname + " " + obj.lastname
    get_member_name.short_description = "Member Name"

@admin.register(Grades)
class ScholarsAdmin(admin.ModelAdmin):
    list_display = ( "semester",  "yearlevel",
                    "course", "grades") 
    search_fields = ("yearlevel", "semester")
    list_filter = ("created_at",)


@admin.register(Requirements)
class ScholarsAdmin(admin.ModelAdmin):
    list_display = ("reqs_listID", "date")
    search_fields = ("reqs_listID", "date")
    list_filter = ("created_at",)

@admin.register(Requirements_list)
class ScholarsAdmin(admin.ModelAdmin):
    list_display = ("reqs_requirements", "notes")
    search_fields = ("reqs_requirements", "notes")
    list_filter = ("created_at",)

@admin.register(Allowances)
class ScholarsAdmin(admin.ModelAdmin):
    list_display = ("semester", "yearlevel",  "month")
    search_fields = ("yearlevel", "semester")
    list_filter = ("created_at",)


admin.site.static_files = [
    {
        'path': settings.STATIC_URL + 'css/admin.css',
        'rel': 'stylesheet',
    },
]
