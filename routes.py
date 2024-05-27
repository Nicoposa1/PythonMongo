from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import Book, BookUpdate

router = APIRouter()


@router.post("/", response_description="Create a new book", status_code=status.HTTP_201_CREATED, response_model=Book)
def create_book(request: Request, book: Book = Body(...)):
    book = jsonable_encoder(book)
    new_book = request.app.database["books"].insert_one(book)
    created_book = request.app.database["books"].find_one(
        {"_id": new_book.inserted_id}
    )

    return created_book

@router.get("/", response_description="List all books", response_model=List[Book])
def list_books(request: Request):
    books = request.app.database["books"].find()
    return books


@router.get("/{id}", response_description="Get a single book by id", response_model=Book)
def find_book(id: str, request: Request):
    if (book := request.app.database["books"].find_one({"_id": id})) is not None:
        return book
    raise HTTPException(
        status_code=404, detail=f"Book with id {id} not found")


@router.put("/{id}", response_description="Update a book", response_model=Book)
def update_book(id: str, request: Request, book: BookUpdate = Body(...)):
    book = {k: v for k, v in book.dict().items() if v is not None}
    if (len(book) >= 1):
        update_result = request.app.database["books"].update_one(
            {"_id": id}, {"$set": book}
        )
        if update_result.modified_count == 1:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {id} not found")

    if (
        existing_book := request.app.database["books"].find_one({"_id": id})
    ) is not None:
        return existing_book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Book with id {id} not found")


@router.delete("/{id}", response_description="Book with id {id} has been deleted")
def delete_book(id: str, request: Request):
    delete_result = request.app.database["books"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return {"status": f"Book with id {id} has been deleted successfully"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Book with id {id} not found")


