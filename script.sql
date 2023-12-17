create schema accounting

create table accounting.faculties
(
	id smallint,
	full_name varchar(63),
	address varchar(127),
	deans_room_num smallint,
	dean_full_name varchar(63),
	dean_phone bigint,
	dean_email varchar(320),
	primary key (id)
);

create table accounting.departments
(
	id smallint,
	full_name varchar(63),
	address varchar(127),
	depart_room_num smallint,
	head_of_depart_full_name varchar(63),
	head_of_depart_phone bigint,
	head_of_depart_email varchar(320),
	faculty_id smallint REFERENCES accounting.faculties (id),
	primary key (id)
);

create table accounting.curators
(
	personnel_number smallint,
	full_name varchar(63),
	job_title varchar(31),
	academic_degree varchar(3),
	phone_number bigint,
	email varchar(320),
	depart_id smallint REFERENCES accounting.departments (id),
	primary key (personnel_number)
);

create table accounting.specialties
(
	code varchar(12),
	full_name varchar(63),
	primary key (code)
);

create table accounting.groups
(
	id smallint,
	formation_year smallint,
	study_year smallint,
	head_of_group_id integer,
	speciality_code varchar(12) REFERENCES accounting.specialties (code),
	depart_id smallint REFERENCES accounting.departments (id),
	primary key (id)
);

create table accounting.curators_groups
(
	personnel_number smallint REFERENCES accounting.curators (personnel_number),
	group_id smallint REFERENCES accounting.groups (id)
);

create table accounting.students
(
	id integer,
	full_name varchar(63),
	payment_basis varchar(11),
	living_address varchar(127),
	inn bigint,
	email varchar(320),
	phone_number bigint,
	phone_number_parent_1 bigint,
	phone_number_parent_2 bigint,
	role_in_group varchar(12),
	type_of_scholarship varchar(11),
	group_id smallint REFERENCES accounting.groups (id),
	primary key (id)
);

create table accounting.passport_data
(
	document_number integer,
	issue_date date,
	series smallint,
	depart_code integer,
	registration_address varchar(127),
	student_id integer REFERENCES accounting.students (id),
	primary key (document_number)
);