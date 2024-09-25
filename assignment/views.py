from django.db import transaction
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, FormView

from .forms import AssignmentForm, FileForm
from .models import File, Assignment


def main_page(request):
    return render(request, 'base.html')


class AssignmentView(ListView):
    template_name = 'assignment/assignment_list.html'
    model = Assignment
    context_object_name = 'assignments'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        if not request.GET.get('page'):
            return redirect(f'{request.path}?page=1')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['status_color_labels'] = Assignment.Status.COLOR_LABELS
        context['priority_color_labels'] = Assignment.PRIORITY_COLOR_LABELS
        return context


class AssignmentInfo(DetailView):
    template_name = 'assignment/assignment_info.html'
    model = Assignment
    context_object_name = 'assignment'
    slug_url_kwarg = 'assignment_uuid'
    slug_field = 'uuid'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['assignment'].subject
        context['status_color_labels'] = Assignment.Status.COLOR_LABELS
        context['priority_color_labels'] = Assignment.PRIORITY_COLOR_LABELS
        return context


class CreateAssignment(View):

    def get(self, request):
        assignment_form = AssignmentForm()
        file_form = FileForm()
        context = {'assignment_form': assignment_form,
                   'file_form': file_form}
        return render(request, 'assignment/create_assignment.html', context=context)

    def post(self, request: HttpRequest):
        assignment_form = AssignmentForm(request.POST)
        file_form = FileForm(request.POST, request.FILES)
        if assignment_form.is_valid() and file_form.is_valid():
            with transaction.atomic():
                assignment = assignment_form.save()
                File.objects.bulk_create([
                    File(file=file, assignment=assignment) for file in file_form.files.getlist('file')
                ])
        else:
            context = {'assignment_form': assignment_form,
                       'file_form': file_form}
            return render(request, 'assignment/create_assignment.html', context=context)
        return redirect('assignment_list')
