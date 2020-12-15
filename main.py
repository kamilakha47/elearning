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
                    VALUES(:first_name, :last_name, :user_name, :email)")
        connection.execute(qry,first_name=first_name,
                                last_name=last_name,
                                user_name=user_name,
                                email=email)
        new_qry = text("SELECT * FROM public.instructor WHERE user_name=:user_name")
        new_result = connection.execute(new_qry, user_name=user_name)
        new_user_instructor = []
        # Constraints: email can be filled with other forms (ex. email must be @gmail/@yahoo etc, but it can fill anything as long as varchar)
                        # username is not unique
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
                    VALUES(:first_name, :last_name, :user_name, :email)")
        connection.execute(qry,first_name=first_name,
                                    last_name=last_name,
                                    user_name=user_name,
                                    email=email)
        new_qry = text("SELECT * FROM public.student WHERE user_name=:user_name")
        new_result = connection.execute(new_qry, user_name=user_name)
        new_user_student = []
        for value in new_result:
            new_user_student.append(
                {"student id":value['student_id'],
                 "first name":value['first_name'],
                 "last name":value['last_name'],
                 "username":value['user_name'],
                 "email":value['email']})
        return jsonify(new_user_student)

# Update User For Instructor#
@app.route('/elearning/user/edit/instructor', methods=['PUT'])
def edit_user_instructor():
    body_req = request.json
    _id = int(request.args.get('instructor_id'))
    first = body_req.get('first_name')
    last = body_req.get('last_name')
    user = body_req.get('user_name')
    email = body_req.get('email')
    with engine.connect() as connection:
        qry = text("UPDATE public.instructor SET first_name=:first, last_name=:last, user_name=:user, email=:email\
                    WHERE instructor_id=:_id")
        connection.execute(qry,first=first, last=last, user=user, email=email, _id=_id)
        new_qry = text("SELECT * FROM public.instructor WHERE instructor_id=:_id")
        new_result = connection.execute(new_qry, _id=_id)
        update_user_instructor = []
        for value in new_result:
            update_user_instructor.append(
                {"instructor id":value['instructor_id'],
                 "first name":value['first_name'],
                 "last name":value['last_name'],
                 "username":value['user_name'],
                 "email":value['email']})
        return jsonify(update_user_instructor)

# Update User For Student#
@app.route('/elearning/user/edit/student', methods=['PUT'])
def edit_user_student():
    body_req = request.json
    _id = int(request.args.get('student_id'))
    first = body_req.get('first_name')
    last = body_req.get('last_name')
    user = body_req.get('user_name')
    email = body_req.get('email')
    with engine.connect() as connection:
        qry = text("UPDATE public.student SET first_name=:first, last_name=:last, user_name=:user, email=:email\
                    WHERE student_id=:_id")
        connection.execute(qry,first=first, last=last, user=user, email=email, _id=_id)
        new_qry = text("SELECT * FROM public.student WHERE student_id=:_id")
        new_result = connection.execute(new_qry, _id=_id)
        update_user_student = []
        for value in new_result:
            update_user_student.append(
                {"student_id":value['student_id'],
                 "first name":value['first_name'],
                 "last name":value['last_name'],
                 "username":value['user_name'],
                 "email":value['email']})
        return jsonify(update_user_student)

