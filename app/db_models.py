from typing import List
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    BigInteger,
    SmallInteger,
    Integer,
    Date,
    Table,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase, synonym


class Base(DeclarativeBase):
    pass


class Faculty(Base):
    __tablename__ = "faculties"

    desc = "Факультет"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(63))
    address: Mapped[str] = mapped_column(String(127))
    deans_room_num: Mapped[int] = mapped_column(SmallInteger)
    dean_full_name: Mapped[str] = mapped_column(String(63))
    dean_phone: Mapped[int] = mapped_column(BigInteger)
    dean_email: Mapped[str] = mapped_column(String(320))

    departments: Mapped[List["Department"]] = relationship(
        back_populates="faculty", cascade="all, delete-orphan"
    )

    refs: list[str] = [
        "departments",
    ]

    field_names: dict = {
        "id": "Номер факультета",
        "full_name": "Название факультета",
        "address": "Адрес факультета",
        "deans_room_num": "Номер кабинета деканата",
        "dean_full_name": "ФИО декана",
        "dean_phone": "Телефон декана",
        "dean_email": "Email декана",
    }

    id_attr = "id"

    def get_id(self):
        return self.id

    def __repr__(self) -> str:
        return f"Faculty(id={self.id!r}, \
        full_name={self.full_name!r}, \
        address={self.address!r}, \
        deans_room_num={self.deans_room_num!r}, \
        dean_full_name={self.dean_full_name!r})"

    have_name = True

    def get_name(self):
        return f"{self.full_name}"


class Department(Base):
    __tablename__ = "departments"

    desc = "Кафедра"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(63))
    address: Mapped[str] = mapped_column(String(127))
    depart_room_num: Mapped[int] = mapped_column(SmallInteger)
    head_of_depart_full_name: Mapped[str] = mapped_column(String(63))
    head_of_depart_phone: Mapped[int] = mapped_column(BigInteger)
    head_of_depart_email: Mapped[str] = mapped_column(String(320))
    faculty_id: Mapped[int] = mapped_column(SmallInteger, ForeignKey("faculties.id"))

    faculty: Mapped["Faculty"] = relationship(back_populates="departments")
    curators: Mapped[List["Curator"]] = relationship(back_populates="depart")
    groups: Mapped[List["Group"]] = relationship(back_populates="depart")

    refs: list[str] = [
        "curators",
    ]

    field_names: dict = {
        "id": "Номер кафедры",
        "full_name": "Название кафедры",
        "address": "Адрес кафедры",
        "depart_room_num": "Номер кабинета кафедры",
        "head_of_depart_full_name": "ФИО завкафедры",
        "head_of_depart_phone": "Телефон завкафедры",
        "head_of_depart_email": "Email завкафедры",
        "faculty_id": "Номер факультета",
    }

    id_attr = "id"

    def get_id(self):
        return self.id

    def __repr__(self) -> str:
        return f"Department(id={self.id!r}, \
        full_name={self.full_name!r}, \
        address={self.address!r}, \
        depart_room_num={self.depart_room_num!r}, \
        head_of_depart_full_name={self.head_of_depart_full_name!r}, \
        faculty_id={self.faculty_id!r})"

    def get_name(self):
        return f"{self.full_name}"

    have_name = True


CuratorsGroups = Table(
    "curators_groups",
    Base.metadata,
    Column("personnel_number", SmallInteger, ForeignKey("curators.personnel_number")),
    Column("group_id", SmallInteger, ForeignKey("groups.id")),
    schema="accounting",
)


class Curator(Base):
    __tablename__ = "curators"

    desc = "Куратор"

    personnel_number: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(63))
    job_title: Mapped[str] = mapped_column(String(31))
    academic_degree: Mapped[str] = mapped_column(String(3))
    phone_number: Mapped[int] = mapped_column(BigInteger)
    email: Mapped[str] = mapped_column(String(320))
    depart_id: Mapped[int] = mapped_column(SmallInteger, ForeignKey("departments.id"))

    depart: Mapped["Department"] = relationship(back_populates="curators")
    # groups: Mapped[List["CuratorsGroups"]] = relationship(back_populates="curator")
    groups: Mapped[List["Group"]] = relationship(
        "Group", secondary=CuratorsGroups, back_populates="curator"
    )

    refs: list[str] = [
        "groups",
    ]

    field_names: dict = {
        "personnel_number": "Табельный номер",
        "full_name": "ФИО",
        "job_title": "Должность",
        "academic_degree": "Степень",
        "phone_number": "Телефон",
        "email": "Email",
        "depart_id": "Номер кафедры",
    }

    linked_fields: dict = {"Group": "groups"}

    link_types: dict = {"groups": "one_to_many"}

    id_attr = "personnel_number"
    id = synonym("personnel_number")

    def get_id(self):
        return self.personnel_number

    def __repr__(self) -> str:
        return f"Curator(personnel_number={self.personnel_number!r}, \
        full_name={self.full_name!r}, \
        job_title={self.job_title!r}, \
        academic_degree={self.academic_degree!r}, \
        phone_number={self.phone_number!r}, \
        depart_id={self.depart_id!r})"

    have_name = True

    def get_name(self):
        return f"{self.full_name}"


