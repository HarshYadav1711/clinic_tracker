from django.contrib import admin
from .models import Clinic, UserProfile, FollowUp, PublicViewLog


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ("name", "clinic_code", "created_at")
    readonly_fields = ("clinic_code", "created_at")


@admin.register(FollowUp)
class FollowUpAdmin(admin.ModelAdmin):
    list_display = (
        "patient_name",
        "clinic",
        "status",
        "due_date",
        "view_count",
    )
    readonly_fields = ("public_token", "created_at", "updated_at")

    def view_count(self, obj):
        return obj.publicviewlog_set.count()
    view_count.short_description = "Views"


admin.site.register(UserProfile)
admin.site.register(PublicViewLog)
