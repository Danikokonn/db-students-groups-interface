from typing import List
from sqlalchemy import String, ForeignKey, LargeBinary, BigInteger, SmallInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Faculty(Base):
    __tablename__ = "faculties"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255))
    address: Mapped[str] = mapped_column(String(511))
    deans_room_num: Mapped[int] = mapped_column(SmallInteger)
    dean_full_name: Mapped[str] = mapped_column(String(255))

    departments: Mapped[List["Department"]] = relationship(back_populates="faculty", cascade="all, delete-orphan")

    refs: dict = {
        "departments": "departments"
    }

    fields: dict = {
        "id": id,
    }

    def get_id(self):
        return self.id

    def __repr__(self) -> str:
        return f"Faculty(id={self.id!r}, full_name={self.full_name!r}, address={self.address!r}, deans_room_num={self.deans_room_num!r}, dean_full_name={self.dean_full_name!r})"

    def get_name(self):
        return f"{self.full_name}"

class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255))
    address: Mapped[str] = mapped_column(String(511))
    depart_room_num: Mapped[int] = mapped_column(SmallInteger)
    head_of_depart_full_name: Mapped[str] = mapped_column(String(255))
    faculty_id: Mapped[int] = mapped_column(SmallInteger, ForeignKey('faculties.id'))

    faculty: Mapped["Faculty"] = relationship(back_populates="departments")
    curators: Mapped[List["Curator"]] = relationship(back_populates="depart")
    groups: Mapped[List["Group"]] = relationship(back_populates="depart")

    refs: dict = {
        "curators": "curators",
        "groups": "groups"
    }

    fields: dict = {
        "id": id,
    }

    def get_id(self):
        return self.id

    def __repr__(self) -> str:
        return f"Department(id={self.id!r}, full_name={self.full_name!r}, address={self.address!r}, depart_room_num={self.depart_room_num!r}, head_of_depart_full_name={self.head_of_depart_full_name!r}, faculty_id={self.faculty_id!r})"

    def get_name(self):
        return f"{self.full_name}"
    

class Curator(Base):
    __tablename__ = "curators"

    personnel_number: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255))
    job_title: Mapped[str] = mapped_column(String(127))
    academic_degree: Mapped[str] = mapped_column(String(31))
    phone_number: Mapped[str] = mapped_column(String(12))
    depart_id: Mapped[int] = mapped_column(SmallInteger,ForeignKey('departments.id'))

    depart: Mapped["Department"] = relationship(back_populates="curators")
    groups: Mapped[List["CuratorsGroups"]] = relationship(back_populates="curator")

    refs: dict = {
        "groups": "groups"
    }

    fields: dict = {
        "id": personnel_number,
    }

    def get_id(self):
        return self.personnel_number

    def __repr__(self) -> str:
        return f"Curator(personnel_number={self.personnel_number!r}, full_name={self.full_name!r}, job_title={self.job_title!r}, academic_degree={self.academic_degree!r}, phone_number={self.phone_number!r}, depart_id={self.depart_id!r})"


class Speciality(Base):
    __tablename__ = "specialties"

    code: Mapped[str] = mapped_column(String(12), primary_key=True)
    full_name: Mapped[str] = mapped_column(String(511))

    group: Mapped["Group"] = relationship(back_populates="spec")

    def get_id(self):
        return self.code
    
    fields: dict = {
        "id": code,
    }

    def __repr__(self) -> str:
        return f"Speciality(code={self.code!r}, full_name={self.full_name!r})"


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    formation_year: Mapped[int] = mapped_column(SmallInteger)
    study_year: Mapped[int] = mapped_column(SmallInteger)
    head_of_group_id: Mapped[int] = mapped_column(Integer)
    speciality_code: Mapped[str] = mapped_column(String(12), ForeignKey('specialties.code'))
    depart_id: Mapped[int] = mapped_column(SmallInteger, ForeignKey('departments.id'))

    depart: Mapped["Department"] = relationship(back_populates="groups")
    spec: Mapped["Speciality"] = relationship(back_populates="group")
    curator: Mapped["CuratorsGroups"] = relationship(back_populates="groups")
    students: Mapped[List["Student"]] = relationship(back_populates="group")

    refs: dict = {
        "students": "students"
    }

    fields: dict = {
        "id": id,
    }

    def get_id(self):
        return self.id

    def __repr__(self) -> str:
        return f"Group(id={self.id!r}, formation_year={self.formation_year!r}, study_year={self.study_year!r}, head_of_group_id={self.head_of_group_id!r}, speciality_code={self.speciality_code!r}, depart_id={self.depart_id!r})"


class CuratorsGroups(Base):
    __tablename__ = "curators_groups"

    personnel_number: Mapped[int] = mapped_column(SmallInteger, ForeignKey('curators.personnel_number'), primary_key=True)
    group_id: Mapped[int] = mapped_column(SmallInteger, ForeignKey('groups.id'), primary_key=True)

    groups: Mapped[List["Group"]] = relationship(back_populates="curator")
    curator: Mapped["Curator"] = relationship(back_populates="groups")

    refs: dict = {
        "groups": groups
    }



class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255))
    payment_basis: Mapped[str] = mapped_column(String(31))
    living_address: Mapped[str] = mapped_column(String(511))
    photo = mapped_column(LargeBinary)
    phone_number: Mapped[str] = mapped_column(String(12))
    phone_number_parent_1: Mapped[str] = mapped_column(String(12))
    phone_number_parent_2: Mapped[str] = mapped_column(String(12))
    role_in_group: Mapped[str] = mapped_column(String(31))
    type_of_scholarship: Mapped[str] = mapped_column(String(31))
    group_id: Mapped[int] = mapped_column(SmallInteger, ForeignKey('groups.id'))

    group: Mapped["Group"] = relationship(back_populates="students")
    documents: Mapped[List["Document"]] = relationship(back_populates="student")
    
    def get_id(self):
        return self.id

    refs: dict = {
        "documents": "documents"
    }

    fields: dict = {
        "id": id,
    }


class Document(Base):
    __tablename__ = "documents"

    document_number: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    doc_type: Mapped[str] = mapped_column(String(31))
    series: Mapped[int] = mapped_column(SmallInteger)
    registration_address: Mapped[str] = mapped_column(String(511))
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey('students.id'))

    student: Mapped["Student"] = relationship(back_populates="documents")

    def get_id(self):
        return self.document_number
    
    fields: dict = {
        "id": document_number,
    }