from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.views import LoginView
User = get_user_model()
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .models import HQDog, TpsMoshiDog, DodomaDog, IringaDog, HQHorse, MedicalRecord, Picture, ActivityLog, \
    AnimalTransfer
from django.db.models import Q
from .models import DodomaHorse, IringaHorse, TpsMoshiHorse
from .forms import HQDogForm, TpsMoshiDogForm, DodomaDogForm, IringaDogForm, HQHorseForm, MedicalRecordForm, PictureForm, DodomaHorseForm, IringaHorseForm, TpsMoshiHorseForm, UserForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import UserRegisterForm


class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        remember_me = self.request.POST.get('remember')
        if not remember_me:
            # Session expires when user closes browser
            self.request.session.set_expiry(0)
        response = super().form_valid(form)
        user = self.request.user
        if user.role == 'admin' or user.role == 'all':
            return redirect('admin_dashboard')
        elif user.role == 'veterinarian':
            return redirect('veterinarian_dashboard')
        else:
            return redirect('user_dashboard')


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Your account has been created! You can now log in.')
        return response


def user_profile(request):
    # Your profile view logic here
    return render(request, 'mysite/user_profile.html', {'user': request.user})

def location_required(allowed_locations):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                messages.error(request, "Please log in to access this page.")
                return redirect('login')  # Redirect to login page if not authenticated

            if user.role == 'admin' and user.location == 'hq':
                return view_func(request, *args, **kwargs)  # HQ admin has full access
            elif user.location in allowed_locations:
                return view_func(request, *args, **kwargs)  # Access granted if location matches
            else:
                messages.error(request, "You do not have permission to access this area.")
                return render(request, 'permission_denied.html')  # Render permission denied page
        return wrapper
    return decorator


def location_required(allowed_locations):
    def decorator(view_func):
        @login_required
        def wrapped_view(request, *args, **kwargs):
            # Admin users can access all locations
            if request.user.role == 'admin' or request.user.location == 'all':
                return view_func(request, *args, **kwargs)

            # Check if user's location is in allowed locations
            if request.user.location in allowed_locations:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "You do not have permission to access this branch's data.")
                return redirect('dashboard')

        return wrapped_view

    return decorator


from django.shortcuts import render
from .models import User  # Ensure you're using the correct import for your custom User model

def dashboard(request):
    # Query user-related data
    friends_list = User.objects.all()[:5]
    top_members = User.objects.all().order_by('-date_joined')[:5]

    # Sample data for animal transfers (replace with real queries as needed)
    animal_transfers = [
        {
            'id': 1,
            'date': '2025-04-15',
            'animal_name': 'Rex',
            'animal_type': 'Dog',
            'from_location': 'HQ',
            'to_location': 'Dodoma',
            'reason': 'Training',
            'handled_by': 'John Doe'
        },
        {
            'id': 2,
            'date': '2025-04-10',
            'animal_name': 'Thunder',
            'animal_type': 'Horse',
            'from_location': 'Iringa',
            'to_location': 'HQ',
            'reason': 'Medical Treatment',
            'handled_by': 'Jane Smith'
        },
    ]

    context = {
        'friends_list': friends_list,
        'top_members': top_members,
        'earnings': 1000,
        'downloads': 150,
        'new_views': 300,
        'comments': 75,
        'animal_transfers': animal_transfers,
    }

    return render(request, 'dashboard.html', context)



def log_activity(user, action, obj=None):
    if obj:
        ActivityLog.objects.create(user=user, action=action, content_object=obj)
    else:
        ActivityLog.objects.create(user=user, action=action)


