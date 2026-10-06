import os
class LLMUnavailable(RuntimeError): pass
class OpenAISummarizer:
 def __init__(self,model=None): self.model=model or os.getenv('OPENAI_MODEL','gpt-5')
 def summarize(self,data):
  if not os.getenv('OPENAI_API_KEY'): raise LLMUnavailable('OPENAI_API_KEY is not set')
  from openai import OpenAI
  r=OpenAI().responses.create(model=self.model,input='Summarize this investment fund fact sheet. Use only supplied content; do not invent numbers.\n\n'+str(data),store=False)
  return r.output_text.strip()
