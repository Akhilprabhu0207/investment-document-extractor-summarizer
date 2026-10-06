import argparse, json
from pathlib import Path
from .extractor import extract_pdf
from .validator import validate

def main():
    p=argparse.ArgumentParser(); p.add_argument('pdf'); p.add_argument('--output',required=True); p.add_argument('--summarize',action='store_true'); a=p.parse_args()
    data=extract_pdf(a.pdf); data['validation']=validate(data)
    if a.summarize:
        from .summarizer import OpenAISummarizer
        data['summary']=OpenAISummarizer().summarize(data)
    Path(a.output).parent.mkdir(parents=True,exist_ok=True); Path(a.output).write_text(json.dumps(data,indent=2),encoding='utf-8'); print(f'Wrote {a.output}')

if __name__ == "__main__": main()