@login_required
def dashboard(request):
    # Admin users can see all stats
    if request.user.role == 'admin' or request.user.location == 'all':
        # Original aggregation code remains the same
        total_dog_weight = HQDog.objects.aggregate(total_weight=Sum('weight'))['total_weight'] or 0
        total_tps_moshi_dog_weight = TpsMoshiDog.objects.aggregate(total_weight=Sum('weight'))['total_weight'] or 0
        total_dodoma_dog_weight = DodomaDog.objects.aggregate(total_weight=Sum('weight'))['total_weight'] or 0
        total_iringa_dog_weight = IringaDog.objects.aggregate(total_weight=Sum('weight'))['total_weight'] or 0
        total_horse_weight = HQHorse.objects.aggregate(total_weight=Sum('weight'))['total_weight'] or 0
        total_dodoma_horse_weight = DodomaHorse.objects.aggregate(total_weight=Sum('weight'))['total_weight'] or 0
        total_iringa_horse_weight = IringaHorse.objects.aggregate(total_weight=Sum('weight'))['total_weight'] or 0
        total_tps_moshi_horse_weight = TpsMoshiHorse.objects.aggregate(total_weight=Sum('weight'))['total_weight'] or 0

        # Dog and horse counts from all locations
        total_dogs = HQDog.objects.count() + TpsMoshiDog.objects.count() + DodomaDog.objects.count() + IringaDog.objects.count()
        total_horses = HQHorse.objects.count() + TpsMoshiHorse.objects.count() + DodomaHorse.objects.count() + IringaHorse.objects.count()
    else:
        # Location-specific aggregation
        if request.user.location == 'hq':
            total_dog_weight = HQDog.objects.aggregate(total_weight=Sum('weight'))['total_weight'] or 0
            total_horse_weight = HQHorse.objects.aggregate(total_weight=Sum('weight'))['total_weight'] or 0
            total_dogs = HQDog.objects.count()
            total_horses = HQHorse.objects.count()
            total_tps_moshi_dog_weight = total_dodoma_dog_weight = total_iringa_dog_weight = 0
            total_tps_moshi_horse_weight = total_dodoma_horse_weight = total_iringa_horse_weight = 0
        elif request.user.location == 'tps_moshi':
            total_dog_weight = TpsMoshiDog.objects.aggregate(total_weight=Sum('weight'))['total_weight'] or 0
            total_horse_weight = TpsMoshiHorse.objects.aggregate(total_weight=Sum('weight'))['total_weight'] or 0
            total_dogs = TpsMoshiDog.objects.count()
            total_horses = TpsMoshiHorse.objects.count()
            total_hq_dog_weight = total_dodoma_dog_weight = total_iringa_dog_weight = 0
            total_hq_horse_weight = total_dodoma_horse_weight = total_iringa_horse_weight = 0
        elif request.user.location == 'dodoma':
            total_dog_weight = DodomaDog.objects.aggregate(total_weight=Sum('weight'))['total_weight'] or 0
            total_horse_weight = DodomaHorse.objects.aggregate(total_weight=Sum('weight'))['total_weight'] or 0
            total_dogs = DodomaDog.objects.count()
            total_horses = DodomaHorse.objects.count()
            total_hq_dog_weight = total_tps_moshi_dog_weight = total_iringa_dog_weight = 0
            total_hq_horse_weight = total_tps_moshi_horse_weight = total_iringa_horse_weight = 0
        elif request.user.location == 'iringa':
            total_dog_weight = IringaDog.objects.aggregate(total_weight=Sum('weight'))['total_weight'] or 0
            total_horse_weight = IringaHorse.objects.aggregate(total_weight=Sum('weight'))['total_weight'] or 0
            total_dogs = IringaDog.objects.count()
            total_horses = IringaHorse.objects.count()
            total_hq_dog_weight = total_tps_moshi_dog_weight = total_dodoma_dog_weight = 0
            total_hq_horse_weight = total_tps_moshi_horse_weight = total_dodoma_horse_weight = 0

    total_earnings = (total_dog_weight + total_horse_weight)
    total_downloads = total_dogs + total_horses

    # Get medical records and pictures only for the user's location
    if request.user.role == 'admin' or request.user.location == 'all':
        total_new_views = MedicalRecord.objects.count()
        total_comments = Picture.objects.count()
        last_activities = ActivityLog.objects.order_by('-timestamp')[:5]
    else:
        # This will need to be modified depending on how medical records and pictures are associated with locations
        # For now, we're showing all records, but you might want to filter them by location
        total_new_views = MedicalRecord.objects.count()
        total_comments = Picture.objects.count()
        last_activities = ActivityLog.objects.filter(
            user__location=request.user.location
        ).order_by('-timestamp')[:5]

    # Get users from the same location
    if request.user.role == 'admin' or request.user.location == 'all':
        friends_list = User.objects.order_by('?')[:5]
        top_members = User.objects.order_by('?')[:5]
    else:
        friends_list = User.objects.filter(location=request.user.location).order_by('?')[:5]
        top_members = User.objects.filter(location=request.user.location).order_by('?')[:5]

    return render(request, 'dashboard.html', {
        'earnings': total_earnings,
        'downloads': total_downloads,
        'new_views': total_new_views,
        'comments': total_comments,
        'friends_list': friends_list,
        'top_members': top_members,
        'last_activities': last_activities


# Dog Views

@login_required
def hq_dog_list(request):
    dogs = HQDog.objects.all()
    age_min = request.GET.get('age_min')
    age_max = request.GET.get('age_max')
    if breed:
        dogs = dogs.filter(breed__in=breed)
    if age_min and age_max:
        dogs = dogs.filter(date_of_birth__range=[age_min, age_max])
    elif age_min:
        dogs = dogs.filter(date_of_birth__gte=age_min)
    elif age_max:
        dogs = dogs.filter(date_of_birth__lte=age_max)

    context = {'dogs': dogs, 'age_min': age_min, 'age_max': age_max}
    return render(request, 'hq_dog_list.html', context)

@login_required
def user_profile(request):
    user = request.user
    return render(request, 'user_profile.html', {'user': user})


@login_required
def hq_dog_detail(request, pk):
    dog = get_object_or_404(HQDog, pk=pk)
    return render(request, 'hq_dog_detail.html', {'dog': dog})

@login_required
@location_required(['hq'])
def hq_dog_create(request):
    if request.method == 'POST':
        form = HQDogForm(request.POST, request.FILES)
        if form.is_valid():
            dog = form.save()
            log_activity(request.user, 'created hq dog', dog)
            return redirect('hq_dog_list')
    else:
        form = HQDogForm()
    return render(request, 'hq_dog_form.html', {'form': form})


@login_required
def hq_dog_update(request, pk):
    dog = get_object_or_404(HQDog, pk=pk)
    if request.method == 'POST':
        form = HQDogForm(request.POST, request.FILES, instance=dog)
        if form.is_valid():
            dog = form.save()
            log_activity(request.user, 'updated hq dog', dog)
            return redirect('hq_dog_list')
    else:
        form = HQDogForm(instance=dog)
    return render(request, 'hq_dog_form.html', {'form': form})

@login_required
def hq_dog_delete(request, pk):
    dog = get_object_or_404(HQDog, pk=pk)
    if request.method == 'POST':
        dog.delete()
        log_activity(request.user, 'deleted hq dog', dog)
        return redirect('hq_dog_list')
    return render(request, 'hq_dog_confirm_delete.html', {'dog': dog})


@login_required
def hq_dog_search(request):
    query = request.GET.get('q')
    if query:
        dogs = HQDog.objects.filter(name__icontains=query)
    else:
        dogs = []
    return render(request, 'hq_dog_list.html', {'dogs': dogs, 'query': query})


@login_required
def tps_moshi_dog_list(request):
    dogs = TpsMoshiDog.objects.all()
    age_min = request.GET.get('age_min')
    age_max = request.GET.get('age_max')
    if breed:
        dogs = dogs.filter(breed__in=breed)
    if age_min and age_max:
        dogs = dogs.filter(date_of_birth__range=[age_min, age_max])
    elif age_min:
        dogs = dogs.filter(date_of_birth__gte=age_min)
    elif age_max:
        dogs = dogs.filter(date_of_birth__lte=age_max)

    context = {'dogs': dogs, 'age_min': age_min, 'age_max': age_max}
    return render(request, 'tps_moshi_dog_list.html', context)

@login_required
@location_required(['tps_moshi'])
def tps_moshi_dog_detail(request, pk):
    dog = get_object_or_404(TpsMoshiDog, pk=pk)
    return render(request, 'tps_moshi_dog_detail.html', {'dog': dog})

@login_required
@location_required(['tps_moshi'])
def tps_moshi_dog_create(request):
    if request.method == 'POST':
        form = TpsMoshiDogForm(request.POST, request.FILES)
        if form.is_valid():
            dog = form.save()
            log_activity(request.user, 'created tps moshi dog', dog)
            return redirect('tps_moshi_dog_list')
    else:
        form = TpsMoshiDogForm()
    return render(request, 'tps_moshi_dog_form.html', {'form': form})

@login_required
@location_required(['tps_moshi'])
def tps_moshi_dog_update(request, pk):
    dog = get_object_or_404(TpsMoshiDog, pk=pk)
    if request.method == 'POST':
        form = TpsMoshiDogForm(request.POST, request.FILES, instance=dog)
        if form.is_valid():
            dog = form.save()
            log_activity(request.user, 'updated tps moshi dog', dog)
            return redirect('tps_moshi_dog_list')
    else:
        form = TpsMoshiDogForm(instance=dog)
    return render(request, 'tps_moshi_dog_form.html', {'form': form})

@login_required
@location_required(['tps_moshi'])
def tps_moshi_dog_delete(request, pk):
    dog = get_object_or_404(TpsMoshiDog, pk=pk)
    if request.method == 'POST':
        dog.delete()
        log_activity(request.user, 'deleted tps moshi dog', dog)
        return redirect('tps_moshi_dog_list')
    return render(request, 'tps_moshi_dog_confirm_delete.html', {'dog': dog})


@login_required
def tps_moshi_dog_search(request):
    query = request.GET.get('q')
    if query:
        dogs = TpsMoshiDog.objects.filter(name__icontains=query)
    else:
        dogs = []
    return render(request, 'tps_moshi_dog_list.html', {'dogs': dogs, 'query': query})


@login_required
def dodoma_dog_list(request):
    dogs = DodomaDog.objects.all()
    age_min = request.GET.get('age_min')
    age_max = request.GET.get('age_max')
    if breed:
        dogs = dogs.filter(breed__in=breed)
    if age_min and age_max:
        dogs = dogs.filter(date_of_birth__range=[age_min, age_max])
    elif age_min:
        dogs = dogs.filter(date_of_birth__gte=age_min)
    elif age_max:
        dogs = dogs.filter(date_of_birth__lte=age_max)

    context = {'dogs': dogs, 'age_min': age_min, 'age_max': age_max}
    return render(request, 'dodoma_dog_list.html', context)

@login_required
@location_required(['dodoma'])
def dodoma_dog_detail(request, pk):
    dog = get_object_or_404(DodomaDog, pk=pk)
    return render(request, 'dodoma_dog_detail.html', {'dog': dog})

@login_required
@location_required(['dodoma'])
def dodoma_dog_create(request):
    if request.method == 'POST':
        form = DodomaDogForm(request.POST, request.FILES)
        if form.is_valid():
            dog = form.save()
            log_activity(request.user, 'created dodoma dog', dog)
            return redirect('dodoma_dog_list')
    else:
        form = DodomaDogForm()
    return render(request, 'dodoma_dog_form.html', {'form': form})

@login_required
@location_required(['dodoma'])
def dodoma_dog_update(request, pk):
    dog = get_object_or_404(DodomaDog, pk=pk)
    if request.method == 'POST':
        form = DodomaDogForm(request.POST, request.FILES, instance=dog)
        if form.is_valid():
            dog = form.save()
            log_activity(request.user, 'updated dodoma dog', dog)
            return redirect('dodoma_dog_list')
    else:
        form = DodomaDogForm(instance=dog)
    return render(request, 'dodoma_dog_form.html', {'form': form})

@login_required
@location_required(['dodoma'])
def dodoma_dog_delete(request, pk):
    dog = get_object_or_404(DodomaDog, pk=pk)
    if request.method == 'POST':
        dog.delete()
        log_activity(request.user, 'deleted dodoma dog', dog)
        return redirect('dodoma_dog_list')
    return render(request, 'dodoma_dog_confirm_delete.html', {'dog': dog})


@login_required
def dodoma_dog_search(request):
    query = request.GET.get('q')
    if query:
        dogs = DodomaDog.objects.filter(name__icontains=query)
    else:
        dogs = []
    return render(request, 'dodoma_dog_list.html', {'dogs': dogs, 'query': query})


@login_required
def iringa_dog_list(request):
    dogs = IringaDog.objects.all()
    age_min = request.GET.get('age_min')
    age_max = request.GET.get('age_max')
    if breed:
        dogs = dogs.filter(breed__in=breed)
    if age_min and age_max:
        dogs = dogs.filter(date_of_birth__range=[age_min, age_max])
    elif age_min:
        dogs = dogs.filter(date_of_birth__gte=age_min)
    elif age_max:
        dogs = dogs.filter(date_of_birth__lte=age_max)

    context = {'dogs': dogs, 'age_min': age_min, 'age_max': age_max}
    return render(request, 'iringa_dog_list.html', context)

@login_required
@location_required(['iringa'])
def iringa_dog_detail(request, pk):
    dog = get_object_or_404(IringaDog, pk=pk)
    return render(request, 'iringa_dog_detail.html', {'dog': dog})

@login_required
@location_required(['iringa'])
def iringa_dog_create(request):
    if request.method == 'POST':
        form = IringaDogForm(request.POST, request.FILES)
        if form.is_valid():
            dog = form.save()
            log_activity(request.user, 'created iringa dog', dog)
            return redirect('iringa_dog_list')
    else:
        form = IringaDogForm()
    return render(request, 'iringa_dog_form.html', {'form': form})

@login_required
@location_required(['iringa'])
def iringa_dog_update(request, pk):
    dog = get_object_or_404(IringaDog, pk=pk)
    if request.method == 'POST':
        form = IringaDogForm(request.POST, request.FILES, instance=dog)
        if form.is_valid():
            dog = form.save()
            log_activity(request.user, 'updated iringa dog', dog)
            return redirect('iringa_dog_list')
    else:
        form = IringaDogForm(instance=dog)
    return render(request, 'iringa_dog_form.html', {'form': form})

@login_required
@location_required(['iringa'])
def iringa_dog_delete(request, pk):
    dog = get_object_or_404(IringaDog, pk=pk)
    if request.method == 'POST':
        dog.delete()
        log_activity(request.user, 'deleted iringa dog', dog)
        return redirect('iringa_dog_list')
    return render(request, 'iringa_dog_confirm_delete.html', {'dog': dog})


@login_required
def iringa_dog_search(request):
    query = request.GET.get('q')
    if query:
        dogs = IringaDog.objects.filter(name__icontains=query)
    else:
        dogs = []
    return render(request, 'iringa_dog_list.html', {'dogs': dogs, 'query': query})


# Horse Views

@login_required
def hq_horse_list(request):
    horses = HQHorse.objects.all()
    age_min = request.GET.get('age_min')
    age_max = request.GET.get('age_max')
    if breed:
        horses = horses.filter(breed__in=breed)
    if age_min and age_max:
        horses = horses.filter(date_of_birth__range=[age_min, age_max])
    elif age_min:
        horses = horses.filter(date_of_birth__gte=age_min)
    elif age_max:
        horses = horses.filter(date_of_birth__lte=age_max)

    context = {'horses': horses, 'age_min': age_min, 'age_max': age_max}
    return render(request, 'hq_horse_list.html', context)

@login_required
@location_required(['hq'])
def hq_horse_detail(request, pk):
    horse = get_object_or_404(HQHorse, pk=pk)
    return render(request, 'hq_horse_detail.html', {'horse': horse})

@login_required
@location_required(['hq'])
def hq_horse_create(request):
    if request.method == 'POST':
        form = HQHorseForm(request.POST, request.FILES)
        if form.is_valid():
            horse = form.save()
            log_activity(request.user, 'created hq horse', horse)
            return redirect('hq_horse_list')
    else:
        form = HQHorseForm()
    return render(request, 'hq_horse_form.html', {'form': form})

@login_required
@location_required(['hq'])
def hq_horse_update(request, pk):
    horse = get_object_or_404(HQHorse, pk=pk)
    if request.method == 'POST':
        form = HQHorseForm(request.POST, request.FILES, instance=horse)
        if form.is_valid():
            horse = form.save()
            log_activity(request.user, 'updated hq horse', horse)
            return redirect('hq_horse_list')
    else:
        form = HQHorseForm(instance=horse)
    return render(request, 'hq_horse_form.html', {'form': form})

@login_required
@location_required(['hq'])
def hq_horse_delete(request, pk):
    horse = get_object_or_404(HQHorse, pk=pk)
    if request.method == 'POST':
        horse.delete()
        log_activity(request.user, 'deleted hq horse', horse)
        return redirect('hq_horse_list')
    return render(request, 'hq_horse_confirm_delete.html', {'horse': horse})

@login_required
@location_required(['hq'])
def hq_horse_search(request):
    query = request.GET.get('q')
    if query:
        horses = HQHorse.objects.filter(name__icontains=query)
    else:
        horses = []
    return render(request, 'hq_horse_list.html', {'horses': horses, 'query': query})


@login_required
@user_passes_test(lambda u: u.role == 'admin')
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        log_activity(request.user, 'deleted user', user)
        return redirect('user_list')
    return render(request, 'user_confirm_delete.html', {'user': user})


@login_required
@user_passes_test(lambda u: u.role == 'admin')
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

@login_required
@user_passes_test(lambda u: u.role == 'admin')
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'user_detail.html', {'user': user})

@login_required
@user_passes_test(lambda u: u.role == 'admin')
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            log_activity(request.user, 'created user', user)
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'user_form.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.role == 'admin')
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            log_activity(request.user, 'updated user', user)
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'user_form.html', {'form': form})

