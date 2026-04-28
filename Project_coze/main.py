from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from cozepy import Coze, TokenAuth, COZE_CN_BASE_URL, Message, ChatEventType
from pydantic import BaseModel
from pathlib import Path
import json

app = FastAPI()

music_dir = Path(__file__).parent / 'music'
if music_dir.exists():
    app.mount('/music', StaticFiles(directory=str(music_dir)), name='music')

API_KEY = 'pat_ML6c35gSfrMlgozQAiAjrUzE4zMi4AdF1LBwa8dyAOc8SYT3tah6i0TU4VNI0g5R'
BOT_ID = '7633418462655709219'

coze = Coze(auth=TokenAuth(API_KEY), base_url=COZE_CN_BASE_URL)


class ChatRequest(BaseModel):
    message: str
    user_id: str = 'web_user'
    conversation_id: str | None = None


@app.get('/')
async def index():
    html_path = Path(__file__).parent / 'index.html'
    return HTMLResponse(content=html_path.read_text(encoding='utf-8'))


@app.post('/api/chat')
async def chat(req: ChatRequest):
    def generate():
        messages = [Message.build_user_question_text(req.message)]
        kwargs = dict(
            bot_id=BOT_ID,
            user_id=req.user_id,
            additional_messages=messages,
        )
        if req.conversation_id:
            kwargs['conversation_id'] = req.conversation_id

        try:
            result_stream = coze.chat.stream(**kwargs)
            conv_id = None
            for chunk in result_stream:
                if chunk.event == ChatEventType.CONVERSATION_CHAT_CREATED:
                    if chunk.chat and chunk.chat.conversation_id:
                        conv_id = chunk.chat.conversation_id
                        yield f"data: {json.dumps({'type': 'conversation', 'conversation_id': conv_id}, ensure_ascii=False)}\n\n"
                elif chunk.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
                    yield f"data: {json.dumps({'type': 'delta', 'content': chunk.message.content}, ensure_ascii=False)}\n\n"
                elif chunk.event == ChatEventType.CONVERSATION_CHAT_COMPLETED:
                    if chunk.chat and chunk.chat.conversation_id:
                        conv_id = chunk.chat.conversation_id
                    yield f"data: {json.dumps({'type': 'done', 'conversation_id': conv_id}, ensure_ascii=False)}\n\n"
                    break
                elif chunk.event == ChatEventType.CONVERSATION_CHAT_FAILED:
                    msg = '对话失败，请重试'
                    if chunk.chat and chunk.chat.last_error:
                        msg = str(chunk.chat.last_error)
                    yield f"data: {json.dumps({'type': 'error', 'message': msg}, ensure_ascii=False)}\n\n"
                    break
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)}, ensure_ascii=False)}\n\n"

    return StreamingResponse(generate(), media_type='text/event-stream')


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