### Course Management ###
## Create New Course ##
@app.route('/elearning/courses/new', methods=['POST'])
def create_new_course():
    body = request.json
    _id = body.get('instructor_id')
    title = body.get('title')
    description =  body.get('description')
    prerequisite_id = body.get('prerequisite_id')
    with engine.connect() as connection:
        course = text("INSERT INTO public.course(instructor_id, title, description)\
                       VALUES(:instructor_id, :title, :description)")
        connection.execute(course, instructor_id=_id, title=title, description=description)
        get_new_course_id = text("SELECT course_id FROM public.course AS c WHERE c.title=:title")
        course_id_result = connection.execute(get_new_course_id, title=title)
        for value in course_id_result:
            new_course_id = int(value['course_id'])
        if prerequisite_id != 0:
            for item in prerequisite_id:
                prerequisite = text("INSERT INTO public.prerequisite(course_id, prerequisite_id)\
                                    VALUES(:new_course_id, :item)")
                connection.execute(prerequisite,new_course_id=new_course_id, item=item)
        elif prerequisite_id == 0:
            prerequisite = text("INSERT INTO public.prerequisite(course_id)\
                                 VALUES(:new_course_id)")
            connection.execute(prerequisite,new_course_id=new_course_id)
        # prerequisite appears on id number form #
        new_course = text("SELECT * FROM public.course AS c\
                           JOIN public.prerequisite AS p\
                           ON p.course_id=c.course_id\
                           WHERE c.course_id=:new_course_id")
        new_result = connection.execute(new_course, new_course_id=new_course_id)
        current_course = []
        for value in new_result:
            current_course.append(
                {"course id":value['course_id'],
                 "instructor id":value['instructor_id'],
                 "title":value['title'],
                 "description":value['description'],
                 "prerequisite":value['prerequisite_id']})
        return jsonify(current_course)

## Update Course ##
@app.route('/elearning/courses/edit', methods=['PUT'])
def update_course():
    _id = int(request.args.get('course_id'))
    body = request.json
    instructor_id = body.get('instructor_id')
    title = body.get('title')
    description = body.get('description')
    prerequisite_id = body.get('prerequisite_id')
    with engine.connect() as connection:
        course = text("UPDATE public.course SET instructor_id=:instructor_id, title=:title, description=:description\
                       WHERE course_id=:_id")
        connection.execute(course, instructor_id=instructor_id, title=title, description=description, _id=_id)   
        existing = text("SELECT p.prerequisite_id FROM public.prerequisite AS p\
                        JOIN public.course AS c ON c.course_id=p.course_id\
                        WHERE c.course_id=:_id")
        e_result = connection.execute(existing, _id=_id)
        data = [i[0] for i in e_result]
        for x, instance in enumerate(prerequisite_id):
            prerequisite = text("UPDATE public.prerequisite SET prerequisite_id=:instance\
                                WHERE course_id=:_id AND prerequisite_id=:data")
            connection.execute(prerequisite, _id=_id, instance=instance, data=data[x])
        # Constraints: Can't add/insert new row for prequisite after course established, update ONLY suit number of rows in prerequisite
        # prerequisite appears on id number form #
        revise_course = text("SELECT * FROM public.course AS c\
                           JOIN public.prerequisite AS p\
                           ON p.course_id=c.course_id\
                           WHERE c.course_id=:_id")
        new_result = connection.execute(revise_course, _id=_id)
        revised_course = []
        for value in new_result:
            revised_course.append(
                {"course id":value['course_id'],
                 "instructor id":value['instructor_id'],
                 "title":value['title'],
                 "description":value['description'],
                 "prerequisite id":value['prerequisite_id']})
        return jsonify(revised_course)

