from django.shortcuts import render, HttpResponse, redirect
from .models import Data
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    datas = Data.objects.filter().values()
    tags = Data.objects.filter().values('tags')
    title_tags = Data.objects.filter().values('title_tags')

    paginator = Paginator(datas, 15)  # Show 15 posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 把 tag 轉成 distinct
    tags_list = tags_distinct(tags)
    title_tags_list = tags_distinct(title_tags)

    return render(request, 'app/index.html', {'tags': tags_list, 'title_tags': title_tags_list, 'page_obj': page_obj})


def data(request, slug):
    # return HttpResponse()
    return HttpResponse(Data.objects.filter(slug__contains = slug).values())


def post(request, slug):
    if request.method == 'POST':
        # return HttpResponse('hi')
        store_tag_taggers_tags_average(request, slug, 'tags')
        return redirect('/post/' + slug)

    if request.method == 'GET':
        data = Data.objects.filter(slug__contains = slug).values()[0]
        tags = Data.objects.filter().values('tags')
        title_tags = Data.objects.filter().values('title_tags')

        # 把 tag 轉成 distinct
        tags_list = tags_distinct(tags)
        title_tags_list = tags_distinct(title_tags)

        return render(request, 'app/post.html',
                      {'data': data, 'tags': tags_list, 'title_tags': title_tags_list, 'slug': slug})


def post_title(request, slug):
    if request.method == 'POST':
        store_tag_taggers_tags_average(request, slug, 'title_tags')
        return redirect('/post/' + slug)


def delete_img(request, slug, img):
    imgs = Data.objects.filter(slug__contains = slug).values('imgs')[0]['imgs']
    img = imgs.pop(int(img))
    Data.objects.filter(slug__contains = slug).update(imgs = imgs)
    return redirect('/post/' + slug)


def delete_tag(request, slug, tag):
    tags = Data.objects.filter(slug__contains = slug).values('tags')[0]['tags']
    tag = tags.pop(int(tag))
    tags_average = tags_averaging(tags, True)

    Data.objects.filter(slug__contains = slug).update(tags = tags)
    Data.objects.filter(slug__contains = slug).update(tags_average = tags_average)
    return redirect('/post/' + slug)


def delete_title_tag(request, slug, tag):
    title_tags = Data.objects.filter(slug__contains = slug).values('title_tags')[0]['title_tags']
    title_tag = title_tags.pop(int(tag))
    tags_average = tags_averaging(title_tags, False)

    Data.objects.filter(slug__contains = slug).update(title_tags = title_tags)
    Data.objects.filter(slug__contains = slug).update(title_tags_average = tags_average)
    return redirect('/post/' + slug)


# 取標籤平均分數 ( 標籤數量 / 標籤總數 )
# attention = True 就是以標籤數量加上關注度標籤，
# 當標籤數量小於等於 10 的時候加上 「低關注」標籤
def tags_averaging(tags, attention):
    if attention:
        if len(tags) <= 10:
            tags_average = {tag: tags.count(tag) / 10 for tag in tags}
            tags_average['低關注'] = (10 - len(tags)) / 10
            return tags_average
        else:
            return {tag: tags.count(tag) / len(tags) for tag in tags}
    else:
        return {tag: tags.count(tag) / len(tags) for tag in tags}


# 把 tag 轉成 distinct
def tags_distinct(tags):
    # [{'tags': None}, {'tags': ['可愛', '巨乳', '巨乳', '短髮', '可愛']},{'tags': None}...]
    # [{'title_tags': None}, {'title_tags': ['可愛', '巨乳', '巨乳', '短髮', '可愛']},{'title_tags': None}...]
    tags_list = []
    if tags is not None:
        for tag_dict in tags:
            dict_value = list(tag_dict.values())
            if dict_value[0]:
                # print(dict_value)
                tags_list.extend(dict_value[0])
    return sorted(list(set(tags_list)), key = len)


def store_tag_taggers_tags_average(request, slug, judge):
    tags = request.POST.get('tags', '').strip().split(' ')
    taggers = request.POST.get('taggers', '')
    ppt_post = Data.objects.get(slug__contains = slug)

    # 若沒有人標過這則 po 文，要先把標注者轉成空陣列
    if not ppt_post.taggers:
        ppt_post.taggers = []
    ppt_post.taggers.append(taggers)

    Data.objects.filter(slug__contains = slug).update(taggers = list(set(ppt_post.taggers)))

    if judge == 'tags':

        # 若沒有人給過這則 po 文圖片標籤，要先把圖片標籤轉成空陣列
        if not ppt_post.tags:
            ppt_post.tags = []
        for tag in tags:
            ppt_post.tags.append(tag)

        # 取標籤平均分數 ( 標籤數量 / 標籤總數 )
        # 當標籤數量小於等於 10 的時候加上 「低關注」標籤
        print(ppt_post.tags)
        tags_average = tags_averaging(ppt_post.tags, True)

        Data.objects.filter(slug__contains = slug).update(tags = ppt_post.tags)
        Data.objects.filter(slug__contains = slug).update(tags_average = tags_average)

    if judge == 'title_tags':

        # 若沒有人給過這則 po 文標題標籤，要先把標題標籤轉成空陣列
        if not ppt_post.title_tags:
            ppt_post.title_tags = []
        for tag in tags:
            ppt_post.title_tags.append(tag)

        # 取標籤平均分數 ( 標籤數量 / 標籤總數 )
        # 當標籤數量小於等於 10 的時候加上 「低關注」標籤
        tags_average = tags_averaging(ppt_post.title_tags, False)

        Data.objects.filter(slug__contains = slug).update(title_tags = ppt_post.title_tags)
        Data.objects.filter(slug__contains = slug).update(title_tags_average = tags_average)
