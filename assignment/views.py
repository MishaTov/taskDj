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
    extra_context = {'title': 'Assignments',
                     'status_color_labels': Assignment.Status.COLOR_LABELS,
                     'priority_color_labels': Assignment.PRIORITY_COLOR_LABELS}

    def get(self, request: HttpRequest, *args, **kwargs):
        request.GET = request.GET.copy()
        if not request.GET.get('page'):
            request.GET['page'] = 1
        paginate_by = request.GET.get('paginate_by', self.paginate_by)
        if paginate_by != str(self.paginate_by) and paginate_by in {'5', '10', '20', '50'}:
            self.paginate_by = int(paginate_by)
        request.GET['paginate_by'] = self.paginate_by
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if not context.get('paginate_by'):
            context['paginate_by'] = self.paginate_by
        paginator = context.get('paginator')
        number = context.get('page_obj').number
        context['pages'] = paginator.get_elided_page_range(number=number, on_each_side=1, on_ends=1)
        filters = ''
        for param, value in self.request.GET.items():
            if param != 'page':
                filters += f'&{param}={value}'
        context['filters'] = filters
        return context


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
        context['title'] = context['assignment'].subject
        context['comment_form'] = CommentForm(user=self.request.user)
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
                   'attachments': assignment.file_set.all(),
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
