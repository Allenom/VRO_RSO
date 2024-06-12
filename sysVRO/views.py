import django.contrib.auth.views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout

from .forms import CreateUserForm, ProfileEditForm, UserEditForm, DetachmentUpdateForm, PartCreateForm, PartUpdateForm, \
    EventForm
from .models import Event, Profile, Detachment, Mark, Area, Institution


def index_page(request):
    return render(request, 'index.html')


def about_page(request):
    return render(request, 'about.html')


def events_page(request):
    events = Event.objects.all
    context = {'events': events}
    return render(request, 'events.html', context)


class EventCreateView(CreateView):
    form_class = EventForm
    success_url = reverse_lazy("events")
    template_name = "events/create.html"

    def form_valid(self, form):
        if self.request.user.profile.position == '':
            return render(self.request, self.template_name)
        event = form.save()
        event.save()
        self.success_url = reverse_lazy("event", kwargs={"event_id": event.id})
        return super(EventCreateView, self).form_valid(form)


def event_page(request, event_id):
    event = Event.objects.filter(id=event_id)
    admin = event[0].admin.filter(id=request.user.profile.id)
    contact = event[0].contact
    part = {}
    if request.user.is_authenticated:
        part = Mark.objects.filter(event_id=event_id, profile_id=request.user.profile.id)

    goings = Mark.objects.filter(event_id=event_id, deleted=False)
    more = len(goings)-5
    goings = goings[:5]
    context = {'contact': contact, 'event': event, 'part': part, 'goings': goings, 'more': more, 'admin': admin}
    return render(request, 'events/event.html', context)


class EventUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "/login/"
    # template_name = 'forum/edit.html'
    # form_class = EventForm
    # success_url = reverse_lazy('index_forum')
    #
    # model = Event
    template_name = 'events/edit.html'
    form_class = EventForm
    success_url = reverse_lazy('events')

    model = Event

    def form_valid(self, form):
        with transaction.atomic():
            context = self.get_context_data()
            if form.is_valid():
                context = self.get_context_data()
                event = Event.objects.get(pk=self.get_object().id)
                admin = event.admin.get(id=self.request.user.profile.id)
                if admin:
                    form.save()
                    self.success_url = reverse_lazy("event", kwargs={"event_id": self.get_object().id})
            else:
                return self.render_to_response(context)
        return super(EventUpdateView, self).form_valid(form)

    # def get_object(self, queryset=None):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = Event.objects.get(pk=self.get_object().id)
        admin = event.admin.get(id=self.request.user.profile.id)
        context.update({'admin': admin})
        return context


def take_part(request, event_id):
    if not request.user.is_authenticated:
        return redirect('/login/?next=/events/'+str(event_id))

    event = Event.objects.filter(id=event_id)

    part = Mark.objects.filter(event_id=event_id, profile_id=request.user.profile.id)

    # Если объекта part нету, то create, если есть то update (Переключение состояние удален)
    if len(part) < 1:
        part_new = Mark(event=event[0], profile=request.user.profile)
        part_new.save()
    else:
        part_old = Mark.objects.get(id=part[0].id)
        part_old.deleted = not (part_old.deleted)
        part_old.save()

    url_to = '/events/' + str(event_id) + '/'
    return redirect(url_to)


def joining_page(request):
    return render(request, 'joining.html')


def detachments_page(request):
    detachments = Detachment.objects.all
    areas = Area.objects.all
    institutions = Institution.objects.all
    context = {'detachments': detachments, 'areas': areas, 'institutions': institutions,}
    return render(request, 'joining/detachments.html', context)


def detachment_page(request, detachment_id):
    detachment = Detachment.objects.filter(id=detachment_id)
    detachment_members = Profile.objects.filter(id=detachment_id)
    more = len(detachment_members)-5
    detachment_members = detachment_members[:5]
    context = {'detachment': detachment, 'detachment_members': detachment_members, 'more': more}
    return render(request, 'joining/detachments/detachment.html', context)


# def index_page(request):
#     return render(request, 'index.html')


def profile_page(request):
    if not request.user.is_authenticated:
        return redirect('/login/?next=/profile/')
    context = {}
    if request.user.profile.detachment:
        detachment = Detachment.objects.filter(id=request.user.profile.detachment.id)
        commander = request.user.profile.detachment.profile_set.filter(position='Командир')
        commissar = request.user.profile.detachment.profile_set.filter(position='Комиссар')
        secretary = request.user.profile.detachment.profile_set.filter(position='Мастер-методист')
        members = commander.union(commissar, secretary)
        context.update(
            {'detachment': detachment, 'commander': commander, 'commissar': commissar, 'secretary': secretary,
             'members': members})
    if request.user.profile.mark_set:
        marks = Mark.objects.filter(profile__pk=request.user.profile.id, deleted=False).order_by('-published')
        points = 0
        for mark in marks:
            if mark.confirmed and not mark.deleted:
                points += mark.points
        marks = marks[:2]
        context.update({'marks': marks, 'points': points})
    return render(request, 'profile.html', context)


