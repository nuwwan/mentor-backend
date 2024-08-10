from django.contrib import admin
from .models import Tag,Task,Timeline,Milestone,Peer,Mentorship

admin.site.register(Tag)
admin.site.register(Task)
admin.site.register(Timeline)
admin.site.register(Milestone)
admin.site.register(Peer)
admin.site.register(Mentorship)
