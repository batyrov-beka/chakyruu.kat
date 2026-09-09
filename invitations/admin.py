from django.contrib import admin
from django.utils.html import format_html
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from .models import Guest, Invitation


class GuestResource(resources.ModelResource):
    invitation = fields.Field(
        column_name="invitation_id",
        attribute="invitation",
        widget=ForeignKeyWidget(Invitation, "id"),
    )
    full_link = fields.Field(column_name="full_link")

    class Meta:
        model = Guest
        fields = ("id", "name", "invitation", "is_attending", "token", "full_link")
        export_order = (
            "id",
            "name",
            "invitation",
            "is_attending",
            "token",
            "full_link",
        )

    def dehydrate_full_link(self, guest):
        base_url = "http://127.0.0.1:8000"
        return f"{base_url}/{guest.invitation.slug}/?guest={guest.token}"


class GuestInline(admin.TabularInline):
    model = Guest
    extra = 1
    fields = ("name", "is_attending")


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ("groom_name", "bride_name", "event_type", "event_date")
    prepopulated_fields = {"slug": ("groom_name",)}
    inlines = [GuestInline]


@admin.register(Guest)
class GuestAdmin(ImportExportModelAdmin):
    resource_class = GuestResource
    list_display = (
        "name",
        "invitation",
        "is_attending",
        "token",
        "get_guest_link",
    )
    search_fields = ("name", "token")
    readonly_fields = ("token",)

    def get_guest_link(self, obj):
        link = f"http://127.0.0.1:8000/{obj.invitation.slug}/?guest={obj.token}"
        return format_html(
            '<a href="{0}" target="_blank" style="color: #2b6cb0; font-weight: bold;">Шилтеме</a>',
            link,
        )

    get_guest_link.short_description = "Жеке шилтеме"