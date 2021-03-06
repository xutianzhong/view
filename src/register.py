# -*- coding: utf-8 -*-
import traceback
import os
import hashlib
from flask import Flask,jsonify, request, make_response
from flask_restful import Resource, Api
from flask_restful import reqparse
import pymysql
import pymysql.cursors
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


################
#照片存储路径配置
################
#图片存储的根目录
basedir = os.path.abspath(os.path.dirname(__file__))
#用户上传原始图片存储的目录名称
photo_directory = 'original_photo'
#生成的大头贴存储的目录名称
photo_sticker_directory = 'photo_sticker'

##########
#数据库配置
##########
#数据库ip地址和端口
DBHOST = '127.0.0.1'
DBPORT = 3306
#数据库登录用户名
DBUSER = 'root'
#数据库登录密码
DBPASSWORD = 'toor'   #'Toortoor'
#使用的数据库库名
DBDATABASE = 'register'


#############
#Flask 配置
#############
#Flask 使用ip地址和端口
FLASK_HOST = '127.0.0.1'
FLASK_PORT = '5000'
DEBUG = True


app = Flask(__name__)
api = Api(app)


def get_db_connection():
    try:
        connection = pymysql.connect(host=DBHOST,
                                     user=DBUSER,
                                     password=DBPASSWORD,
                                     port=DBPORT,
                                     db=DBDATABASE,
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)
    except:
        print traceback.format_exc()
        connection = False
    return connection


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,session_id')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,HEAD')
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


def query_sql(sql):
    result = []
    try:
        connection = get_db_connection()
        if connection != None:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                r = cursor.fetchall()
            result = r
    except:
        error = traceback.format_exc()
        print(error)
        return False,error
    return True,result


def write_sql(sql):
    result = []
    try:
        connection = get_db_connection()
        if connection != None:
            with connection.cursor() as cursor:
                cursor.execute(sql)
            connection.commit()
    except:
        error = traceback.format_exc()
        print(error)
        return False,error
    return True,result


def generate_md5(fstream):
    md5_init = hashlib.md5()
    md5_init.update(fstream)
    md5 = md5_init.hexdigest()
    return md5


parser = reqparse.RequestParser()
parser.add_argument('company')
parser.add_argument('department')
parser.add_argument('user')
parser.add_argument('mail')
parser.add_argument('comment')
parser.add_argument('pid')
parser.add_argument('company')
parser.add_argument('department')
parser.add_argument('type')


class StatisticByType(Resource):
    def get(self):
        args = parser.parse_args()
        statistic_type = request.args.get('type')
        # company = request.args.get('company')
        # department = request.args.get('department')
        if statistic_type not in ['company','department']:
            return {'state':'Success','info':'Success','result':{'type':'','values':[]}}
        elif statistic_type == 'company':
            sql = 'select company,count(company) as amount from register_user group by company'
            sql_state, sql_result = query_sql(sql)
            if sql_state == False:
                return {'state':'Fail' ,'info':sql_result,'result':''}
            else:
                try:
                    result = {'state':'Success','info':'Success','result':{'type':'company','values':[]}}
                    for c in sql_result:
                        result['result']['values'].append({'name':c['company'],'amount':c['amount']})
                    return result
                except:
                    print traceback.format_exc()
                    return {'state':'Fail' ,'info':traceback.format_exc(),'result':''}
        elif statistic_type == 'department':
            company = request.args.get('company')
            if company:
                sql = 'select department,count(department) as amount from register_user where company = "%s" group by department'%company
                sql_state, sql_result = query_sql(sql)
                if sql_state == False:
                    return {'state': 'Fail', 'info': sql_result, 'result': ''}
                else:
                    try:
                        result = {'state': 'Success', 'info': 'Success', 'result': {'type': 'department', 'values': []}}
                        for c in sql_result:
                            result['result']['values'].append({'name': c['department'], 'amount': c['amount']})
                        return result
                    except:
                        print traceback.format_exc()
                        return {'state': 'Fail', 'info': traceback.format_exc(), 'result': ''}
            else:
                result = {'state': 'Success', 'info': 'Success', 'result': {'type': 'department', 'values': []}}
                return result


