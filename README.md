# P27 — E-Shop Customer Support Chatbot
Minimal syllabus demonstration with Python, Streamlit and Groq. Five mock products and three mock orders. No database or real customer data.

## Run (Windows PowerShell)
Use Python 3.11 and extract the ZIP. Open a terminal in the extracted project folder.

```powershell
py -3.11 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
.venv\Scripts\python.exe -m streamlit run app.py
```
Paste your Groq key in `.env`, or enter it in the sidebar. Obtain a key at https://console.groq.com/keys. The first semantic/photo search downloads pretrained models. Internet is required for Groq, model downloads and gTTS. Use mock data only. CPU supported; model downloads and LoRA require additional disk space and RAM.

## Syllabus mapping
- U1: `core.py`: polite system prompt, three few-shot examples, fixed policy and hand-off.
- U2: `lora.py`: same small base model evaluated with few-shot examples before real LoRA training; five held-out questions afterward. Keyword match is a rough metric; inspect results manually. Groq is the main app, not the LoRA training host.
- U3: `search.py`: MiniLM Sentence-BERT and CLIP ViT-B/32 cosine search; supplied images are synthetic product illustrations, not real product photos. Similarity thresholds are heuristic, not calibrated.
- U4: `media.py`: generates template-based PNG product banners with verified catalogue values; gTTS reply audio. This is programmatic image generation, not a diffusion model.
- U5: `core.py`: verified prices rendered by Python, no arbitrary LLM text displayed, basic regex PII masking (email/phone/card; not comprehensive), reason-only refusal log. Human hand-off is a simulated message, not live ticket creation. The Groq response is used as an uncertainty gate; verified facts are rendered deterministically for safety.

## Demonstrate / evaluate
```powershell
.venv\Scripts\python.exe lora.py
.venv\Scripts\python.exe evaluate.py
.venv\Scripts\python.exe -m unittest test_core
```
`lora.py` saves adapter and `lora_results.json`. `evaluate.py` runs ten cases and generates `evaluation.csv` with correct/partly/wrong labels and a score. Automatic checks are approximate; verify meaning manually. To demonstrate CLIP upload `images/P03.png`; for semantic search try “Suggest something for typing”.

## Validation status
Local unit tests use a mock Groq client. Live API, pretrained search, TTS, LoRA training and full evaluation require dependencies/network and were not executed when packaging. No fabricated scores or trained weights included. Never commit your `.env` file.
