from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from tutdb.models import Department

@login_required
def faculty_chat_room(request, department):
    try:
    # retrieve course with given id joined by the current user
        department = Department.objects.get(slug=department)
    except Department.DoesNotExist:
    # user is not a student of the course or course does not exist
        return HttpResponseNotFound("Can't find department")
    context = {'department': department}
    return render(request, 'chat/room.html', context)
