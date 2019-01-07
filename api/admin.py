from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    # editable = ['name', 'cpu', 'mem', 'disk']
    fields = ('name', 'cpu', 'mem', 'disk', 'cpu_available', 'mem_available', 'disk_available', 'created_date',
              'last_update', 'interface')
    readonly_fields = ('cpu_available', 'mem_available', 'disk_available', 'created_date', 'last_update')
    list_display = ('id', 'name', 'cpu_available', 'mem_available', 'disk_available', 'created_date', 'last_update')
    list_display_links = ('id', 'name')


@admin.register(Vhost)
class VhostAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cpu', 'mem', 'disk_size', 'created_date', 'last_update')
    list_display_links = ('id', 'name')
    # list_editable = ('name', '')


@admin.register(Interface)
class InterfaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'machine', 'mac', 'ip')


@admin.register(IP)
class IpAdmin(admin.ModelAdmin):
    pass


@admin.register(IPPool)
class IPPoolAdmin(admin.ModelAdmin):
    list_display = ('id', 'network', 'mask', 'available_ip', 'used_ip')


@admin.register(Images)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'os_type', 'os_version', 'image_type', 'image_path')


