from typing import List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

Base = declarative_base()

class Faculty(Base):
    __tablename__ = "faculties"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255))
    address: Mapped[str] = mapped_column(String(511))
    deans_room_num: Mapped[int]
    dean_full_name: Mapped[str] = mapped_column(String(255))

    departments: Mapped[List["Department"]] = relationship(back_populates="faculty", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, full_name={self.full_name!r}, address={self.address!r}, deans_room_num={self.deans_room_num!r}, dean_full_name={self.dean_full_name!r})"


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255))
    address: Mapped[str] = mapped_column(String(511))
    depart_room_num: Mapped[int]
    head_of_depart_full_name: Mapped[str] = mapped_column(String(255))
    faculty_id: Mapped[int] = mapped_column(ForeignKey('faculties.id'))

    faculty: Mapped["Faculty"] = relationship(back_populates="departments")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, full_name={self.full_name!r}, address={self.address!r}, depart_room_num={self.deans_room_num!r}, head_of_depart_full_name={self.dean_full_name!r}, faculty_id={self.faculty_id!r})"


class Curator:
    __tablename__ = "curators"

    personnel_number: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255))
    job_title: Mapped[str] = mapped_column(String(127))
    academic_degree: Mapped[str] = mapped_column(String(31))
    phone_number: Mapped[str] = mapped_column(String(12))
    depart_id: Mapped[int] = mapped_column(ForeignKey('departments.id'))


class Speciality:
    __tablename__ = "specialties"


class Groups:
    __tablename__ = "groups"


class CuratorsGroups:
    __tablename__ = "curators_groups"


class Student:
    __tablename__ = "students"


class Document:
    __tablename__ = "documents"