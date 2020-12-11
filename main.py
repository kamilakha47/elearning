from flask import Flask, request, json, jsonify
from sqlalchemy import create_engine
from sqlalchemy.sql import text

app = Flask(__name__)

connects = 'postgresql://postgres:24434@localhost:5432/elearning'
engine = create_engine(connects, echo=False)

## User Management ##
# Register New User For Instructor #
@app.route('/elearning/user/register/instructor', methods=['POST'])
def create_new_user_instructor():
    body_req = request.json
    first_name = body_req.get('first_name')
    last_name = body_req.get('last_name')
    user_name = body_req.get('user_name')
    email = body_req.get('email')
    with engine.connect() as connection:
        qry = text("INSERT INTO public.instructor(first_name, last_name, user_name, email)\
                    VALUE(:first_name, :last_name, :user_name, :email)")
        result = connection.execute(qry,first_name=first_name,
                                        last_name=last_name,
                                        user_name=user_name,
                                        email=email)
        new_qry = text("SELECT * FROM public.instructor WHERE user_name=:user_name")
        new_result = connection.execute(new_qry, user_name=user_name)
        new_user_instructor = []
        for value in new_result:
            new_user_instructor.append(
                {"instructor id":value['instructor_id'],
                 "first name":value['first_name'],
                 "last name":value['last_name'],
                 "username":value['user_name'],
                 "email":value['email']})
        return jsonify(new_user_instructor)

# Register New User For Student #
@app.route('/elearning/user/register/student', methods=['POST'])
def create_new_user_student():
    body_req = request.json
    first_name = body_req.get('first_name')
    last_name = body_req.get('last_name')
    user_name = body_req.get('user_name')
    email = body_req.get('email')
    with engine.connect() as connection:
        qry = text("INSERT INTO public.student(first_name, last_name, user_name, email)\
                    VALUE(:first_name, :last_name, :user_name, :email)")
        result = connection.execute(qry,first_name=first_name,
                                        last_name=last_name,
                                        user_name=user_name,
                                        email=email)
        new_qry = text("SELECT * FROM public.student WHERE user_name=:user_name")
        new_result = connection.execute(new_qry, user_name=user_name)
        new_user_student =[]
        for value in new_result:
            new_user_student.append(
                {"student id":value['student_id'],
                 "num of courses enrolled":value['num_of_courses_enrolled'],
                 "num of courses completed":value['num_of_courses_completed'],
                 "first name":value['first_name'],
                 "last name":value['last_name'],
                 "username":value['user_name'],
                 "email":value['email']}
                 )
        return jsonify(new_user_student)

# Update User For Instructor#
@app.route('/elearning/user/edit/instructor', methods=['PUT'])
def edit_user_instructor(_id):
    body_req = request.json
    _id = request.args.get()
    first = body_req.get('first_name')
    last = body_req.get('last_name')
    user = body_req.get('user_name')
    email = body_req.get('email')
    with engine.connect() as connection:
        qry = text("UPDATE public.instructor SET frist_name=:first, last_name=:last, user=:user, email=:email\
                    WHERE instructor_id=:_id")
        result = connection.execute(qry,first_name=first,
                                        last_name=last,
                                        user_name=user,
                                        email=email)
        new_qry = text("SELECT * FROM public.instructor WHERE instructor_id=:_id")
        new_result = connection.execute(new_qry, _id=_id)
        update_user_instructor = []
        for value in new_result:
            update_user_instructor.append(
                {"instructor id":value['instructor_id'],
                 "first name":value['first_name'],
                 "last name":value['last_name'],
                 "username":value['user_name'],
                 "email":value['email']}
                 )
        return jsonify(update_user_instructor)

# Update User For Student#
@app.route('/elearning/user/edit/student', methods=['PUT'])
def edit_user_student(_id):
    body_req = request.json
    _id = int(request.args.get('_id'))
    first = body_req.get('first_name')
    last = body_req.get('last_name')
    user = body_req.get('user_name')
    email = body_req.get('email')
    with engine.connect() as connection:
        qry = text("UPDATE public.student SET frist_name=:first, last_name=:last, user=:user, email=:email\
                    WHERE student_id=:_id")
        result = connection.execute(qry,first_name=first,
                                        last_name=last,
                                        user_name=user,
                                        email=email)
        new_qry = text("SELECT * FROM public.student WHERE student_id=:_id")
        new_result = connection.execute(new_qry, _id=_id)
        update_user_student = []
        for value in new_result:
            update_user_student.append(
                {"student_id":value['student_id'],
                 "num of courses enrolled":value['num_of_courses_enrolled'],
                 "num of courses completed":value['num_of_courses_completed'],
                 "first name":value['first_name'],
                 "last name":value['last_name'],
                 "username":value['user_name'],
                 "email":value['email']}
                 )
        return jsonify(update_user_student)

