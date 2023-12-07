from django.shortcuts import get_object_or_404
from ninja import Router
from .models import Reservable
from .schema import ReservableSchemaIn, ReservableSchemaOut, ReservableSchemaPatchIn

router = Router()

@router.get("/", response={200: list[ReservableSchemaOut]})
def get_reservables(request):
    reservables = Reservable.objects.all()

    return 200, reservables

@router.post("/", response={201: ReservableSchemaOut})
def post_reservable(request, payload: ReservableSchemaIn):
    reservable = Reservable.objects.create(**payload.dict())
    
    return 201, reservable

@router.get("/{int:reservable_id}/", response={200: ReservableSchemaOut})
def get_reservable_by_id(request, reservable_id: int):
    reservable = get_object_or_404(Reservable, id=reservable_id)
    
    return 200, reservable

@router.patch("/{int:reservable_id}/", response={200: ReservableSchemaOut})
def patch_reservable(request, payload: ReservableSchemaPatchIn, reservable_id: int):
    reservable = get_object_or_404(Reservable, id=reservable_id)

    for key, value in payload.dict(exclude_none=True, exclude_unset=True).items():
        setattr(reservable, key, value)
    reservable.save()
    
    return 200, reservable

@router.delete("/{int:reservable_id}/", response={204: None})
def delete_reservable(request, reservable_id: int):
    reservable = get_object_or_404(Reservable, id=reservable_id)

    reservable.delete()
    
    return 204, None