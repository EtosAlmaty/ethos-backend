from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI(title="Ethos TMA Backend")

# Разрешаем запросы из нашего фронтенда
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


# Системный промпт ИИ-наставника (КПТ + Стоицизм + адаптивный тон)
ETHOS_SYSTEM_PROMPT = (
	"Ты — «Этос», умный наставник и персональный проводник на стыке когнитивно-поведенческой "
	"терапии (КПТ) и классического стоицизма. Твой стиль общения глубокий, рациональный, эмпатичный, "
	"но без стерильного ханжества. Если пользователь общается эмоционально или использует крепкое словцо, "
	"ты можешь органично адаптироваться под его стиль для создания доверительного контакта. "
	"Твоя задача — вычленять когнитивные искажения, опираться на разум, фокус и возвращать пользователя "
	"к зоне его личного контроля (в стиле Марка Аврелия и Эпиктета), используя историю его памяти."
)


class UserMessage(BaseModel):
	message: str
	user_id: str = "default_user"


@app.post("/api/chat")
async def chat_with_ethos(data: UserMessage):
	# Здесь в будущем мы подключим вызов к языковой модели (LLM)
	# с учетом системного промпта и базы долгосрочной памяти пользователя.
	user_text = data.message

	# Заглушка интеллектуального ответа для проверки связи
	ai_response = (
		f"Разум зафиксировал твой запрос: «{user_text}». "
		"Давай посмотрим на эту ситуацию через призму стоицизма: что здесь зависит от тебя, а что нет?"
	)

	return {
		"status": "success",
		"response": ai_response,
	}


if __name__ == "__main__":
	import uvicorn

	uvicorn.run(app, host="127.0.0.1", port=8000)
