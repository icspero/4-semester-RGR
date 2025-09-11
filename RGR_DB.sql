--
-- PostgreSQL database dump
--

\restrict GDAyeK0oCsYNGERprUNNA4OgA5BjJSO9U20cte5Xozvb9guZTnbTgCO7zqiH7tb

-- Dumped from database version 17.6 (Ubuntu 17.6-1.pgdg24.04+1)
-- Dumped by pg_dump version 17.6 (Ubuntu 17.6-1.pgdg24.04+1)

-- Started on 2025-09-11 15:30:21 +07

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 227 (class 1259 OID 16445)
-- Name: accesslog; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accesslog (
    log_id integer NOT NULL,
    doctor_id integer NOT NULL,
    card_id integer NOT NULL,
    access_time timestamp without time zone NOT NULL,
    access_type character varying(20) NOT NULL
);


ALTER TABLE public.accesslog OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 16444)
-- Name: accesslog_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.accesslog_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.accesslog_log_id_seq OWNER TO postgres;

--
-- TOC entry 3500 (class 0 OID 0)
-- Dependencies: 226
-- Name: accesslog_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.accesslog_log_id_seq OWNED BY public.accesslog.log_id;


--
-- TOC entry 223 (class 1259 OID 16417)
-- Name: doctorpatient; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.doctorpatient (
    doctor_id integer NOT NULL,
    patient_id integer NOT NULL
);


ALTER TABLE public.doctorpatient OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16433)
-- Name: medicalcard; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.medicalcard (
    card_id integer NOT NULL,
    patient_id integer NOT NULL,
    diagnosis character varying(200) NOT NULL,
    treatment_plan character varying(200) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.medicalcard OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 16432)
-- Name: medicalcard_card_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.medicalcard_card_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.medicalcard_card_id_seq OWNER TO postgres;

--
-- TOC entry 3501 (class 0 OID 0)
-- Dependencies: 224
-- Name: medicalcard_card_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.medicalcard_card_id_seq OWNED BY public.medicalcard.card_id;


--
-- TOC entry 222 (class 1259 OID 16411)
-- Name: patient; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.patient (
    visitor_id integer NOT NULL,
    full_name character varying(100) NOT NULL,
    phone_number character varying(30) NOT NULL,
    is_patient boolean NOT NULL,
    date_registration timestamp without time zone NOT NULL
);


ALTER TABLE public.patient OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16410)
-- Name: patient_visitor_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.patient_visitor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.patient_visitor_id_seq OWNER TO postgres;

--
-- TOC entry 3502 (class 0 OID 0)
-- Dependencies: 221
-- Name: patient_visitor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.patient_visitor_id_seq OWNED BY public.patient.visitor_id;


--
-- TOC entry 218 (class 1259 OID 16390)
-- Name: role; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.role (
    role_id integer NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.role OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16389)
-- Name: role_role_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.role_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.role_role_id_seq OWNER TO postgres;

--
-- TOC entry 3503 (class 0 OID 0)
-- Dependencies: 217
-- Name: role_role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.role_role_id_seq OWNED BY public.role.role_id;


--
-- TOC entry 220 (class 1259 OID 16397)
-- Name: staff; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.staff (
    staff_id integer NOT NULL,
    last_name character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    middle_name character varying(30),
    phone_number character varying(30) NOT NULL,
    login character varying(30) NOT NULL,
    password character varying(100) NOT NULL,
    role_id integer NOT NULL
);


ALTER TABLE public.staff OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16396)
-- Name: staff_staff_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.staff_staff_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.staff_staff_id_seq OWNER TO postgres;

--
-- TOC entry 3504 (class 0 OID 0)
-- Dependencies: 219
-- Name: staff_staff_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.staff_staff_id_seq OWNED BY public.staff.staff_id;