### Course Management ###
## Create New Course ##
@app.route('/elearning/courses/new', methods=['POST'])
def create_new_course():
    body = request.json
    _id = body.get('instructor_id')
    title = body.get('title')
    description =  body.get('description')
    prerequisite = body.get('prerequisite')
    with engine.connect() as connection:
        course = text("INSERT INTO public.course(instructor_id, title, description)\
                    VALUE(:instructor_id, :title, :description)")
        course_result = connection.execute(course, instructor_id=_id,
                                         title=title,
                                         description=description)
        get_new_course_id = text("SELECT course_id FROM public.course AS c\
                               WHERE c.title=:title")
        course_id_result = connection.execute(get_new_course_id, title=title)
        for value in course_id_result:
            new_course_id = value['course_id']
        prerequisite = text("INSERT INTO public.course(course_id, prerequisite_id)\
                            VALUE(:new_course_id, :prerequisite_id)")
        prerequisite_result = connection.execute(prerequisite,new_course_id=new_course_id, prerequisite_id=prerequisite_id)
        # prerequisite appears still on id number form #
        new_course = text("SELECT * FROM public.course AS c\
                           JOIN public.prerequisite AS p\
                           ON p.course_id=c.course_id\
                           WHERE c.course_id=:new_course_id")
        new_result = connection.execute(new_course, new_course_id=new_course_id)
        current_course = []
        # number of courses enroll still manual #
        for value in new_result:
            current_course.append(
                {"course id":value['course_id'],
                 "instructor id":value['instructor_id'],
                 "title":value['title'],
                 "description":value['description'],
                 "prerequisite":value['prerequisite'],
                 "num of courses enrolled":value['num_of_courses_enrolled']
                 )
        return jsonify(current_course)           

## Update Course ##
@app.route('/elearning/courses/edit', methods=['PUT'])
def update_course(_id):
    _id = int(request.args.get('course_id'))
    body = request.json
    instructor_id = body.get('instructor_id')
    title = body.get('title')
    description = body.get('description')
    prerequisite = body.get('prerequisite')
    with engine.connect() as connection:
        course = text("UPDATE public.course SET instructor_id=:instructor_id, title=:title, description=:description\
                       WHERE course_id=:_id")
        course_result = connection.execute(course, instructor_id=_id,
                                         title=title,
                                         description=description
                                         _id=_id)   
        prerequisite = text("INSERT INTO public.course(course_id, prerequisite_id)\
                            VALUE(:_id, :prerequisite_id)")
        prerequisite_result = connection.execute(prerequisite, _id=_id, prerequisite_id=prerequisite_id)
        # prerequisite appears still on id number form #
        revise_course = text("SELECT * FROM public.course AS c\
                           JOIN public.prerequisite AS p\
                           ON p.course_id=c.course_id\
                           WHERE c.course_id=:_id")
        new_result = connection.execute(revise_course, _id=_id)
        revised_course = []
        # number of courses enroll still manual #
        for value in new_result:
            revised_course.append(
                {"course id":value['course_id'],
                 "instructor id":value['instructor_id'],
                 "title":value['title'],
                 "description":value['description'],
                 "prerequisite":value['prerequisite'],
                 "num of courses enrolled":value['num_of_courses_enrolled']
                 )
        return jsonify(revised_course)   






@app.route('/employee/add', methods=['POST'])
def add_employee():
    body_req = request.json
    nik = body_req.get('nik')
    name = body_req.get('name')
    start_year = body_req.get('start year')
    with engine.connect() as connection:
        qry = text("INSERT INTO public.employee(nik, name, start_year)\
                    VALUES (:nik, :name, :start_year)")
        result = connection.execute(qry, nik=nik, name=name, start_year=start_year)
        new_qry = text("SELECT * FROM public.employee")
        new_result = connection.execute(new_qry)
        post = []
        for value in new_result:
            post.append({"nik":value['nik'], "name":value['name'], "start year":value['start_year']})
        return jsonify(post)

@app.route('/employee/update', methods=['PUT'])
def update_employee():
    body = request.json
    nik = body.get('nik')
    name = body.get('name')
    start_year = body.get('start year')
    with engine.connect() as connection:
        qry = text("UPDATE public.employee SET name=:name, start_year=:start_year\
                    WHERE nik=:nik")
        result = connection.execute(qry, nik=nik, name=name, start_year=start_year)
        new_qry = text("SELECT * FROM public.employee")
        new_result = connection.execute(new_qry)
        put = []
        for value in new_result:
            put.append({"nik":value['nik'], "name":value['name'], "start year":value['start_year']})
        return jsonify(put)

@app.route('/employee/delete', methods=['DELETE'])
def delete_employee():
    body_req = request.json
    nik = request.args.get('nik')
    with engine.connect() as connection:
        qry = text("DELETE FROM public.employee\
                    WHERE nik=:nik")
        result = connection.execute(qry, nik=nik)
        new_qry = text("SELECT * FROM public.employee")
        new_result = connection.execute(new_qry)
        post = []
        for value in new_result:
            post.append({"nik":value['nik'], "name":value['name'], "start year":value['start_year']})
        return jsonify(post)

if __name__ == '__main__':
    app.run(debug=True)