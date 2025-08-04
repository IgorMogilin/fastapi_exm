from fastapi import FastAPI, Path, Query

import uvicorn
from typing import Optional
from enum import Enum


app = FastAPI(docs_url='/swagger')


@app.get('/me', tags=['special methods'], summary='Приветствие автора')
def hello_author():
    return {'hello': 'author'}


class EducationLevel(str, Enum):
    SECONDARY = 'Среднее образование'
    SPECIAL = 'Среднее специальное образование'
    HIGHER = 'Высшее образование'


@app.get(
    '/{name}',
    tags=['common methods'],
    summary='Общее приветствие',
    response_description='Полная строка приветствия'
)
def greetings(
    *,
    name: str = Path(
        ...,
        min_lenght=2,
        max_linght=20,
        title='Полное имя',
        description='Можно вводить в любом регистре'

    ),
    surname: list[str] = Query(
        ...,
        min_length=2,
        max_length=5
    ),
    age: Optional[int] = Query(
        None,
        gt=4,
        le=99
    ),
    is_staff: bool = Query(
        False,
        alias='is-staff',
        include_in_schema=False
    ),
    education_level: Optional[EducationLevel] = None
) -> dict[str, str]:
    """
    Приветствие пользователя:

    - **name**: имя
    - **surname**: фамилия
    - **age**: возраст (опционально)
    - **education_level**: уровень образования (опционально)
    """
    result = ' '.join(name, surname)
    result.title()
    if age is not None:
        result += ', ' + str(age)
    if is_staff:
        result += ', сотрудник'
    if education_level is not None:
        result += ', ' + education_level.lower()
    return {'Hello': result}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
