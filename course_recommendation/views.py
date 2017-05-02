from django.shortcuts import render, get_object_or_404
from.models import jobs,courses,services
from django.http import JsonResponse
# from rest_framework import viewsets
import re
import logging, logging.config
import sys

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    }
}

logging.config.dictConfig(LOGGING)


def index(request):
    # all_j=jobs.objects.all()
    # return render(request,'courses/jobs.html',{'all_jobs': all_j})
    return render(request, 'uni_friend-frontend/index.html')

def job(request):
    all_j = jobs.objects.all()
    return render(request, 'uni_friend-frontend/courserec.html',{'all_jobs': all_j})

def test(request,job_id):
    # id=request.GET.get('id',None)
    data={

        'id':1
    }
    return JsonResponse(data)

def recommend(request,job_id,prog=None):
    rec_courses = []
    recommend_courses=[]
    dict={}
    jobfull = get_object_or_404(jobs,pk=job_id)
    jobdesc = jobfull.description.lower()
    job_list = re.split("[^a-zA-Z0-9]", jobdesc)
    keywrods={'CMPE 226':['mysql','php','xml'], 'CMPE 225':['java','python'], 'CMPE 207': ['tcp', 'ip', 'ssl'], 'CMPE 280':['html','css','css3','jquery']}
    a_list=keywrods.keys()
    for i in job_list:
        for course_num in a_list:
            if(i in keywrods.get(course_num)):
                rec_courses.append(course_num)
    fil_courses = set(rec_courses)
    for k in fil_courses:
        count = rec_courses.count(k)
        dict[k] = count


    if prog is None:
        for l in range(len(dict)):
            # if (dict.values()[l]) >= 2:
            recommend_courses.append(courses.objects.filter(number=dict.keys()[l]))
    else:
        for l in range(len(dict)):
        # if (dict.values()[l]) >= 2:
            recommend_courses.append(courses.objects.filter(number=dict.keys()[l],program=prog ))



    # return JsonResponse(data)

    return render(request, 'uni_friend-frontend/modelPopUp.html',{'jobs': jobfull, 'filter_courses': recommend_courses})


