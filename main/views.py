from django.shortcuts import redirect, render


def index(request):
    if request.user.is_authenticated:
        return render(request, 'main/index.html', {'user': request.user})
    else:
        return redirect('admin/')
