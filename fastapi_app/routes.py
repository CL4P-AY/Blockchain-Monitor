from datetime import timedelta

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from fastapi import HTTPException, status, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from app.models import Block, Provider
from .auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from .schemas import BlockSchema, UserSchema, ProviderSchema

router = APIRouter()


@router.post("/register", response_model=UserSchema)
def register(username: str, password: str):
    if User.objects.filter(username=username).exists():
        raise HTTPException(status_code=400, detail="Username already exists")
    user = User.objects.create_user(username=username, password=password)
    return UserSchema(username=user.username, id=user.id)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate(username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/providers", response_model=list[ProviderSchema])
def list_providers():
    providers = Provider.objects.all()
    return [ProviderSchema.model_validate(provider) for provider in providers]


@router.get("/blocks", response_model=list[BlockSchema])
def list_blocks(
    currency: str = None, provider: str = None, page: int = 1, per_page: int = 10
):
    blocks = Block.objects.all().order_by("-stored_at")
    if currency:
        blocks = blocks.filter(currency__name__iexact=currency)
    if provider:
        blocks = blocks.filter(provider__name__iexact=provider)

    paginator = Paginator(blocks, per_page)
    try:
        page_obj = paginator.page(page)
    except Exception:
        raise HTTPException(status_code=404, detail="Page not found")

    return [BlockSchema.from_orm(block) for block in page_obj.object_list]


@router.get("/blocks/{block_id}", response_model=BlockSchema)
def get_block_by_id(block_id: int):
    try:
        block = Block.objects.get(id=block_id)
    except Block.DoesNotExist:
        raise HTTPException(status_code=404, detail="Block not found")
    return BlockSchema.from_orm(block)


@router.get("/blocks/{currency_name}/{block_number}", response_model=BlockSchema)
def get_block_by_currency_and_number(currency_name: str, block_number: str):
    try:
        block = Block.objects.get(
            currency__name__iexact=currency_name, block_number=block_number
        )
    except Block.DoesNotExist:
        raise HTTPException(status_code=404, detail="Block not found")
    return BlockSchema.from_orm(block)
