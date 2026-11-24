import csv, os
from core import answer, redact, ROOT
from search import semantic, photo_search
from media import banner,speech
from PIL import Image
from dotenv import load_dotenv
from groq import Groq

def main():
    load_dotenv(); client=Groq(api_key=os.environ['GROQ_API_KEY'])
    tests=[('Price of headphones?',lambda:answer('Price of headphones?',client,semantic),['1,499']),('Product under 1000',lambda:answer('Product under 1000',client,semantic),['599','999']),('Where is ORD001?',lambda:answer('Where is ORD001?',client),['Shipped']),('Where is ORD999?',lambda:answer('Where is ORD999?',client),['HUMAN_HANDOFF']),('Return after 3 days?',lambda:answer('Return after 3 days?',client),['7 days','Undamaged']),('Return after 15 days?',lambda:answer('Return after 15 days?',client),['No.','7 days']),('Find this item (mouse image)',lambda:photo_search(Image.open(ROOT/'images/P03.png'))[0]['name'],['Mouse']),('Generate smartwatch banner',lambda:'PNG generated' if banner(__import__('core').PRODUCTS[1]).startswith(b'\x89PNG') else '', ['PNG generated']),('Read reply aloud',lambda:'Audio generated' if len(speech('Your order has shipped.'))>100 else '', ['Audio generated']),('My email is test@example.com. Help.',lambda:redact('My email is test@example.com. Help.')+' '+answer('My email is test@example.com. Help.',client),['[EMAIL]','HUMAN_HANDOFF'])]
    rows=[]
    for q,fn,expected in tests:
        try:
            result=fn(); n=sum(x.lower() in result.lower() for x in expected); grade='Correct' if n==len(expected) else 'Partly' if n else 'Wrong'
            if 'test@example.com' in result: grade='Wrong'
        except Exception as e: result=type(e).__name__; grade='Wrong'
        rows.append([q,'; '.join(expected),result,grade]); print(q,grade)
    with open('evaluation.csv','w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f); w.writerow(['Query','Expected','Actual','Grade']); w.writerows(rows)
    print('Score:',sum({'Correct':1,'Partly':0.5,'Wrong':0}[r[-1]] for r in rows),'/ 10')
if __name__=='__main__': main()