## Enroll the Course ##
@app.route('/elearning/courses/new/enroll', methods=['POST'])
def enroll_the_course():
    _id = int(request.args.get('student_id'))
    course_id = int(request.args.get('course_id'))
    with engine.connect() as connection:
        taken = text ("SELECT student.student_id, learning_progress.status, enrollment.course_id\
                         FROM enrollment JOIN student ON student.student_id = enrollment.student_id\
                         JOIN learning_progress ON learning_progress.enrollment_id=enrollment.enrollment_id\
                         WHERE student.student_id=:_id")
        taken_course = connection.execute(taken,_id=_id)
        course_taken = []
        course_pick = (course_id,)
        for value in taken_course:
            course_taken.append(value['course_id'])
        process = all(item in course_taken for item in course_pick)
        if process is True:
            return jsonify("Course has been taken")
        else:
            st_enrolled = text("SELECT student.student_id, count(learning_progress.status) as lp\
                            FROM enrollment JOIN student ON student.student_id = enrollment.student_id\
                            JOIN learning_progress ON learning_progress.enrollment_id=enrollment.enrollment_id\
                            WHERE learning_progress.status='P' AND student.student_id=:_id\
                            GROUP BY student.student_id")
            st_enrolled_result = connection.execute(st_enrolled, _id=_id)
            num = []
            for value in st_enrolled_result:
                num.append(value['lp'])
            if num == [] or num[0] < 5:
                l_course = text("SELECT course.course_id\
                            FROM enrollment JOIN student ON student.student_id = enrollment.student_id\
                            JOIN course ON course.course_id=enrollment.course_id\
                            JOIN learning_progress ON enrollment.enrollment_id=learning_progress.enrollment_id\
                            WHERE learning_progress.status = 'C' and student.student_id=:_id")
                l_course_student = connection.execute(l_course, _id=_id)
                lcs = [0]
                for value in l_course_student:
                    lcs.append(value['course_id'])
                l_prerequisite = text("SELECT CASE WHEN prerequisite.prerequisite_id IS NULL THEN 0 ELSE prerequisite.prerequisite_id END\
                                    FROM course JOIN prerequisite ON course.course_id=prerequisite.course_id\
                                    WHERE course.course_id=:course_id")
                l_p = connection.execute(l_prerequisite, course_id=course_id)
                lp1 = []
                for value in l_p:
                    lp1.append(value['prerequisite_id'])
                check = all(item in lcs for item in lp1)
                if check is True:
                    enroll = text("INSERT INTO public.enrollment(student_id, course_id)\
                                    VALUES(:_id, :course_id)")
                    connection.execute(enroll, _id=_id, course_id=course_id)
                    enrolled = text("SELECT e.enrollment_id, s.first_name, s.last_name, c.course_id\
                                        FROM enrollment AS e JOIN student AS s ON e.student_id=s.student_id\
                                        JOIN course AS c ON c.course_id=e.course_id\
                                        WHERE c.course_id=:course_id AND s.student_id=:_id")
                    enrolled_result = connection.execute(enrolled, _id=_id, course_id=course_id)
                    create_enroll = []
                    create_update = []
                    for value in enrolled_result:
                            create_enroll.append(
                                {"enrollment id":value['enrollment_id'],
                                "first name":value['first_name'],
                                "last name":value['last_name'],
                                "course id":value['course_id']})
                            create_update.append(value['enrollment_id'])
                    update_status = text("INSERT INTO public.learning_progress(enrollment_id, status)\
                                        VALUES(:new_enrollment, 'P')")
                    connection.execute(update_status, new_enrollment=create_update[0])
                    return jsonify(create_enroll)
                else:
                    return jsonify("Can't Add Enroll the Course Because Prerequisite Courses Haven't Completed yet")
            else:
                return jsonify("Can't Add Enroll the Course Because Maximum Enroll of Five")

## Get list users enrolled to course ##
@app.route('/elearning/courses/list/enroll', methods=['GET'])
def get_list_users():
    course_id = int(request.args.get('course_id'))
    with engine.connect() as connection:
        qry = text("SELECT s.student_id, s.first_name, s.last_name, c.course_id, c.title\
                    FROM public.enrollment AS e\
                    JOIN public.student AS s ON e.student_id=s.student_id\
                    JOIN public.course AS c ON e.course_id=c.course_id\
                    WHERE e.course_id=:course_id")
        result = connection.execute(qry,course_id=course_id)
        users = []
        for value in result:
            users.append(
                {"student id":value['student_id'],
                "first name":value['first_name'],
                "last name":value['last_name'],
                "course id":value['course_id'],
                "title":value['title']})
        return jsonify(users)

