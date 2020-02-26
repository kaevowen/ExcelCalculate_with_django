from django.shortcuts import render, redirect
from django.http import HttpResponse
import pandas as pd

# Create your views here.
def calculate(req):
    file = req.FILES['fileInput']
    print("사용자가 등록한 파일의 이름 : ", file)
    df = pd.read_excel(file, sheet_name='Sheet1', header=0)
    #print(df.head(5))
    grade_dic = {}
    total_row_num = len(df.index)

    for i in range(total_row_num):
        data = df.loc[i]
        if not data['grade'] in grade_dic.keys():
            grade_dic[data['grade']] = [data['value']]
        else:
            grade_dic[data['grade']].append(data['value'])

    grade_calc_dic = {}
    for key in grade_dic.keys():
        grade_calc_dic[key] = {}
        grade_calc_dic[key]['min'] = min(grade_dic[key])
        grade_calc_dic[key]['max'] = max(grade_dic[key])
        grade_calc_dic[key]['avg'] = float(sum(grade_dic[key])) / len(grade_dic[key])

    grade_list = list(grade_calc_dic.keys())
    grade_list.sort()

    for key in grade_list:
        print("# grade: ", key)
        print("min:", grade_calc_dic[key]['min'], end='')
        print("/ max:", grade_calc_dic[key]['max'], end='')
        print("/ avg:", grade_calc_dic[key]['avg'], end='\n\n')

    email_domain_dic = {}
    for i in range(total_row_num):
        data = df.loc[i]
        email_domamin = (data['email'].split("@"))[1]
        if not email_domamin in email_domain_dic.keys():
            email_domain_dic[email_domamin] = 1
        else:
            email_domain_dic[email_domamin] += 1
    print("## EMAIL 도메인별 사용 인원")
    for key in email_domain_dic.keys():
        print("#", key, ": ", email_domain_dic[key],"명")

    grade_calc_dic_to_session = {}
    for key in grade_list:
        grade_calc_dic_to_session[int(key)] = {}
        grade_calc_dic_to_session[int(key)]['max'] = \
            float(grade_calc_dic[key]['max'])

        grade_calc_dic_to_session[int(key)]['avg'] = \
            float(grade_calc_dic[key]['avg'])

        grade_calc_dic_to_session[int(key)]['min'] = \
            float(grade_calc_dic[key]['min'])

    req.session['grade_calc_dic'] = grade_calc_dic_to_session
    req.session['email_domain_dic'] = email_domain_dic
    return redirect("/result")