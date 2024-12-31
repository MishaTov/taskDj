from django.db import transaction
from django.http import FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.timezone import localtime
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView

from template_tags.templatetags.custom_tags import get_filename
from .forms import AssignmentForm, FileForm, CommentForm, FilterForm
from .models import File, Assignment


def main_page(request):
    return render(request, 'base.html')


class AssignmentView(ListView):
    template_name = 'assignment/assignment_list.html'
    model = Assignment
    context_object_name = 'assignments'
    paginate_by = 5
    ordering = '-created_at'
    extra_context = {'title': 'Assignments',
                     'status_color_labels': Assignment.Status.COLOR_LABELS,
                     'priority_color_labels': Assignment.PRIORITY_COLOR_LABELS}

    def __init__(self):
        super().__init__()
        self.pagination_options = {
            '5': 5,
            '10': 10,
            '20': 20,
            '50': 50
        }
        self.ordering_options = {
            '-created_at': 'Creation date',
            'deadline': 'Deadline',
            'priority': 'Priority'
        }

    def get(self, request, *args, **kwargs):
        request.GET = self.process_request_params()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        object_list = self.model.get_filtrated_queryset(self.request.GET, self.ordering)
        context = super().get_context_data(object_list=object_list, **kwargs)
        paginator = context.get('paginator')
        current_page_number = context.get('page_obj').number
        context.update({
            'paginate_by': self.paginate_by,
            'order_by': self.ordering_options[self.ordering],
            'pages': paginator.get_elided_page_range(number=current_page_number, on_each_side=1, on_ends=1),
            'pagination_options': self.pagination_options,
            'ordering_options': self.ordering_options,
            'reverse': self.request.GET.get('reverse') == 'True',
            'filter_form': FilterForm(self.request.GET),
        })
        return context

    def process_request_params(self):
        print(self.paginate_by)
        params = self.request.GET.copy()
        # paginate_by = params.get('paginate_by', self.paginate_by)
        order_by = params.get('order_by', self.ordering)
        # if paginate_by != self.paginate_by and paginate_by in self.pagination_options:
        #     self.calculate_page_number()
        #     self.paginate_by = int(paginate_by)
        if order_by != self.ordering and order_by in self.ordering_options:
            self.ordering = order_by
        params['paginate_by'] = self.paginate_by
        params['order_by'] = self.ordering
        return params
    
    def get_paginate_by(self, queryset):
        paginate_by = self.request.GET.get('paginate_by', self.paginate_by)
        if paginate_by != self.paginate_by and paginate_by in self.pagination_options:
            # self.calculate_page_number()
            self.paginate_by = paginate_by
            return int(paginate_by)

    # def calculate_page_number(self):
    #     request = self.request.GET.copy()
    #     paginate_by = int(self.request.GET.get('paginate_by'))
    #     current_page_number = request.get('page')
    #     print(self.paginate_by)
    #     difference = paginate_by / self.paginate_by
    #     print(difference)



class AssignmentInfo(DetailView):
    template_name = 'assignment/assignment_info.html'
    model = Assignment
    context_object_name = 'assignment'
    slug_url_kwarg = 'assignment_uuid'
    slug_field = 'uuid'
    extra_context = {'status_color_labels': Assignment.Status.COLOR_LABELS,
                     'priority_color_labels': Assignment.PRIORITY_COLOR_LABELS}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.subject
        context['comment_form'] = CommentForm(user=self.request.user)
        context['attachments'] = self.object.files.all()
        context['comments'] = self.object.comments.all().select_related('created_by')
        return context

    @staticmethod
    def download(request, assignment_uuid, file_uuid):
        file = get_object_or_404(File, uuid=file_uuid)
        filename = get_filename(file.file)
        response = FileResponse(file.file, 'rb', filename=filename, as_attachment=True)
        return response


class CreateAssignment(View):

    def get(self, request):
        assignment_form = AssignmentForm()
        file_form = FileForm()
        context = {'assignment_form': assignment_form,
                   'file_form': file_form,
                   'title': 'Create assignment'}
        return render(self.request, 'assignment/create_assignment.html', context=context)

    def post(self, request):
        assignment_form = AssignmentForm(self.request.POST)
        file_form = FileForm(self.request.POST, self.request.FILES)
        if assignment_form.is_valid() and file_form.is_valid():
            with transaction.atomic():
                assignment = assignment_form.save(commit=False)
                assignment.created_by = self.request.user
                assignment.save()
                File.objects.bulk_create([
                    File(file=file, assignment=assignment) for file in file_form.files.getlist('file')
                ])
        else:
            context = {'assignment_form': assignment_form,
                       'file_form': file_form,
                       'title': 'Create assignment'}
            return render(self.request, 'assignment/create_assignment.html', context=context)
        return redirect('assignment_list')


class UpdateAssignment(View):

    def get(self, request, assignment_uuid):
        assignment = Assignment.objects.get(uuid=assignment_uuid)
        if assignment.deadline:
            assignment.deadline = localtime(assignment.deadline).strftime('%Y-%m-%dT%H:%M')
        assignment_form = AssignmentForm(instance=assignment)
        file_form = FileForm()
        context = {'assignment_form': assignment_form,
                   'file_form': file_form,
                   'attachments': assignment.files.all(),
                   'title': assignment.subject}
        return render(self.request, 'assignment/create_assignment.html', context=context)

    def post(self, request, assignment_uuid):
        assignment = Assignment.objects.get(uuid=assignment_uuid)
        assignment_form = AssignmentForm(self.request.POST, instance=assignment)
        file_form = FileForm(self.request.POST, self.request.FILES)
        if assignment_form.is_valid() and file_form.is_valid():
            with transaction.atomic():
                assignment.save(update_fields=assignment_form.changed_data)
                File.objects.bulk_create([
                    File(file=file, assignment=assignment) for file in file_form.files.getlist('file')
                ])
                files_to_delete = self.request.POST.get('files-to-delete', default='').split()
                assignment.remove_files(files_to_delete)
        else:
            context = {'assignment_form': assignment_form,
                       'file_form': file_form,
                       'title': assignment.subject}
            return render(self.request, 'assignment/create_assignment.html', context=context)
        return redirect('assignment_info', assignment_uuid=assignment.uuid)


class DeleteAssignment(DeleteView):
    model = Assignment
    success_url = reverse_lazy('assignment_list')

    def get_object(self, queryset=None):
        assignment_uuid = self.kwargs.get('assignment_uuid')
        return get_object_or_404(Assignment, uuid=assignment_uuid)
