from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from server.auth import get_user
from server.database import db


###########################
#         SCHEMAS         #
###########################
class TaskOutput(BaseModel):
    # id task done due
    id: str
    task: str
    done: bool
    due: datetime


class TaskCreateInput(BaseModel):
    # task
    # optional: done due
    task: str
    done: bool | None
    due: datetime | None


class TaskUpdateInput(BaseModel):
    # optional: task done due
    task: str | None
    done: bool | None
    due: datetime | None


###########################
#         ROUTES          #
###########################
task_router = APIRouter(prefix="/tasks", tags=["Task"])


# task list
@task_router.get(
    "/",
    response_model=list[TaskOutput],
)
async def task_list(user=Depends(get_user)):
    tasks = await db.task.find_many(where={"user_id": user.id})
    return tasks


# task create
@task_router.post(
    "/",
    response_model=TaskOutput,
    status_code=201,
)
async def create_task(data: TaskCreateInput, user=Depends(get_user)):
    data_dict = data.dict(exclude_unset=True)
    data_dict["user_id"] = user.id
    task = await db.task.create(data=data_dict)
    return task


# task detail
@task_router.get(
    "/{id}",
    response_model=TaskOutput,
    responses={404: {}},
)
async def task_detail(id: int, user=Depends(get_user)):
    task = await db.task.find_first(where={"id": id, "user_id": user.id})
    if task:
        return task
    else:
        raise HTTPException(status_code=404, detail="Task not found")


# task update
@task_router.put(
    "/{id}",
    response_model=TaskOutput,
    responses={404: {}},
    status_code=202,
)
async def update_task(id: int, data: TaskUpdateInput, user=Depends(get_user)):
    task = await db.task.find_first(where={"id": id, "user_id": user.id})
    if task:
        task = await db.task.update(
            data=data.dict(exclude_unset=True), where={"id": id}
        )
        return task
    else:
        raise HTTPException(status_code=404, detail="Task not found")


# task delete
@task_router.delete(
    "/{id}",
    responses={404: {}},
    status_code=204,
)
async def delete_task(id: int, user=Depends(get_user)):
    num_deleted = await db.task.delete_many(where={"id": id, "user_id": user.id})
    if num_deleted == 0:
        raise HTTPException(status_code=404, detail="Task not found")
