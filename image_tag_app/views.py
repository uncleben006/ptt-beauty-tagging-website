from django.shortcuts import render, HttpResponse, redirect
from .models import Data
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    datas = Data.objects.filter().values()
    taggers = Data.objects.filter().values('taggers')
    tags = Data.objects.filter().values('tags')

    paginator = Paginator(datas, 15)  # Show 15 posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 把 tag 轉成 distinct
    tags_list = []
    if tags is not None:
        for tag in tags:
            if tag['tags'] is not None:
                tags_list.extend(tag['tags'])
    tags_list = sorted(list(set(tags_list)), key = len)

    return render(request, 'app/index.html', {'tags': tags_list, 'page_obj': page_obj})


def data(request, slug):
    return HttpResponse(Data.objects.filter(slug__contains = slug).values())

def post(request, slug):
    if request.method == 'POST':

        tags = request.POST.get('tags', '').strip().split(' ')
        taggers = request.POST.get('taggers', '')
        ppt_post = Data.objects.get(slug__contains = slug)

        # 若沒有人標過，把標注者轉成空陣列
        if not ppt_post.taggers:
            ppt_post.taggers = []
        ppt_post.taggers.append(taggers)

        # 若沒有人給過標籤，把標籤轉成空陣列
        if not ppt_post.tags:
            ppt_post.tags = []
        for tag in tags:
            ppt_post.tags.append(tag)

        Data.objects.filter(slug__contains = slug).update(taggers = list(set(ppt_post.taggers)))
        Data.objects.filter(slug__contains = slug).update(tags = ppt_post.tags)
        return redirect('/post/' + slug)

    if request.method == 'GET':
        data = Data.objects.filter(slug__contains = slug).values()[0]
        tags = Data.objects.filter().values('tags')

        # 把 tag 轉成 distinct
        tags_list = []
        if tags is not None:
            for tag in tags:
                if tag['tags'] is not None:
                    tags_list.extend(tag['tags'])
        tags_list = sorted(list(set(tags_list)), key = len)

        return render(request, 'app/post.html', {'data': data, 'tags': tags_list, 'slug': slug})


def delete_img(request, slug, img):
    imgs = Data.objects.filter(slug__contains = slug).values('imgs')[0]['imgs']
    img = imgs.pop(int(img))
    Data.objects.filter(slug__contains = slug).update(imgs = imgs)
    return redirect('/post/' + slug)


def delete_tag(request, slug, tag):
    tags = Data.objects.filter(slug__contains = slug).values('tags')[0]['tags']
    tag = tags.pop(int(tag))
    Data.objects.filter(slug__contains = slug).update(tags = tags)
    return redirect('/post/' + slug)