--
-- TOC entry 3318 (class 2604 OID 16448)
-- Name: accesslog log_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accesslog ALTER COLUMN log_id SET DEFAULT nextval('public.accesslog_log_id_seq'::regclass);


--
-- TOC entry 3317 (class 2604 OID 16436)
-- Name: medicalcard card_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medicalcard ALTER COLUMN card_id SET DEFAULT nextval('public.medicalcard_card_id_seq'::regclass);


--
-- TOC entry 3316 (class 2604 OID 16414)
-- Name: patient visitor_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.patient ALTER COLUMN visitor_id SET DEFAULT nextval('public.patient_visitor_id_seq'::regclass);


--
-- TOC entry 3314 (class 2604 OID 16393)
-- Name: role role_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role ALTER COLUMN role_id SET DEFAULT nextval('public.role_role_id_seq'::regclass);


--
-- TOC entry 3315 (class 2604 OID 16400)
-- Name: staff staff_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staff ALTER COLUMN staff_id SET DEFAULT nextval('public.staff_staff_id_seq'::regclass);


--
-- TOC entry 3494 (class 0 OID 16445)
-- Dependencies: 227
-- Data for Name: accesslog; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accesslog (log_id, doctor_id, card_id, access_time, access_type) FROM stdin;
23	9	13	2025-09-11 08:14:32.986497	view
24	9	13	2025-09-11 08:17:04.055764	view
25	9	13	2025-09-11 08:17:05.464754	view
26	11	14	2025-09-11 08:19:06.135247	view
27	9	13	2025-09-11 08:20:09.962898	view
28	9	13	2025-09-11 08:20:13.880261	view
\.


--
-- TOC entry 3490 (class 0 OID 16417)
-- Dependencies: 223
-- Data for Name: doctorpatient; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.doctorpatient (doctor_id, patient_id) FROM stdin;
9	10
11	11
\.


--
-- TOC entry 3492 (class 0 OID 16433)
-- Dependencies: 225
-- Data for Name: medicalcard; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.medicalcard (card_id, patient_id, diagnosis, treatment_plan, created_at, updated_at) FROM stdin;
13	10	Дота 2	Нету	2025-09-11 08:12:35.861257	2025-09-11 08:12:35.861261
14	11	ОРВИ	Сидеть дома	2025-09-11 08:19:02.038843	2025-09-11 08:19:02.038847
\.


--
-- TOC entry 3489 (class 0 OID 16411)
-- Dependencies: 222
-- Data for Name: patient; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.patient (visitor_id, full_name, phone_number, is_patient, date_registration) FROM stdin;
10	Тырышкин Клим Андреевич	89030778914	t	2025-09-11 08:11:07.54036
11	Вовкин Вова Вовочкин	88003451267	t	2025-09-11 08:18:41.03703
\.


--
-- TOC entry 3485 (class 0 OID 16390)
-- Dependencies: 218
-- Data for Name: role; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.role (role_id, name) FROM stdin;
6	Doctor
7	Admin
\.


--
-- TOC entry 3487 (class 0 OID 16397)
-- Dependencies: 220
-- Data for Name: staff; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.staff (staff_id, last_name, first_name, middle_name, phone_number, login, password, role_id) FROM stdin;
9	Самойлов	Сергей	Ярославович	89005554545	sergey	$2b$12$aoI6P8CXkR/3lPNsT4c4YusZHDo6t.cf02ZbGghnn/SLZthKqjj3m	6
10	Глеб	Щудро	Алексеевич	88006663636	gleb	$2b$12$/t5eqxZWiGK.DVaLFtFzY.dW4pr14/bu2/PIFJyfkiz2iBsmdDJw6	7
11	Наумов	Глеб		89004567898	glebn	$2b$12$fyJPGR.rrYzR1asxuCYRu.jkVQcfDptZZ76yuCkxnZWpaPFwbeQ3y	6
\.


--
-- TOC entry 3505 (class 0 OID 0)
-- Dependencies: 226
-- Name: accesslog_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accesslog_log_id_seq', 28, true);