# Medical Record Views

@veterinarian_required
def medical_record_list(request):
    medical_records = MedicalRecord.objects.all()
    return render(request, 'medical_record_list.html', {'medical_records': medical_records})

@veterinarian_required
def medical_record_detail(request, pk):
    medical_record = get_object_or_404(MedicalRecord, pk=pk)
    return render(request, 'medical_record_detail.html', {'medical_record': medical_record})

@veterinarian_required
def medical_record_create(request):
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            medical_record = form.save()
            log_activity(request.user, 'created medical record', medical_record)
            return redirect('medical_record_list')
    else:
        form = MedicalRecordForm()
    return render(request, 'medical_record_form.html', {'form': form})

@veterinarian_required
def medical_record_update(request, pk):
    medical_record = get_object_or_404(MedicalRecord, pk=pk)
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, instance=medical_record)
        if form.is_valid():
            medical_record = form.save()
            log_activity(request.user, 'updated medical record', medical_record)
            return redirect('medical_record_list')
    else:
        form = MedicalRecordForm(instance=medical_record)
    return render(request, 'medical_record_form.html', {'form': form})

@veterinarian_required
def medical_record_delete(request, pk):
    medical_record = get_object_or_404(MedicalRecord, pk=pk)
    if request.method == 'POST':
        medical_record.delete()
        log_activity(request.user, 'deleted medical record', medical_record)
        return redirect('medical_record_list')
    return render(request, 'medical_record_confirm_delete.html', {'medical_record': medical_record})


