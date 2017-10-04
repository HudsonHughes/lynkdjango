from django.shortcuts import render
from account.decorators import *
# Create your views here.


@group_required('admin')
def course_manager(request):

	return render(request, 'admin_base.html', {

	})