--
-- TOC entry 3506 (class 0 OID 0)
-- Dependencies: 224
-- Name: medicalcard_card_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.medicalcard_card_id_seq', 14, true);


--
-- TOC entry 3507 (class 0 OID 0)
-- Dependencies: 221
-- Name: patient_visitor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.patient_visitor_id_seq', 11, true);


--
-- TOC entry 3508 (class 0 OID 0)
-- Dependencies: 217
-- Name: role_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.role_role_id_seq', 7, true);


--
-- TOC entry 3509 (class 0 OID 0)
-- Dependencies: 219
-- Name: staff_staff_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.staff_staff_id_seq', 11, true);


--
-- TOC entry 3332 (class 2606 OID 16450)
-- Name: accesslog accesslog_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accesslog
    ADD CONSTRAINT accesslog_pkey PRIMARY KEY (log_id);


--
-- TOC entry 3328 (class 2606 OID 16421)
-- Name: doctorpatient doctorpatient_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doctorpatient
    ADD CONSTRAINT doctorpatient_pkey PRIMARY KEY (doctor_id, patient_id);


--
-- TOC entry 3330 (class 2606 OID 16438)
-- Name: medicalcard medicalcard_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medicalcard
    ADD CONSTRAINT medicalcard_pkey PRIMARY KEY (card_id);


--
-- TOC entry 3326 (class 2606 OID 16416)
-- Name: patient patient_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.patient
    ADD CONSTRAINT patient_pkey PRIMARY KEY (visitor_id);


--
-- TOC entry 3320 (class 2606 OID 16395)
-- Name: role role_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_pkey PRIMARY KEY (role_id);


--
-- TOC entry 3322 (class 2606 OID 16404)
-- Name: staff staff_login_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staff
    ADD CONSTRAINT staff_login_key UNIQUE (login);


--
-- TOC entry 3324 (class 2606 OID 16402)
-- Name: staff staff_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staff
    ADD CONSTRAINT staff_pkey PRIMARY KEY (staff_id);


--
-- TOC entry 3337 (class 2606 OID 16456)
-- Name: accesslog fk_accesslog_card; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accesslog
    ADD CONSTRAINT fk_accesslog_card FOREIGN KEY (card_id) REFERENCES public.medicalcard(card_id);


--
-- TOC entry 3338 (class 2606 OID 16451)
-- Name: accesslog fk_accesslog_doctor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accesslog
    ADD CONSTRAINT fk_accesslog_doctor FOREIGN KEY (doctor_id) REFERENCES public.staff(staff_id);


--
-- TOC entry 3334 (class 2606 OID 16422)
-- Name: doctorpatient fk_doctor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doctorpatient
    ADD CONSTRAINT fk_doctor FOREIGN KEY (doctor_id) REFERENCES public.staff(staff_id);


--
-- TOC entry 3336 (class 2606 OID 16439)
-- Name: medicalcard fk_medicalcard_patient; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medicalcard
    ADD CONSTRAINT fk_medicalcard_patient FOREIGN KEY (patient_id) REFERENCES public.patient(visitor_id);


--
-- TOC entry 3335 (class 2606 OID 16427)
-- Name: doctorpatient fk_patient; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doctorpatient
    ADD CONSTRAINT fk_patient FOREIGN KEY (patient_id) REFERENCES public.patient(visitor_id);


--
-- TOC entry 3333 (class 2606 OID 16405)
-- Name: staff fk_staff_role; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staff
    ADD CONSTRAINT fk_staff_role FOREIGN KEY (role_id) REFERENCES public.role(role_id);


-- Completed on 2025-09-11 15:30:21 +07

--
-- PostgreSQL database dump complete
--

\unrestrict GDAyeK0oCsYNGERprUNNA4OgA5BjJSO9U20cte5Xozvb9guZTnbTgCO7zqiH7tb

