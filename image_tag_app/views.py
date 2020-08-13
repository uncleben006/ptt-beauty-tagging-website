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
    # return HttpResponse()
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

        # 取標籤平均分數 ( 標籤數量 / 標籤總數 )
        # 當標籤數量小於等於 10 的時候加上 「低關注」標籤
        tags_average = tags_averaging(ppt_post.tags)

        Data.objects.filter(slug__contains = slug).update(taggers = list(set(ppt_post.taggers)))
        Data.objects.filter(slug__contains = slug).update(tags = ppt_post.tags)
        Data.objects.filter(slug__contains = slug).update(tags_average = tags_average)
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
    tags_average = tags_averaging(tags)

    Data.objects.filter(slug__contains = slug).update(tags = tags)
    Data.objects.filter(slug__contains = slug).update(tags_average = tags_average)
    return redirect('/post/' + slug)


def tags_averaging(tags):
    if len(tags) <= 10:
        tags_average = {tag: tags.count(tag) / 10 for tag in tags}
        tags_average['低關注'] = (10 - len(tags)) / 10
        return tags_average
    else:
        return {tag: tags.count(tag) / len(tags) for tag in tags}