class Speciality(Base):
    __tablename__ = "specialties"

    desc = "Специальность"

    code: Mapped[str] = mapped_column(String(12), primary_key=True)
    full_name: Mapped[str] = mapped_column(String(63))

    group: Mapped["Group"] = relationship(back_populates="spec")

    field_names: dict = {
        "code": "Код специальности",
        "full_name": "Название",
    }

    id_attr = "code"
    id = synonym("code")

    def get_id(self):
        return self.code

    def __repr__(self) -> str:
        return f"Speciality(code={self.code!r}, full_name={self.full_name!r})"

    have_name = True

    def get_name(self):
        return f"{self.full_name}"


class Group(Base):
    __tablename__ = "groups"

    desc = "Группа"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    formation_year: Mapped[int] = mapped_column(SmallInteger)
    study_year: Mapped[int] = mapped_column(SmallInteger)
    head_of_group_id: Mapped[int] = mapped_column(Integer)
    speciality_code: Mapped[str] = mapped_column(
        String(12), ForeignKey("specialties.code")
    )
    depart_id: Mapped[int] = mapped_column(SmallInteger, ForeignKey("departments.id"))

    depart: Mapped["Department"] = relationship(back_populates="groups")
    spec: Mapped["Speciality"] = relationship(back_populates="group")
    # curator: Mapped["CuratorsGroups"] = relationship(back_populates="groups")
    curator: Mapped["Curator"] = relationship(
        "Curator", secondary=CuratorsGroups, back_populates="groups"
    )
    students: Mapped[List["Student"]] = relationship(back_populates="group")

    refs: list[str] = [
        "students",
    ]

    field_names: dict = {
        "id": "Номер",
        "formation_year": "Год формирования",
        "study_year": "Год обучения",
        "head_of_group_id": "Номер зачетки старосты",
        "speciality_code": "Код специальности",
        "depart_id": "Номер кафедры",
    }

    linked_fields: dict = {"Curator": "curator"}

    link_types: dict = {"curator": "many_to_one"}

    id_attr = "id"

    def get_id(self):
        return self.id

    def __repr__(self) -> str:
        return f"Group(id={self.id!r}, \
        formation_year={self.formation_year!r}, \
        study_year={self.study_year!r}, \
        head_of_group_id={self.head_of_group_id!r}, \
        speciality_code={self.speciality_code!r}, \
        depart_id={self.depart_id!r})"

    have_name = True

    def get_name(self):
        return f"{self.id}"


class Student(Base):
    __tablename__ = "students"

    desc = "Студент"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(63))
    payment_basis: Mapped[str] = mapped_column(String(11))
    living_address: Mapped[str] = mapped_column(String(127))
    inn: Mapped[int] = mapped_column(BigInteger)
    email: Mapped[str] = mapped_column(String(320))
    phone_number: Mapped[int] = mapped_column(BigInteger)
    phone_number_parent_1: Mapped[int] = mapped_column(BigInteger)
    phone_number_parent_2: Mapped[int] = mapped_column(BigInteger)
    role_in_group: Mapped[str] = mapped_column(String(12))
    type_of_scholarship: Mapped[str] = mapped_column(String(11))
    group_id: Mapped[int] = mapped_column(SmallInteger, ForeignKey("groups.id"))

    group: Mapped["Group"] = relationship(back_populates="students")
    passport: Mapped[List["Passport"]] = relationship(back_populates="student")

    refs: list[str] = [
        "passport",
    ]

    field_names: dict = {
        "id": "Номер зачётки",
        "full_name": "ФИО",
        "payment_basis": "Бюджетная основа",
        "living_address": "Адрес фактического проживания",
        "inn": "ИНН",
        "email": "Email",
        "phone_number": "Номер телефона",
        "phone_number_parent_1": "Телефон родителя 1",
        "phone_number_parent_2": "Телефон родителя 2",
        "role_in_group": "Роль в группе",
        "type_of_scholarship": "Вид стипендии",
        "group_id": "Номер группы",
    }

    have_name = True

    id_attr = "id"

    def get_id(self):
        return self.id

    def get_name(self):
        return f"{self.full_name}"


class Passport(Base):
    __tablename__ = "passport_data"

    desc = "Паспортные данные"

    document_number: Mapped[int] = mapped_column(Integer, primary_key=True)
    issue_date = mapped_column(Date, primary_key=True)
    series: Mapped[int] = mapped_column(SmallInteger)
    depart_code: Mapped[int] = mapped_column(Integer)
    registration_address: Mapped[str] = mapped_column(String(127))
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id"))

    student: Mapped["Student"] = relationship(back_populates="passport")

    refs = []

    field_names: dict = {
        "document_number": "Номер",
        "issue_date": "Дата выдачи",
        "series": "Серия",
        "depart_code": "Код подразделения",
        "registration_address": "Адрес регистрации",
        "student_id": "Номер зачётки",
    }

    id_attr = "document_number"
    id = synonym("document_number")

    def get_id(self):
        return self.document_number

    have_name = False

    def get_values(self):
        return [
            f"Номер: {self.document_number}",
            f"Серия: {self.series}",
            f"Дата выдачи: {self.issue_date}",
            f"Код подразделения: {self.depart_code}",
            f"Адрес регистрации: {self.registration_address}",
        ]
