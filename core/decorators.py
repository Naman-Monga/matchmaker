from django.http import HttpResponse
from django.shortcuts import redirect

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*args, **kwargs):
            group = None
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.groups.exists():
                groups = request.user.groups.all()
                for group in groups:
                    if group.name in allowed_roles:
                        return view_func(request, *args, **kwargs)
                return HttpResponse("<h1>You dont have the permission to view this page.</h1>")
            else:
                return HttpResponse("<h1>You dont have the permission to view this page.</h1>")
        return wrapper_func
    return decorator