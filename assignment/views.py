from django.db import transaction
from django.http import HttpRequest, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.timezone import localtime
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView

from template_tags.templatetags.custom_tags import get_filename
from .forms import AssignmentForm, FileForm, CommentForm
from .models import File, Assignment


def main_page(request):
    return render(request, 'base.html')


class AssignmentView(ListView):
    template_name = 'assignment/assignment_list.html'
    model = Assignment
    context_object_name = 'assignments'
    paginate_by = 5
    ordering = 'created_at'
    extra_context = {'title': 'Assignments',
                     'status_color_labels': Assignment.Status.COLOR_LABELS,
                     'priority_color_labels': Assignment.PRIORITY_COLOR_LABELS}

    def __init__(self):
        super().__init__()
        self.allowed_pagination_options = {'5': 5,
                                           '10': 10,
                                           '20': 20,
                                           '50': 50}
        self.allowed_ordering_options = {'created_at': 'Creation date',
                                         'deadline': 'Deadline',
                                         'priority': 'Priority'}

    def get(self, request: HttpRequest, *args, **kwargs):
        request.GET = request.GET.copy()
        if not request.GET.get('page'):
            request.GET['page'] = 1
        paginate_by = request.GET.get('paginate_by', self.paginate_by)
        order_by = request.GET.get('order_by', self.ordering)
        if paginate_by != self.paginate_by and paginate_by in self.allowed_pagination_options:
            self.paginate_by = int(paginate_by)
        if order_by != self.ordering and order_by in self.allowed_ordering_options:
            self.ordering = order_by
        request.GET['paginate_by'] = self.paginate_by
        request.GET['order_by'] = self.ordering
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        object_list = self.model.get_filtrated_queryset(self.request.GET)
        context = super().get_context_data(object_list=object_list, **kwargs)
        if not context.get('paginate_by'):
            context['paginate_by'] = self.paginate_by
        if not context.get('order_by'):
            context['order_by'] = self.allowed_ordering_options[self.ordering]
        paginator = context.get('paginator')
        number = context.get('page_obj').number
        context['pages'] = paginator.get_elided_page_range(number=number, on_each_side=1, on_ends=1)
        context['paginate_options'] = self.allowed_pagination_options
        context['order_options'] = self.allowed_ordering_options
        context['reverse'] = True if self.request.GET.get('reverse') else False
        url_params = ''
        for param, value in self.request.GET.items():
            if param != 'page':
                url_params += f'&{param}={value}'
        context['url_params'] = url_params
        return context


class AssignmentInfo(DetailView):
    template_name = 'assignment/assignment_info.html'
    model = Assignment
    context_object_name = 'assignment'
    slug_url_kwarg = 'assignment_uuid'
    slug_field = 'uuid'
    extra_context = {'status_color_labels': Assignment.Status.COLOR_LABELS,
                     'priority_color_labels': Assignment.PRIORITY_COLOR_LABELS}

    def get_queryset(self):
        return super().get_queryset().select_related('created_by')

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
        return render(request, 'assignment/create_assignment.html', context=context)

    def post(self, request: HttpRequest):
        assignment_form = AssignmentForm(request.POST)
        file_form = FileForm(request.POST, request.FILES)
        if assignment_form.is_valid() and file_form.is_valid():
            with transaction.atomic():
                assignment = assignment_form.save(commit=False)
                assignment.created_by = request.user
                assignment.save()
                File.objects.bulk_create([
                    File(file=file, assignment=assignment) for file in file_form.files.getlist('file')
                ])
        else:
            context = {'assignment_form': assignment_form,
                       'file_form': file_form,
                       'title': 'Create assignment'}
            return render(request, 'assignment/create_assignment.html', context=context)
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
        return render(request, 'assignment/create_assignment.html', context=context)

    def post(self, request: HttpRequest, assignment_uuid):
        assignment = Assignment.objects.get(uuid=assignment_uuid)
        assignment_form = AssignmentForm(request.POST, instance=assignment)
        file_form = FileForm(request.POST, request.FILES)
        if assignment_form.is_valid() and file_form.is_valid():
            with transaction.atomic():
                assignment.save(update_fields=assignment_form.changed_data)
                File.objects.bulk_create([
                    File(file=file, assignment=assignment) for file in file_form.files.getlist('file')
                ])
                files_to_delete = request.POST.get('files-to-delete', default='').split()
                assignment.remove_files(files_to_delete)
        else:
            context = {'assignment_form': assignment_form,
                       'file_form': file_form,
                       'title': assignment.subject}
            return render(request, 'assignment/create_assignment.html', context=context)
        return redirect('assignment_info', assignment_uuid=assignment.uuid)


class DeleteAssignment(DeleteView):
    model = Assignment
    success_url = reverse_lazy('assignment_list')

    def get_object(self, queryset=None):
        assignment_uuid = self.kwargs.get('assignment_uuid')
        return get_object_or_404(Assignment, uuid=assignment_uuid)
