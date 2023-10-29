from time import timezone

from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from .models import Post
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm


class PostsList(ListView):
    model = Post
    template_name = 'news/posts.html'
    context_object_name = 'posts'
    ordering = ['-dateCreation']
    form_class = PostForm
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = timezone.localtime(timezone.now())  # добавим переменную текущей даты time_now
        context['posts_count'] = Post.objects.all().count()  # добавим переменную кол-во постов
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса
        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не накосячил, то сохраняем новый товар
            form.save()
        return super().get(request, *args, **kwargs)


class PostSearch(ListView):
    model = Post
    template_name = 'news/postSearch.html'
    context_object_name = 'posts'
    ordering = ['-id']
    form_class = PostForm
    paginate_by = 2

    def get_queryset(self):
        queryset = PostFilter(self.request.GET, super().get_queryset()).qs
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = timezone.localtime(timezone.now())  # добавим переменную текущей даты time_now
        context['posts_count'] = Post.objects.all().count()  # добавим переменную кол-во постов всего
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['form'] = PostForm()
        return context


class PostDetailView(DetailView):
    template_name = 'news/post_detail.html'
    queryset = Post.objects.all()


class PostCreateView(CreateView):
    template_name = 'news/post_create.html'
    form_class = PostForm


class PostUpdateView(UpdateView):
    template_name = 'news/post_update.html'
    form_class = PostForm

    # метод get_object мы используем вместо queryset,
    # чтобы получить информацию об объекте который
    # мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = 'news/post_delete.html'
    queryset = Post.objects.all()
    success_url = reverse_lazy('news:posts')