# def profile_detachment_page(request):
#     if request.user.profile.detachment:
#         detachment = Detachment.objects.filter(id=request.user.profile.detachment.id)
#         commander = request.user.profile.detachment.profile_set.filter(position='Командир')
#         commissar = request.user.profile.detachment.profile_set.filter(position='Комиссар')
#         secretary = request.user.profile.detachment.profile_set.filter(position='Мастер-методист')
#         context = {'detachment': detachment, 'commander': commander, 'commissar': commissar, 'secretary': secretary}
#         return render(request, 'profile/detachment.html', context)
#     else:
#         return render(request, 'profile/detachment.html')

class DetachmentUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "/login/"

    template_name = 'profile/detachment.html'
    form_class = DetachmentUpdateForm
    success_url = reverse_lazy('profile_detachment')

    model = Detachment

    # @method_decorator(login_required(login_url='login'))
    # def dispatch(self, request, *args, **kwargs):
    #     super(DetachmentUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        context = self.get_context_data()
        with transaction.atomic():
            if form.is_valid():
                form.save()
            else:
                return self.render_to_response(context)
        return super(DetachmentUpdateView, self).form_valid(form)

    def get_object(self, queryset=None):
        return self.request.user.profile.detachment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.profile.detachment:
            detachment = Detachment.objects.filter(id=self.request.user.profile.detachment.id)
            members = self.request.user.profile.detachment.profile_set
            commander = members.filter(position='Командир')
            commissar = members.filter(position='Комиссар')
            secretary = members.filter(position='Мастер-методист')
            specialists = members.filter(position='Специалист')
            warriors = members.filter(position='', membership_fee=True)
            candidates = members.filter(position='', membership_fee=False)
            count = members.count()
            members = members.filter()
            context.update({'detachment': detachment, 'commander': commander, 'commissar': commissar,
                            'secretary': secretary, 'specialists': specialists, 'warriors': warriors,
                            'candidates': candidates, 'count': count, 'members': members})
            return context
        else:
            return context
        
class DetachmentUpdateView1(LoginRequiredMixin, UpdateView):
    login_url = "/login/"

    template_name = 'joining/detachments/edit.html'
    form_class = DetachmentUpdateForm
    success_url = reverse_lazy('profile_detachment')

    model = Detachment

    # @method_decorator(login_required(login_url='login'))
    # def dispatch(self, request, *args, **kwargs):
    #     super(DetachmentUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        context = self.get_context_data()
        with transaction.atomic():
            if form.is_valid():
                form.save()
            else:
                return self.render_to_response(context)
        return super(DetachmentUpdateView1, self).form_valid(form)

    def get_object(self, queryset=None):
        return self.request.user.profile.detachment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.profile.detachment:
            detachment = Detachment.objects.filter(id=self.request.user.profile.detachment.id)
            members = self.request.user.profile.detachment.profile_set
            commander = members.filter(position='Командир')
            commissar = members.filter(position='Комиссар')
            secretary = members.filter(position='Мастер-методист')
            specialists = members.filter(position='Специалист')
            warriors = members.filter(position='', membership_fee=True)
            candidates = members.filter(position='', membership_fee=False)
            count = members.count()
            members = members.filter()
            context.update({'detachment': detachment, 'commander': commander, 'commissar': commissar,
                            'secretary': secretary, 'specialists': specialists, 'warriors': warriors,
                            'candidates': candidates, 'count': count, 'members': members})
            return context
        else:
            return context


def profile_events_page(request):
    if not request.user.is_authenticated:
        return redirect('/login/?next=/profile/events/')
    marks = Mark.objects.filter(profile__pk=request.user.profile.id, deleted=False)
    # future = marks.filter()
    # past = marks.filter()
    context = {'marks': marks}
    return render(request, 'profile/events.html', context)


class ProfileEditView(LoginRequiredMixin, UpdateView):
    login_url = "/login/"

    template_name = 'profile/settings.html'
    form_class = ProfileEditForm
    success_url = reverse_lazy('profile_settings')
    model = Profile

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование профиля пользователя: {self.request.user.username}'
        if self.request.POST:
            context['user_form'] = UserEditForm(self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = UserEditForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        with transaction.atomic():
            if all([form.is_valid(), user_form.is_valid()]):
                user_form.save()
                form.save()
            else:
                context.update({'user_form': user_form})
                return self.render_to_response(context)
        return super(ProfileEditView, self).form_valid(form)


class SignUp(CreateView):
    form_class = CreateUserForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"

    def form_valid(self, form):
        c = {'form': form, }
        user = form.save(commit=False)
        # Cleaned(normalized) data
        # institution = form.cleaned_data['institution']
        telephone = form.cleaned_data['telephone']
        password = form.cleaned_data['password']
        repeat_password = form.cleaned_data['repeat_password']
        if password != repeat_password:
            form.add_error('repeat_password', "Пароли не совпадают")
            return render(self.request, self.template_name, c)
        user.set_password(password)
        user.save()

        # Create UserProfile model
        Profile.objects.create(user=user, telephone=telephone)

        return super(SignUp, self).form_valid(form)


def coming_soon_page(request):
    return render(request, 'coming_soon.html')


def page_404(request):
    return render(request, '404.html')


def agreements_page(request):
    return render(request, 'agreements.html')

def logout_view(request):
    logout(request)
    return redirect('/login')