"""
This module contains class-based views for interactions application representing
"""
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, RedirectView
from crm.models import Project
from crm.views import FilteredListView
from interactions.filters import InteractionFilter
from interactions.forms import InteractionForm, KeywordFormSet
from interactions.models import Interaction, Mark, Keyword


class InteractionsListView(PermissionRequiredMixin, FilteredListView):
    """
    Class representing interactions objects list view
    """
    model = Interaction  # object model class
    paginate_by = 5  # count of objects on page
    paginate_orphans = 1  # min objects on page
    filterset_class = InteractionFilter  # class with set of filters for interaction model
    permission_required = 'interactions.view_interaction'  # (str) permission to see the page


class InteractionDetailView(PermissionRequiredMixin, DetailView):
    """
    Class for view details of interaction
    """
    model = Interaction  # object model class
    permission_required = 'interactions.view_interaction'  # (str) permission to see the page

    def get_context_data(self, **kwargs):
        """
        Returns context extended with list of available marks
        """
        context = super(InteractionDetailView, self).get_context_data(**kwargs)
        mark_list = [i for i in range(-5, 6)]
        context['mark_list'] = mark_list
        return context


class InteractionAddMarkRedirectView(PermissionRequiredMixin, RedirectView):
    """
    Class for redirect after saving mark data
    """
    pattern_name = 'interaction-details'  # name of url pattern for redirect
    permission_required = 'interactions.add_mark'  # (str) permission to see the page
    queryset = Interaction.objects.all().prefetch_related('Mark').prefetch_related('Project')  # set of interactions

    def get_redirect_url(self, *args, **kwargs):
        """
        Apply mark data from kwargs (save Mark object and update interaction's rating).
        Returns redirect to pattern_name with args
        """
        interaction = get_object_or_404(Interaction, pk=kwargs['pk'])
        rate = self.request.GET.get('mark', 0)
        mark, created = Mark.objects.get_or_create(
            interaction=interaction,
            manager=self.request.user,
            defaults={'rate': rate},
        )
        if not created:
            mark.rate = rate
        mark.save()
        avg = Mark.objects.filter(interaction=interaction).aggregate(rate_avg=Avg('rate'))['rate_avg']
        interaction.rating = avg
        interaction.save()
        return super().get_redirect_url(*args, **kwargs)


class InteractionCreateView(PermissionRequiredMixin, CreateView):
    """
    Class for creating Interaction object view
    """
    model = Interaction  # object model class
    form_class = InteractionForm  # form-class for interaction creating
    permission_required = 'interactions.add_interaction'  # (str) permission to see the page
    project = None  # project for interaction (related object)

    def get_context_data(self, **kwargs):
        """
        Extends context with related data and formset for keywords add
        """
        context = super(InteractionCreateView, self).get_context_data(**kwargs)
        self.project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        print('project=', self.project)
        context['project'] = self.project
        context['client'] = self.project.company
        context['manager'] = self.request.user
        if self.request.POST:
            context['keyword_formset'] = KeywordFormSet(self.request.POST)
            context['keyword_formset'].full_clean()
        else:
            context['keyword_formset'] = KeywordFormSet()
        return context

    def form_valid(self, form):
        """
        saving creation form data and keywords from formsets
        """
        context = self.get_context_data(form=form)
        formset_keyword = context['keyword_formset']
        self.object = form.save(commit=False)
        self.object.project = context['project']  # self.project
        self.object.manager = self.request.user
        self.object.save()
        if formset_keyword.is_valid():
            for form_obj in formset_keyword:
                if form_obj.is_valid():
                    keyword = form_obj.save(commit=False)
                    if len(keyword.word) > 0 and not Keyword.objects.filter(word=keyword.word).exists():
                        print('new keyword:', keyword)
                        self.object.keyword.create(word=keyword.word)
                        # new_keyword = keyword.save()
                        # self.object.keyword.add(new_keyword)
        return super(InteractionCreateView, self).form_valid(form)

    def get_success_url(self):
        """
        Returns url for redirect on successful create object
        """
        return reverse_lazy('interaction-details', args=[self.object.pk])


class InteractionUpdateView(PermissionRequiredMixin, UpdateView):
    """
    Class representing ViewForm for editing data of Interaction model object.
    Based on generic.UpdateView
   """
    model = Interaction  # object model class
    form_class = InteractionForm  # form-class for interaction updating
    permission_required = 'interactions.change_interaction'  # (str) permission to see the page

    def get_context_data(self, **kwargs):
        """
        Extends context with formsets for keywords add
        """
        context = super(InteractionUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['keyword_formset'] = KeywordFormSet(self.request.POST)
            context['keyword_formset'].full_clean()
        else:
            context['keyword_formset'] = KeywordFormSet()
        return context

    def form_valid(self, form):
        """
        saving update form data and keywords from formsets
        """
        context = self.get_context_data(form=form)
        formset_keyword = context['keyword_formset']
        self.object = form.save()
        if formset_keyword.is_valid():
            for form_obj in formset_keyword:
                if form_obj.is_valid():
                    keyword = form_obj.save(commit=False)
                    if len(keyword.word) > 0 and not Keyword.objects.filter(word=keyword.word).exists():
                        print('new keyword:', keyword)
                        self.object.keyword.create(word=keyword.word)
                        # new_keyword = keyword.save(force_insert=True)
                        # self.object.keyword.add(new_keyword)
        return super().form_valid(form)

    def get_success_url(self):
        """
        Returns url for redirect on successful update object
        """
        return reverse_lazy('interaction-details', args=[self.object.pk])


class InteractionDeleteView(PermissionRequiredMixin, DeleteView):
    model = Interaction  # object model class
    permission_required = 'interaction.delete_interaction'  # (str) permission to see the page

    def get_success_url(self):
        """
        Returns url for redirect on successful delete object
        """
        return reverse_lazy('project-details', args=[self.object.project.pk])
