import os
class LLMUnavailable(RuntimeError): pass
class OpenAISummarizer:
    def __init__(self, model: str | None=None): self.model=model or os.getenv('OPENAI_MODEL','gpt-5')
    def summarize(self, data: dict) -> str:
        key=os.getenv('OPENAI_API_KEY')
        if not key: raise LLMUnavailable('OPENAI_API_KEY is not set')
        from openai import OpenAI
        client=OpenAI(api_key=key)
        prompt=('Summarize this investment fund fact sheet for a research analyst. Use only the supplied extracted content. Do not invent numbers. Mention strategy, asset class, fees and holdings when present. If a field is missing, say it is not stated.\n\nStructured fields:\n'+str(data)+'\n\nRaw extracted text:\n'+data.get('raw_text',''))
        response=client.responses.create(model=self.model,input=prompt,store=False)
        return response.output_text.strip()