class GetUsers(Resource):
    def get(self):
        args = parser.parse_args()
        company = request.args.get('company')
        if company:
            sql = 'select user_name,company,insert_time from register_user where company="%s" order by insert_time desc limit 10'%company
        else:
            sql = 'select user_name,company,insert_time from register_user order by insert_time desc limit 10'
        sql_state, sql_result = query_sql(sql)
        if sql_state == False:
            return {'state':'Fail' ,'info':sql_result,'result':''}
        else:
            try:
                result = {'state': 'Success', 'info': 'Success', 'Users': []}
                for c in sql_result:
                    result['Users'].append({'user_name':c['user_name'], 'company_name':c['company'], 'time':c['insert_time'].strftime("%Y-%m-%d %H:%S:%M")})
                return result
            except:
                print traceback.format_exc()
                return {'state':'Fail' ,'info':traceback.format_exc(),'result':''}


class SearchByType(Resource):
    def get(self):
        args = parser.parse_args()
        company = request.args.get('company')
        department = request.args.get('department')
        try:
            result = {'state': 'Success', 'info': 'Success', 'result': {'company':[],'department':[]}}
            if (company == '*' and not department) or not (company or department):
                # return all company name
                sql = 'select company from company_department group by company'
                sql_state, sql_result = query_sql(sql)
                if sql_state == False:
                    return {'state': 'Fail', 'info': sql_result, 'result': ''}
                else:
                    try:
                        for c in sql_result:
                            result['result']['company'].append(c['company'])
                        return result
                    except:
                        print traceback.format_exc()
                        return {'state': 'Fail', 'info': traceback.format_exc(), 'result': ''}
            elif (company != '*' and company) and not department:
                # return matched company
                sql = 'select company from company_department group by company'
                sql_state, sql_result = query_sql(sql)
                if sql_state == False:
                    return {'state': 'Fail', 'info': sql_result, 'result': ''}
                else:
                    try:
                        matched_company = []
                        for c in sql_result:
                            if company in c['company']:
                                matched_company.append(c['company'])
                        result['result']['company'] = matched_company
                        return result
                    except:
                        print traceback.format_exc()
                        return {'state': 'Fail', 'info': traceback.format_exc(), 'result': ''}
            else:
                if company and department:
                    # return department belong to company
                    sql = 'select department from company_department where company = "%s"'%company
                    sql_state, sql_result = query_sql(sql)
                    if sql_state == False:
                        return {'state': 'Fail', 'info': sql_result, 'result': ''}
                    else:
                        try:
                            matched_department = []
                            for c in sql_result:
                                if department in c['department']:
                                    matched_department.append(c['department'])
                            result['result']['department'] = matched_department
                            return result
                        except:
                            print traceback.format_exc()
                            return {'state': 'Fail', 'info': traceback.format_exc(), 'result': ''}
                else:
                    return {'state': 'Success', 'info': 'Success', 'result': {'company': [], 'department': []}}
        except:
            print traceback.format_exc()
            return {'state': 'Fail', 'info': traceback.format_exc(), 'result': ''}


class RegisterInfo(Resource):
    def post(self):
        try:
            args = parser.parse_args()
            sql = 'insert into register_user (user_name,company,department,mail,pid,comments) values ("%s","%s","%s","%s",%s,"%s")'
            sql_state, sql_result = query_sql(sql%(args['company'],args['department'],args['user'],args['mail'],args['pid'],args['comment']))
            if sql_state == True:
                return {'state': 'Success', 'info': 'Success', 'result': {'verify': '1', 'msg': 'Success', 'pid':args['pid']}}
            else:
                if '1062' in sql_result and 'Duplicate entry' in sql_result :
                    return {'state': 'Success', 'info': 'Success','result': {'verify': '2', 'msg': 'Duplicate Registration information !', 'pid': args['pid']}}
                else:
                    return {'state': 'Success', 'info': 'Success', 'result': {'verify': '0', 'msg': sql_result, 'pid':''}}
        except:
            print traceback.format_exc()
            return {'state': 'Fail', 'info': traceback.format_exc(), 'result': ''}