# Picture Views

@login_required
def picture_list(request):
    pictures = Picture.objects.all()
    return render(request, 'picture_list.html', {'pictures': pictures})


@login_required
def picture_detail(request, pk):
    picture = get_object_or_404(Picture, pk=pk)

    # Get the name of the related object (dog or horse)
    related_object_name = "Unknown"

    # Check if the picture is related to a dog from any location
    if hasattr(picture, 'hqdog') and picture.hqdog:
        related_object_name = picture.hqdog.name
    elif hasattr(picture, 'tpsmoshidog') and picture.tpsmoshidog:
        related_object_name = picture.tpsmoshidog.name
    elif hasattr(picture, 'dodomadog') and picture.dodomadog:
        related_object_name = picture.dodomadog.name
    elif hasattr(picture, 'iringadog') and picture.iringadog:
        related_object_name = picture.iringadog.name
    # Check if the picture is related to a horse from any location
    elif hasattr(picture, 'hqhorse') and picture.hqhorse:
        related_object_name = picture.hqhorse.name
    elif hasattr(picture, 'dodomahorse') and picture.dodomahorse:
        related_object_name = picture.dodomahorse.name
    elif hasattr(picture, 'iringahorse') and picture.iringahorse:
        related_object_name = picture.iringahorse.name
    elif hasattr(picture, 'tpsmoshihorse') and picture.tpsmoshihorse:
        related_object_name = picture.tpsmoshihorse.name
    return render(request, 'picture_detail.html', {'picture': picture, 'related_object_name': related_object_name})

