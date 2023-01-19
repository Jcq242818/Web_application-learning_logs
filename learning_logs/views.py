from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic,Entry
from .forms import TopicForm,EntryForm

#只有主页和注册页面不需要用login_required装饰器进行保护，其他的页面都需要用改装饰器进行保护，以防止未登录就可以访问这些页面的情况
def index(request):
    """学习笔记的主页"""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """显示所有的主题"""
    topics = Topic.objects.order_by("date_added")
    # 只允许用户访问自己的主题
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request,topic_id):
    """显示单个主题及其所有条目"""
    topic = Topic.objects.get(id=topic_id)
    # 进行检查:确定请求的主题属于当前用户
    if topic.owner != request.user:
        # 如果不是当前主题的用户在访问，立刻挂出404请求的资源不存在，拒绝用户访问
        raise Http404
    entries = topic.entry_set.order_by("-date_added")
    context = {"topic":topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """用户添加一个新主题"""
    if request.method != 'POST':
        """未提交数据，创建一个新表单"""
        form = TopicForm()
    else:
        # Post提交的数据:对用户提交的数据进行处理
        form = TopicForm(data=request.POST)
        if form.is_valid():
            # 将新主题关联到当前request的用户
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save() # 将表单中的数据写入数据库
            return redirect('learning_logs:topics')


    # 显示空表单或指出表单数据无效
    context = {'form':form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request,topic_id):
    """在特定主题中添加新条目"""
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        # 如果不是当前主题的用户在访问，立刻挂出404请求的资源不存在，拒绝用户访问
        raise Http404
    if request.method != 'POST':
        """未提交数据，创建一个新的空表单"""
        form = EntryForm()
    else:
        # Post提交的数据:对用户提交的数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False) # 这里先不把数据保存到数据库里面，得先和前面的主题关联起来在保存
            new_entry.topic = topic
            new_entry.save() # 关联完主题后将表单数据保存到数据库中
            return redirect('learning_logs:topic', topic_id=topic_id)

    # 显示空表单或指出表单数据无效
    context = {'topic':topic, 'form':form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """编辑既有条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        # 如果不是当前主题的用户在访问，立刻挂出404请求的资源不存在，拒绝用户访问
        raise Http404
    if request.method != 'POST':
        # 初次请求：使用当前的条目填充表单
        form = EntryForm(instance=entry)
    else:
        # Post提交的数据:对数据进行处理
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
