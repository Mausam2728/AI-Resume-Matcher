from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# AI Model load kar rahe hain jo words ka matlab samajhta hai
model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_match_score(resume_text, job_description):
    # AI model dono texts ko mathematical numbers (vectors) me badlega
    embeddings = model.encode([resume_text, job_description])
    
    # Cosine similarity dono ke beech ka common match score nikalta hai (0 se 1 ke beech)
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    
    # Score ko percentage (0 se 100) me badalna
    percentage_score = round(float(similarity) * 100, 2)
    return percentage_score