@login_required
def picture_create(request):
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)  # Ensure request.FILES is included
        if form.is_valid():
            picture = form.save()
            log_activity(request.user, 'created picture', picture)
            return redirect('picture_list')
    else:
        form = PictureForm()
    return render(request, 'picture_form.html', {'form': form})

@login_required
def picture_update(request, pk):
    picture = get_object_or_404(Picture, pk=pk)
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES, instance=picture)  # Ensure request.FILES is included
        if form.is_valid():
            picture = form.save()
            log_activity(request.user, 'updated picture', picture)
            return redirect('picture_list')
    else:
        form = PictureForm(instance=picture)
    return render(request, 'picture_form.html', {'form': form})

@login_required
def picture_delete(request, pk):
    picture = get_object_or_404(Picture, pk=pk)
    if request.method == 'POST':
        picture.delete()
        log_activity(request.user, 'deleted picture', picture)
        return redirect('picture_list')
    return render(request, 'picture_confirm_delete.html', {'picture': picture})


@login_required
@user_passes_test(lambda u: u.role == 'admin')
def activity_log_list(request):
    activities = ActivityLog.objects.order_by('-timestamp')[:20]
    return render(request, 'activity_log_list.html', {'activities': activities})

# Dodoma Horse Views

@login_required
def dodoma_horse_list(request):
    horses = DodomaHorse.objects.all()
    age_min = request.GET.get('age_min')
    age_max = request.GET.get('age_max')
    if breed:
        horses = horses.filter(breed__in=breed)
    if age_min and age_max:
        horses = horses.filter(date_of_birth__range=[age_min, age_max])
    elif age_min:
        horses = horses.filter(date_of_birth__gte=age_min)
    elif age_max:
        horses = horses.filter(date_of_birth__lte=age_max)

    context = {'horses': horses, 'age_min': age_min, 'age_max': age_max}
    return render(request, 'dodoma_horse_list.html', context)