## Complete and DropOut Course ##
## Number of student who drops the course??
@app.route('/elearning/courses/status', methods=['GET'])
def complete_course():
    status = request.args.get('status') # This column status is filled with 'D' (Drop), 'P'(Progress), 'C'(Complete)
    with engine.connect() as connection:
        qry = text("SELECT student_id, first_name, last_name, title, status\
                    FROM public.list_enroll_by_student\
                    WHERE status=:status")
        result = connection.execute(qry, status=status)
        list_status = []
        for value in result:
            list_status.append(
                {"student id":value['student_id'],
                "first name":value['first_name'],
                "last name":value['last_name'],
                "title":value['title'],
                "status":value['status']})
        return jsonify(list_status)

## Student Drop Out the Course ##
@app.route('/elearning/courses/users/drop', methods=['PUT'])
def drop_course():
    student_id = int(request.args.get('student_id'))
    course_id = int(request.args.get('course_id'))
    status = request.args.get('status')
    # Constraints: There is no message status changing from 'C' can't be 'P', thus we can change 
    with engine.connect() as connection:
        drop = text("UPDATE public.learning_progress AS lp\
                     SET status =:status\
                     FROM public.enrollment AS e\
                     WHERE lp.enrollment_id = e.enrollment_id AND\
                            e.student_id =:student_id AND\
                            e.course_id =:course_id")
        connection.execute(drop, student_id=student_id, course_id=course_id, status=status)
        validation = text("SELECT s.student_id, s.first_name, s.last_name, c.course_id, c.title, lp.status\
                           FROM public.enrollment AS e\
                           JOIN public.student AS s ON e.student_id=s.student_id\
                           JOIN public.course AS c ON e.course_id=c.course_id\
                           JOIN public.learning_progress AS lp ON e.enrollment_id=lp.enrollment_id\
                           WHERE e.course_id=:course_id AND s.student_id=:student_id")
        validation_result = connection.execute(validation, course_id=course_id, student_id=student_id)
        drop_course = []
        for value in validation_result:
            drop_course.append(
                {"student id":value['student_id'],
                 "first name":value['first_name'],
                 "last name":value['last_name'],
                 "course id":value['course_id'],
                 "title":value['title'],
                 "status":value['status']})
        return jsonify(drop_course)

## Search The Course By title, description, or prerequisite##
@app.route('/elearning/courses/search', methods=['GET'])
def search_the_courses():
    value = request.args.get('value')
    #prerequisite still id#
    with engine.connect() as connection:
        search = text(f"SELECT title FROM public.course\
                       WHERE title ~* '{value}' OR description ~* '{value}' ")
        search_result = connection.execute(search)
        searching = []
        for value in search_result:
            searching.append(
                {"search":value['title']})
        return jsonify(searching)

## Get List Top 5 Student Most Compeleted The Course ##
@app.route('/elearning/courses/top/student', methods=['GET'])
def top_5_student():
    with engine.connect() as connection:
        top_student = text("SELECT first_name, last_name, COUNT(status) AS num_complete\
                        FROM public.list_enroll_by_student\
                        WHERE status='C'\
                        GROUP BY first_name, last_name\
                        ORDER BY num_complete DESC\
                        LIMIT 5")
        top_student_result = connection.execute(top_student)
        top_5 = []
        for value in top_student_result:
            top_5.append(
                {"first name":value['first_name'],
                 "last name":value['last_name'],
                 "number of complete course":value['num_complete']})
        return jsonify(top_5)

## Get List Top 5 Courses Enrolled By Student ##
@app.route('/elearning/courses/top/enrolled', methods=['GET'])
def top_5_courses():
    with engine.connect() as connection:
        top_courses = text("SELECT course.title, count(enrollment.enrollment_id) AS count\
                            FROM course, enrollment\
                            WHERE course.course_id = enrollment.course_id\
                            GROUP BY course.title, course.course_id\
                            ORDER BY count DESC, course.title ASC\
                            LIMIT 5")
        top_courses_result = connection.execute(top_courses)
        top_5_c = []
        for value in top_courses_result:
            top_5_c.append(
                {"title":value['title'],
                 "number of courses enrolled":value['count']})
        return jsonify(top_5_c)

