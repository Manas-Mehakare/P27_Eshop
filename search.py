from core import PRODUCTS, ROOT
from functools import lru_cache
from PIL import Image
@lru_cache(maxsize=1)
def text_index():
    from sentence_transformers import SentenceTransformer
    model=SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    return model,model.encode([p['name']+' '+p['description'] for p in PRODUCTS],normalize_embeddings=True)
def semantic(query):
    model, vectors=text_index(); scores=vectors @ model.encode(query,normalize_embeddings=True)
    i=int(scores.argmax()); return [PRODUCTS[i]] if scores[i]>=0.35 else []
@lru_cache(maxsize=1)
def image_index():
    from sentence_transformers import SentenceTransformer
    model=SentenceTransformer('sentence-transformers/clip-ViT-B-32')
    imgs=[Image.open(ROOT/'images'/f"{p['id']}.png").convert('RGB') for p in PRODUCTS]
    return model,model.encode(imgs,normalize_embeddings=True)
def photo_search(image):
    model,vectors=image_index(); scores=vectors @ model.encode(image.convert('RGB'),normalize_embeddings=True)
    i=int(scores.argmax()); return PRODUCTS[i],float(scores[i])
