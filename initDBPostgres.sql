-- Database: elearning

-- DROP DATABASE elearning;

CREATE DATABASE elearning
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Indonesian_Indonesia.1252'
    LC_CTYPE = 'Indonesian_Indonesia.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

-- Table: public.course

-- DROP TABLE public.course;

CREATE TABLE public.course
(
    course_id integer NOT NULL DEFAULT nextval('course_course_id_seq'::regclass),
    instructor_id integer NOT NULL,
    title character varying(100) COLLATE pg_catalog."default" NOT NULL,
    description character varying(100) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT course_id_pkey PRIMARY KEY (course_id),
    CONSTRAINT instructor_id_fkey FOREIGN KEY (instructor_id)
        REFERENCES public.instructor (instructor_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.course
    OWNER to postgres;

-- Table: public.enrollment

-- DROP TABLE public.enrollment;

CREATE TABLE public.enrollment
(
    enrollment_id integer NOT NULL DEFAULT nextval('enrolment_id_enrolment_id_seq'::regclass),
    student_id integer NOT NULL,
    course_id integer NOT NULL,
    enrollment_date timestamp without time zone NOT NULL DEFAULT now(),
    CONSTRAINT enrollment_id_pkey PRIMARY KEY (enrollment_id),
    CONSTRAINT course_id_fkey FOREIGN KEY (course_id)
        REFERENCES public.course (course_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT student_id_fkey FOREIGN KEY (student_id)
        REFERENCES public.student (student_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.enrollment
    OWNER to postgres;


-- Table: public.instructor

-- DROP TABLE public.instructor;

CREATE TABLE public.instructor
(
    instructor_id integer NOT NULL DEFAULT nextval('instructor_instructor_id_seq'::regclass),
    active boolean DEFAULT true,
    first_name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    last_name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    user_name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    email character varying(100) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT instructor_id_pkey PRIMARY KEY (instructor_id)
)

TABLESPACE pg_default;

ALTER TABLE public.instructor
    OWNER to postgres;

-- Table: public.learning_progress

-- DROP TABLE public.learning_progress;

CREATE TABLE public.learning_progress
(
    enrollment_id integer NOT NULL,
    status t_status NOT NULL,
    CONSTRAINT learning_progress_pkey PRIMARY KEY (enrollment_id),
    CONSTRAINT enrolment_id_fkey FOREIGN KEY (enrollment_id)
        REFERENCES public.enrollment (enrollment_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.learning_progress
    OWNER to postgres;

-- Table: public.prerequisite

-- DROP TABLE public.prerequisite;

CREATE TABLE public.prerequisite
(
    course_id integer NOT NULL,
    prerequisite_id integer,
    CONSTRAINT course_id_fkey FOREIGN KEY (course_id)
        REFERENCES public.course (course_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT prerequisite_id_fkey FOREIGN KEY (prerequisite_id)
        REFERENCES public.course (course_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE public.prerequisite
    OWNER to postgres;

-- Table: public.student

-- DROP TABLE public.student;

CREATE TABLE public.student
(
    student_id integer NOT NULL DEFAULT nextval('student_student_id_seq'::regclass),
    registration_date date DEFAULT CURRENT_DATE,
    active boolean NOT NULL DEFAULT true,
    first_name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    last_name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    user_name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    email character varying(100) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT student_id_pkey PRIMARY KEY (student_id)
)

TABLESPACE pg_default;

ALTER TABLE public.student
    OWNER to postgres;

-- Type: t_status

-- DROP TYPE public.t_status;

CREATE TYPE public.t_status AS ENUM
    ('D', 'P', 'C');

ALTER TYPE public.t_status
    OWNER TO postgres;

-- View: public.list_enroll_by_student

-- DROP VIEW public.list_enroll_by_student;

CREATE OR REPLACE VIEW public.list_enroll_by_student
 AS
 SELECT s.student_id,
    s.first_name,
    s.last_name,
    c.title,
    lp.status
   FROM (((enrollment e
     JOIN student s ON ((e.student_id = s.student_id)))
     JOIN course c ON ((e.course_id = c.course_id)))
     JOIN learning_progress lp ON ((e.enrollment_id = lp.enrollment_id)));

ALTER TABLE public.list_enroll_by_student
    OWNER TO postgres;

-- SEQUENCE: public.course_course_id_seq

-- DROP SEQUENCE public.course_course_id_seq;

CREATE SEQUENCE public.course_course_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.course_course_id_seq
    OWNER TO postgres;

-- SEQUENCE: public.enrolment_id_enrolment_id_seq

-- DROP SEQUENCE public.enrolment_id_enrolment_id_seq;

CREATE SEQUENCE public.enrolment_id_enrolment_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.enrolment_id_enrolment_id_seq
    OWNER TO postgres;

-- SEQUENCE: public.instructor_instructor_id_seq

-- DROP SEQUENCE public.instructor_instructor_id_seq;

CREATE SEQUENCE public.instructor_instructor_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.instructor_instructor_id_seq
    OWNER TO postgres;

-- SEQUENCE: public.student_student_id_seq

-- DROP SEQUENCE public.student_student_id_seq;

CREATE SEQUENCE public.student_student_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.student_student_id_seq
    OWNER TO postgres;