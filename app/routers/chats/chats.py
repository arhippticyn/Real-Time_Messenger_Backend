from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...models.chat.chat import Chat, ChatType
from ...models.chat.chatParticant import ChatParticipant, ChatParticipantType
from ...models.user.user import User
from ...db.session import get_db
from ...schemas.chats.chats import ChatCreateGroup, ChatCreatePrivate
from ...services.token import get_current_user
from typing import List

router = APIRouter()

@router.post('/group')
async def create_group_chat(chat: ChatCreateGroup, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    chat_db = Chat(type=ChatType.group, title=chat.title)

    db.add(chat_db)
    await db.flush()


    db.add(ChatParticipant(chat_id=chat_db.id, user_id=user.id, role=ChatParticipantType.admin))

    for participant_id in chat.participants:
        db.add(ChatParticipant(chat_id=chat_db.id, user_id=participant_id, role=ChatParticipantType.base))

    await db.commit()
    await db.refresh(chat_db)

    return chat_db

@router.post('/private')
async def create_private_chat(chat: ChatCreatePrivate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    chat_db = Chat(type=ChatType.private, title=None)
    db.add(chat_db)
    await db.flush()

    db.add(ChatParticipant(chat_id=chat_db.id, user_id=user.id, role=ChatParticipantType.base))
    db.add(ChatParticipant(chat_id=chat_db.id, user_id=chat.user_id, role=ChatParticipantType.base))

    await db.commit()
    await db.refresh(chat_db)

    return chat_db

@router.get('')
async def get_all_chats(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    chats = (await db.execute(select(Chat).join(ChatParticipant, ChatParticipant.chat_id == Chat.id).where(ChatParticipant.user_id == user.id))).scalars().all()

    return chats

@router.get('/{chat_id}')
async def get_chat(chat_id: int, db: AsyncSession = Depends(get_db)):
    return (await db.execute(select(Chat).join(ChatParticipant).where(ChatParticipant.chat_id == chat_id))).scalars().first()