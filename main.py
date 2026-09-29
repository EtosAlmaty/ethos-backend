from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import openai

app = FastAPI(title="Ethos TMA Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация API клиента (ключ подтягивается из защищенных настроек Render)
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Системный промпт с базами знаний по КПТ и стоицизму
ETHOS_SYSTEM_PROMPT = (
    "Ты — «Этос», умный наставник и персональный проводник на стыке когнитивно-поведенческой "
    "терапии (КПТ) и классического стоицизма. Твой стиль общения глубокий, рациональный, эмпатичный, "
    "но без стерильного ханжества. Если пользователь общается эмоционально или использует крепкое словцо, "
    "ты можешь органично адаптироваться под его стиль для создания доверительного контакта. "
    "Твоя задача — вычленять когнитивные искажения (катастрофизацию, долженствование и др.), "
    "опираться на разум, фокус и возвращать пользователя к зоне его личного контроля "
    "(в стиле Марка Аврелия и Эпиктета), используя философию и мудрость классических текстов."
)

class UserMessage(BaseModel):
    message: str
    user_id: str = "default_user"

@app.post("/api/chat")
async def chat_with_ethos(data: UserMessage):
    try:
        # Отправляем запрос к языковой модели с учетом промпта Этоса
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": ETHOS_SYSTEM_PROMPT},
                {"role": "user", "content": data.message}
            ],
            temperature=0.7,
        )
        ai_response = response.choices[0].message.content
    except Exception as e:
        ai_response = f"Разум столкнулся с технической помехой: {e}. Но фокус внимания остается на тебе."

    return {
        "status": "success",
        "response": ai_response
    }