@login_required
@location_required(['dodoma'])
def dodoma_horse_create(request):
    if request.method == 'POST':
        form = DodomaHorseForm(request.POST, request.FILES)
        if form.is_valid():
            horse = form.save()
            log_activity(request.user, 'created dodoma horse', horse)
            return redirect('dodoma_horse_list')
    else:
        form = DodomaHorseForm()
    return render(request, 'dodoma_horse_form.html', {'form': form})

@login_required
@location_required(['dodoma'])
def dodoma_horse_update(request, pk):
    horse = get_object_or_404(DodomaHorse, pk=pk)
    if request.method == 'POST':
        form = DodomaHorseForm(request.POST, request.FILES, instance=horse)
        if form.is_valid():
            horse = form.save()
            log_activity(request.user, 'updated dodoma horse', horse)
            return redirect('dodoma_horse_list')
    else:
        form = DodomaHorseForm(instance=horse)
    return render(request, 'dodoma_horse_form.html', {'form': form})

@login_required
@location_required(['dodoma'])
def dodoma_horse_delete(request, pk):
    horse = get_object_or_404(DodomaHorse, pk=pk)
    if request.method == 'POST':
        horse.delete()
        log_activity(request.user, 'deleted dodoma horse', horse)
        return redirect('dodoma_horse_list')
    return render(request, 'dodoma_horse_confirm_delete.html', {'horse': horse})

@login_required
@location_required(['dodoma'])
def dodoma_horse_search(request):
    query = request.GET.get('q')
    if query:
        horses = DodomaHorse.objects.filter(name__icontains=query)
    else:
        horses = []
    return render(request, 'dodoma_horse_list.html', {'horses': horses, 'query': query})


@login_required
@location_required(['dodoma'])
def dodoma_horse_detail(request, pk):
    horse = get_object_or_404(DodomaHorse, pk=pk)

    # Get related medical records
    medical_records = MedicalRecord.objects.filter(
        content_type__model='dodomahorse',
        object_id=horse.id
    ).order_by('-date')

    # Get related pictures
    pictures = Picture.objects.filter(
        content_type__model='dodomahorse',
        object_id=horse.id
    ).order_by('-upload_date')

    # Calculate age
    from datetime import date
    today = date.today()
    age_years = today.year - horse.date_of_birth.year - (
            (today.month, today.day) < (horse.date_of_birth.month, horse.date_of_birth.day)
    )

    # Get activity logs related to this horse
    activity_logs = ActivityLog.objects.filter(
        content_type__model='dodomahorse',
        object_id=horse.id
    ).order_by('-timestamp')[:10]  # Get the 10 most recent activities

    context = {
        'horse': horse,
        'medical_records': medical_records,
        'pictures': pictures,
        'age_years': age_years,
        'activity_logs': activity_logs,
    }

    return render(request, 'dodoma_horse_detail.html', context)

# Iringa Horse Views

@login_required
def iringa_horse_list(request):
    horses = IringaHorse.objects.all()
    age_min = request.GET.get('age_min')
    age_max = request.GET.get('age_max')
    if breed:
        horses = horses.filter(breed__in=breed)
    if age_min and age_max:
        horses = horses.filter(date_of_birth__range=[age_min, age_max])
    elif age_min:
        horses = horses.filter(date_of_birth__gte=age_min)
    elif age_max:
        horses = horses.filter(date_of_birth__lte=age_max)

    context = {'horses': horses, 'age_min': age_min, 'age_max': age_max}
    return render(request, 'iringa_horse_list.html', context)

