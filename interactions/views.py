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
    model = Interaction
    paginate_by = 5
    paginate_orphans = 1
    filterset_class = InteractionFilter
    permission_required = 'interactions.view_interaction'


class InteractionDetailView(PermissionRequiredMixin, DetailView):
    model = Interaction
    permission_required = 'interactions.view_interaction'

    def get_context_data(self, **kwargs):
        context = super(InteractionDetailView, self).get_context_data(**kwargs)

        mark_list = [i for i in range(-5, 6)]
        context['mark_list'] = mark_list
        return context


class InteractionAddMarkRedirectView(PermissionRequiredMixin, RedirectView):
    pattern_name = 'interaction-details'
    permission_required = 'interactions.add_mark'
    queryset = Interaction.objects.all().prefetch_related('Mark').prefetch_related('Project')

    def get_redirect_url(self, *args, **kwargs):
        interaction = get_object_or_404(Interaction, pk=kwargs['pk'])
        rate = self.request.GET.get('mark', 0)
        # mark = Mark.objects.get(interaction=interaction)
        mark, created = Mark.objects.get_or_create(
            interaction=interaction,
            manager=self.request.user,
            defaults={'rate': rate},
        )
        if not created:
            mark.rate = rate
        # mark = Mark(rate=rate, interaction=interaction, manager=self.request.user)
        print('Mark created=', created)
        mark.save()
        avg = Mark.objects.filter(interaction=interaction).aggregate(rate_avg=Avg('rate'))['rate_avg']
        print(avg)
        interaction.rating = avg
        interaction.save()
        return super().get_redirect_url(*args, **kwargs)


class InteractionCreateView(PermissionRequiredMixin, CreateView):
    model = Interaction
    form_class = InteractionForm
    permission_required = 'interactions.add_interaction'
    project = None

    def get_context_data(self, **kwargs):
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
            context['keyword_formset'] = KeywordFormSet()  # KeywordInlineFormset()  #
        return context

    def form_valid(self, form):
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
        return reverse_lazy('interaction-details', args=[self.object.pk])


class InteractionUpdateView(PermissionRequiredMixin, UpdateView):
    """
    Class representing ViewForm for editing data of Interaction model object.
    Based on generic.UpdateView
    attributes:
    model - model-class representing object's data
    form_class - form-based class with set of fields to display on form for editing object data

    methods:

    """
    model = Interaction
    form_class = InteractionForm
    permission_required = 'interactions.change_interaction'

    def get_context_data(self, **kwargs):
        context = super(InteractionUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['keyword_formset'] = KeywordFormSet(self.request.POST)
            context['keyword_formset'].full_clean()
        else:
            context['keyword_formset'] = KeywordFormSet()
        return context

    def form_valid(self, form):
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
                        # new_keyword = keyword.save()
                        # self.object.keyword.add(new_keyword)
                        # self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('interaction-details', args=[self.object.pk])


class InteractionDeleteView(PermissionRequiredMixin, DeleteView):
    model = Interaction
    permission_required = 'interaction.delete_interaction'

    def get_success_url(self):
        return reverse_lazy('project-details', args=[self.object.project.pk])