ALLOWED_EXTENSIONS = set(['jpg', 'JPG'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/register/photo_sticker', methods=['GET'])
def GetPhoto():
    pid =request.args.get('pid')
    file_dir = os.path.join(basedir, photo_sticker_directory)
    if not os.path.isdir(file_dir):
        return jsonify({'state': 'Fail', 'info': 'Can not find photo directory !', 'result': ''})
    if pid:
        for file_suffix in ALLOWED_EXTENSIONS:
            file_path = os.path.join(file_dir,str(pid)+'.'+file_suffix)
            if os.path.isfile(file_path):
                image_data = open(file_path, "rb").read()
                response = make_response(image_data)
                response.headers['Content-Type'] = 'image/%s'%file_suffix
                return response
            else:
                return jsonify({'state': 'Fail', 'info': 'Can not find photo !', 'result': ''})


def face_verify(photo_path):
    return True


def generate_photo_sticker(photo_path):
    return photo_path


@app.route('/register/verify_photo', methods=['POST'])
def VerifyPhoto():
    file_dir = os.path.join(basedir, photo_directory)
    photo_sticker_dir = os.path.join(basedir, photo_sticker_directory)
    if not os.path.isdir(file_dir):
        try:
            os.mkdir(file_dir)
        except:
            print traceback.format_exc()
            return jsonify({'state': 'Fail', 'info': traceback.format_exc(), 'result': ''})
    if not os.path.isdir(photo_sticker_dir):
        try:
            os.mkdir(photo_sticker_dir)
        except:
            print traceback.format_exc()
            return jsonify({'state': 'Fail', 'info': traceback.format_exc(), 'result': ''})
    f = request.files['photo']
    if f and allowed_file(f.filename):
        file_stream = f.read()
        pid = generate_md5(file_stream)
        file_path = os.path.join(file_dir, str(pid) + '.' + f.filename.split('.')[-1])
        if not os.path.isfile(file_path):
            fopen = open(file_path, 'wb')
            fopen.write(file_stream)
            fopen.close()
        verify_result = face_verify(file_path)
        if verify_result == True:
            photo_sticker_path = generate_photo_sticker(file_path)
            # photo_sticker_path = 'F:/workplace/PycharmProjects/alarmapp/photo_sotre/screenshot-11.11.110.1-48081-2018.12.28-16-21-48.png'
            p = open(photo_sticker_path,'rb')
            pstream = p.read()
            new_pid = generate_md5(pstream)
            new_ps_path = os.path.join(photo_sticker_dir,str(new_pid)+'.'+photo_sticker_path.split('.')[-1])
            if os.path.isfile(new_ps_path):
                return jsonify({'state': 'Success', 'info': 'Success','result': {'verify': '3', 'msg': 'Photo is already used !', 'pid': new_pid}})
            new_psopen =open(new_ps_path,'wb')
            new_psopen.write(pstream)
            new_psopen.close()
            p.close()
            return jsonify({'state': 'Success', 'info': 'Success', 'result': {'verify': '1', 'msg': 'Success', 'pid': new_pid}})
        else:
            return jsonify({'state': 'Success', 'info': 'Success', 'result': {'verify': '0', 'msg': 'Can not find human face !', 'pid': ''}})
    else:
        return jsonify({'state': 'Success', 'info': 'Success', 'result': {'verify': '2', 'msg': 'Photo format is not support !', 'pid': ''}})


api.add_resource(StatisticByType, '/screen_display/statistic')
api.add_resource(GetUsers, '/screen_display/get_users')
api.add_resource(SearchByType, '/register/search')
api.add_resource(RegisterInfo, '/register/register')



if __name__ == '__main__':
    app.run(debug=DEBUG,host=FLASK_HOST,port=FLASK_PORT)