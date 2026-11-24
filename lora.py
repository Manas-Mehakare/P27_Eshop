"""Real CPU LoRA experiment, separate from the production Groq chatbot."""
import json, torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig, get_peft_model
from core import STORE
MODEL='HuggingFaceTB/SmolLM2-135M-Instruct'
TRAIN=[('Where is ORD001?','Shipped'),('Status of ORD002?','Delivered'),('Track ORD003','Processing'),('What is the return window?','7 days'),('Can I return after 20 days?','No'),('Do you sell laptops?','HUMAN_HANDOFF'),('Track ORD999','HUMAN_HANDOFF'),('Price of mouse?','599')]
TEST=[('Has ORD001 been dispatched?','Shipped'),('Did ORD002 arrive?','Delivered'),('How many days do I have to return?','7 days'),('Can I return after 14 days?','No'),('Where is ORD888?','HUMAN_HANDOFF')]
def main():
    torch.manual_seed(7); torch.set_num_threads(4)
    tok=AutoTokenizer.from_pretrained(MODEL); tok.pad_token=tok.eos_token
    base=AutoModelForCausalLM.from_pretrained(MODEL)
    def prefix(q,examples=False):
        s='Answer briefly as store support. Store facts: '+json.dumps(STORE)+'\n'
        if examples: s+=''.join(f'Q: {x}\nA: {y}\n' for x,y in TRAIN)
        return s+f'Q: {q}\nA:'
    def predict(model,q,examples):
        model.eval(); x=tok(prefix(q,examples),return_tensors='pt');
        with torch.no_grad(): out=model.generate(**x,max_new_tokens=16,do_sample=False,pad_token_id=tok.eos_token_id)
        return tok.decode(out[0,x.input_ids.shape[1]:],skip_special_tokens=True).strip().split('\n')[0]
    few=[predict(base,q,True) for q,_ in TEST]
    model=get_peft_model(base,LoraConfig(r=4,lora_alpha=8,target_modules=['q_proj','v_proj'],task_type='CAUSAL_LM')); model.print_trainable_parameters(); model.train()
    opt=torch.optim.AdamW((p for p in model.parameters() if p.requires_grad),lr=0.0005)
    for epoch in range(5):
        total=0
        for q,a in TRAIN:
            p=prefix(q); x=tok(p+' '+a+tok.eos_token,return_tensors='pt'); labels=x.input_ids.clone(); labels[:,:len(tok(p).input_ids)]=-100
            opt.zero_grad(); loss=model(**x,labels=labels).loss; loss.backward(); opt.step(); total+=loss.item()
        print('Epoch',epoch+1,'loss',total/len(TRAIN))
    model.save_pretrained('lora_adapter'); tok.save_pretrained('lora_adapter')
    rows=[]
    for (q,expected),f in zip(TEST,few):
        l=predict(model,q,False); rows.append(dict(question=q,expected=expected,few_shot=f,lora=l,few_shot_match=expected.lower() in f.lower(),lora_match=expected.lower() in l.lower()))
    with open('lora_results.json','w') as f: json.dump(rows,f,indent=2)
    print(json.dumps(rows,indent=2)); print('Keyword matches:',sum(r['few_shot_match'] for r in rows),sum(r['lora_match'] for r in rows),'of',len(rows))
if __name__=='__main__': main()