@login_required
@location_required(['iringa'])
def iringa_horse_detail(request, pk):
    horse = get_object_or_404(IringaHorse, pk=pk)
    return render(request, 'iringa_horse_detail.html', {'horse': horse})

@login_required
@location_required(['iringa'])
def iringa_horse_create(request):
    if request.method == 'POST':
        form = IringaHorseForm(request.POST, request.FILES)
        if form.is_valid():
            horse = form.save()
            log_activity(request.user, 'created iringa horse', horse)
            return redirect('iringa_horse_list')
    else:
        form = IringaHorseForm()
    return render(request, 'iringa_horse_form.html', {'form': form})

@login_required
@location_required(['iringa'])
def iringa_horse_update(request, pk):
    horse = get_object_or_404(IringaHorse, pk=pk)
    if request.method == 'POST':
        form = IringaHorseForm(request.POST, request.FILES, instance=horse)
        if form.is_valid():
            horse = form.save()
            log_activity(request.user, 'updated iringa horse', horse)
            return redirect('iringa_horse_list')
    else:
        form = IringaHorseForm(instance=horse)
    return render(request, 'iringa_horse_form.html', {'form': form})

@login_required
@location_required(['iringa'])
def iringa_horse_delete(request, pk):
    horse = get_object_or_404(IringaHorse, pk=pk)
    if request.method == 'POST':
        horse.delete()
        log_activity(request.user, 'deleted iringa horse', horse)
        return redirect('iringa_horse_list')
    return render(request, 'iringa_horse_confirm_delete.html', {'horse': horse})

@login_required
@location_required(['iringa'])
def iringa_horse_search(request):
    query = request.GET.get('q')
    if query:
        horses = IringaHorse.objects.filter(name__icontains=query)
    else:
        horses = []
    return render(request, 'iringa_horse_list.html', {'horses': horses, 'query': query})

# TPS Moshi Horse Views

@login_required
def tps_moshi_horse_list(request):
    horses = TpsMoshiHorse.objects.all()
    age_min = request.GET.get('age_min')
    age_max = request.GET.get('age_max')
    if breed:
        horses = horses.filter(breed__in=breed)
    if age_min and age_max:
        horses = horses.filter(date_of_birth__range=[age_min, age_max])
    elif age_min:
        horses = horses.filter(date_of_birth__gte=age_min)
    elif age_max:
        horses = horses.filter(date_of_birth__lte=age_max)

    context = {'horses': horses, 'age_min': age_min, 'age_max': age_max}
    return render(request, 'tps_moshi_horse_list.html', context)

@login_required
@location_required(['tps_moshi'])
def tps_moshi_horse_detail(request, pk):
    horse = get_object_or_404(TpsMoshiHorse, pk=pk)
    return render(request, 'tps_moshi_horse_detail.html', {'horse': horse})

@login_required
@location_required(['tps_moshi'])
def tps_moshi_horse_create(request):
    if request.method == 'POST':
        form = TpsMoshiHorseForm(request.POST, request.FILES)
        if form.is_valid():
            horse = form.save()
            log_activity(request.user, 'created tps moshi horse', horse)
            return redirect('tps_moshi_horse_list')
    else:
        form = TpsMoshiHorseForm()
    return render(request, 'tps_moshi_horse_form.html', {'form': form})

@login_required
@location_required(['tps_moshi'])
def tps_moshi_horse_update(request, pk):
    horse = get_object_or_404(TpsMoshiHorse, pk=pk)
    if request.method == 'POST':
        form = TpsMoshiHorseForm(request.POST, request.FILES, instance=horse)
        if form.is_valid():
            horse = form.save()
            log_activity(request.user, 'updated tps moshi horse', horse)
            return redirect('tps_moshi_horse_list')
    else:
        form = TpsMoshiHorseForm(instance=horse)
    return render(request, 'tps_moshi_horse_form.html', {'form': form})

@login_required
@location_required(['tps_moshi'])
def tps_moshi_horse_delete(request, pk):
    horse = get_object_or_404(TpsMoshiHorse, pk=pk)
    if request.method == 'POST':
        horse.delete()
        log_activity(request.user, 'deleted tps moshi horse', horse)
        return redirect('tps_moshi_horse_list')
    return render(request, 'tps_moshi_horse_confirm_delete.html', {'horse': horse})

@login_required
@location_required(['tps_moshi'])
def tps_moshi_horse_search(request):
    query = request.GET.get('q')
    if query:
        horses = TpsMoshiHorse.objects.filter(name__icontains=query)
    else:
        horses = []
    return render(request, 'tps_moshi_horse_list.html', {'horses': horses, 'query': query})


from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import Picture
from .forms import PictureForm


class PictureListView(ListView):
    model = Picture
    template_name = 'picture_list.html'
    context_object_name = 'pictures'
    ordering = ['-created_at']


