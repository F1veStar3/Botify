from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import ProfileForm, UserForm
from .forms import ReviewForm
from .models import Events, Category, Menu, MapPoint, Partner,Message


def base(request):
    events = Events.objects.order_by('-id')[:3]
    categories = Category.objects.all()
    partners = Partner.objects.all()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ReviewForm()

    context = {

        'partners': partners,
        'categories': categories,
        'form': form,
        'events': events,
    }

    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')


def show_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Menu.objects.filter(category=category)

    context = {
        'category': category,
        'products': products,
    }

    return render(request, 'category_detail.html', context)


class MapPointsAPI(View):
    def get(self, request):
        points = MapPoint.objects.all().values('name', 'latitude', 'longitude')
        return JsonResponse(list(points), safe=False)


@login_required
def profile_view(request):
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)

    if request.method == 'POST':
        if 'user_form' in request.POST:
            user_form = UserForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                return redirect('profile')
        else:
            profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if profile_form.is_valid():
                profile_form.save()
                return redirect('profile')

    context = {
        'user_form': user_form,
        'profile_form': profile_form,

    }

    return render(request, 'profile.html', context)

@login_required
def mark_notifications_as_read(request):
    if request.method == 'POST':
        Message.objects.filter(recipient=request.user, read=False).update(read=True)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'})
