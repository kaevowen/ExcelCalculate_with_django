from django.shortcuts import render, redirect, HttpResponse
from .models import *
from sendEmail.views import *

import random
import hashlib


def index(req):
    if 'user_name' in req.session.keys():
        return render(req, 'main/index.html')
    else:
        return redirect('main_signin')


def signup(req):
    return render(req, 'main/signup.html')


def join(req):
    name = req.POST['signupName']
    email = req.POST['signupEmail']
    pw = req.POST['signupPW']
    encoded_pw = pw.encode()
    encrypted_pw = hashlib.sha256(encoded_pw).hexdigest()
    user = User(user_name=name, user_email=email, user_pw=encrypted_pw)
    user.save()
    code = random.randint(1000, 9999)
    response = redirect('main_verifyCode')
    response.set_cookie('code', code)
    response.set_cookie('user_id', user.id)

    send_result = send(email, code)
    print(send_result)
    if send_result:
        return response
    else:
        content = {'message': '이메일 발송에 실패했습니다.'}
        return render(req, 'main/error.html', content)


def signin(req):
    return render(req, 'main/signin.html')


def login(req):
    loginEmail = req.POST['loginEmail']
    loginPW = req.POST['loginPW']
    try:
        user = User.objects.get(user_email=loginEmail)
    except:
        content = {'message': '아이디 또는 비밀번호가 틀립니다.'}
        return render(req, 'main/error.html', content)

    encoded_loginPW = loginPW.encode()
    encrypted_loginPW = hashlib.sha256(encoded_loginPW).hexdigest()
    if user.user_pw == encrypted_loginPW:
        req.session['user_name'] = user.user_name
        req.session['user_email'] = user.user_email
        return redirect('main_index')
    else:
        content = {'message': '아이디 또는 비밀번호가 틀립니다.'}
        return render(req, 'main/error.html', content)



def loginFail(req):
    return render(req, 'main/loginFail.html')


def verifyCode(req):
    return render(req, 'main/verifyCode')


def verify(req):
    user_code = req.POST['verifyCode']
    cookie_code = req.COOKIES.get('code')
    if user_code == cookie_code:
        user = User.objects.get(id=req.COOKIES.get('user_id'))
        user.user_validate = 1
        user.save()
        response = redirect('main_index')
        response.delete_cookie('code')
        response.delete_cookie('user_id')
        req.session['user_name'] = user.user_name
        req.session['user_email'] = user.user_email
        return response
    else:
        return redirect('main_verifyCode')


def result(req):
    if 'user_name' in req.session.keys():
        content = {}
        content['grade_calculate_dic'] = req.session['grade_domain_dic']
        content['grade_domain_dic'] = req.session['email_domain_dic']
        del req.session['grade_calculate_dic']
        del req.session['email_domain_dic']
        return render(req, 'main/result.html', content)
    else:
        return redirect('main_signin')


def logout(req):
    del req.session['user_name']
    del req.session['user_email']
    return redirect('main_signin')