class PictureDetailView(DetailView):
    model = Picture
    template_name = 'picture_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the related object name to the template
        context['related_object_name'] = self.object.related_object_name
        return context


class PictureCreateView(CreateView):
    model = Picture
    form_class = PictureForm
    template_name = 'picture_form.html'
    success_url = reverse_lazy('picture_list')


class PictureUpdateView(UpdateView):
    model = Picture
    form_class = PictureForm
    template_name = 'picture_form.html'

    def get_success_url(self):
        return reverse_lazy('picture_detail', kwargs={'pk': self.object.pk})


class PictureDeleteView(DeleteView):
    model = Picture
    template_name = 'picture_confirm_delete.html'
    success_url = reverse_lazy('picture_list')


def add_animal_selection(request):
    """
    View to display a selection page for adding different types of animals
    at different locations.
    """
    # Simple context to use in the template
    context = {
        'title': 'Add New Animal',
        'locations': [
            {'id': 'hq', 'name': 'Headquarters'},
            {'id': 'tps_moshi', 'name': 'TPS Moshi'},
            {'id': 'dodoma', 'name': 'Dodoma'},
            {'id': 'iringa', 'name': 'Iringa'},
        ],
        'animal_types': [
            {'id': 'dog', 'name': 'Dog'},
            {'id': 'horse', 'name': 'Horse'},
        ]
    }

    return render(request, 'add_animal_selection.html', context)


def transfer_animal_selection(request):
    """
    View to display a selection page for transferring animals between locations.
    """
    # Context for the template
    context = {
        'title': 'Initiate Animal Transfer',
        'locations': [
            {'id': 'hq', 'name': 'Headquarters'},
            {'id': 'tps_moshi', 'name': 'TPS Moshi'},
            {'id': 'dodoma', 'name': 'Dodoma'},
            {'id': 'iringa', 'name': 'Iringa'},
        ],
        'animal_types': [
            {'id': 'dog', 'name': 'Dog'},
            {'id': 'horse', 'name': 'Horse'},
        ]
    }

    return render(request, 'transfer_animal_selection.html', context)


def generate_report(request):
    """
    View to generate reports based on selected criteria.
    """
    # Context for the template
    context = {
        'title': 'Generate Report',
        'report_types': [
            {'id': 'animal_inventory', 'name': 'Animal Inventory'},
            {'id': 'medical_records', 'name': 'Medical Records'},
            {'id': 'transfers', 'name': 'Transfer History'},
            {'id': 'activity_logs', 'name': 'Activity Logs'},
        ],
        'locations': [
            {'id': 'all', 'name': 'All Locations'},
            {'id': 'hq', 'name': 'Headquarters'},
            {'id': 'tps_moshi', 'name': 'TPS Moshi'},
            {'id': 'dodoma', 'name': 'Dodoma'},
            {'id': 'iringa', 'name': 'Iringa'},
        ],
        'animal_types': [
            {'id': 'all', 'name': 'All Types'},
            {'id': 'dog', 'name': 'Dogs'},
            {'id': 'horse', 'name': 'Horses'},
        ]
    }

    return render(request, 'generate_report.html', context)

@login_required
def transfer_list(request):
    transfers = AnimalTransfer.objects.all().order_by('-date')
    return render(request, 'transfer_list.html', {'transfers': transfers})

def transfer_detail(request, pk):
    transfer = get_object_or_404(AnimalTransfer, pk=pk)
    return render(request, 'transfer_detail.html', {'transfer': transfer})

def transfer_create(request):
    if request.method == 'POST':
        # Process form submission
        pass
    return render(request, 'transfer_form.html')

def transfer_update(request, pk):
    transfer = get_object_or_404(AnimalTransfer, pk=pk)
    if request.method == 'POST':
        # Process form submission
        pass
    return render(request, 'transfer_form.html', {'transfer': transfer})

def transfer_delete(request, pk):
    transfer = get_object_or_404(AnimalTransfer, pk=pk)
    if request.method == 'POST':
        transfer.delete()
        return redirect('transfer_list')
    return render(request, 'transfer_confirm_delete.html', {'transfer': transfer})

def transfer_approve(request, pk):
    transfer = get_object_or_404(AnimalTransfer, pk=pk)
    transfer.approved = True
    transfer.save()
    return redirect('transfer_list')

@login_required
@user_passes_test(lambda u: u.role == 'admin' or u.role == 'all', login_url='dashboard')
def admin_dashboard(request, role='admin'):  # Default to 'admin' role

    return render(request, 'admin_dashboard.html', {'role': role})

@login_required
def user_dashboard(request):
    # Add user-specific content here
    return render(request, 'user_dashboard.html')


@login_required
def veterinarian_dashboard(request):
    # Add veterinarian-specific content here
    return render(request, 'veterinarian_dashboard.html')
def transfer_report(request, pk):
    transfer = get_object_or_404(AnimalTransfer, pk=pk)
    # Generate report logic here
    return HttpResponse("Report for transfer " + str(pk))


def veterinarian_dashboard(request):
