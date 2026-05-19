import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def _call_openai(messages):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
        max_tokens=450
    )
    return response.choices[0].message["content"].strip()

def generate_first_question(domain: str, cv_text: str) -> str:
    prompt = (
        "Aşağıdaki CV içeriğine göre mevcut alanda teknik bir mülakat sorusu üret.\n\n"
        f"Alan: {domain}\n\n"
        f"CV Özeti:\n{cv_text[:2000]}\n\n"
        "Kısa ve doğrudan bir soru sor. Adayın yanıtını sınayacak bir teknik senaryo olsun."
    )
    return _call_openai([
        {"role": "system", "content": "Sen deneyimli bir teknik mülakat yöneticisisin."},
        {"role": "user", "content": prompt},
    ])

def generate_followup_question(domain: str, cv_text: str, conversation: str, answer: str) -> str:
    prompt = (
        "Önceki mülakat konuşmasını ve adaya verilen yanıtı değerlendir.\n\n"
        f"Alan: {domain}\n\n"
        f"CV Özeti:\n{cv_text[:1500]}\n\n"
        f"Mülakat geçmişi:\n{conversation}\n\n"
        f"Adayın cevabı:\n{answer}\n\n"
        "Bu yanıt üzerinden mantıklı bir takip sorusu sor."
    )
    return _call_openai([
        {"role": "system", "content": "Sen sorular üretirken mantıklı takip soruları hazırlayan bir teknik mülakatçısın."},
        {"role": "user", "content": prompt},
    ])

def evaluate_answer(answer: str, question: str, cv_text: str) -> str:
    prompt = (
        "Aşağıdaki soruya verilen yanıtı değerlendir.\n\n"
        f"Soru:\n{question}\n\n"
        f"Yanıt:\n{answer}\n\n"
        f"CV Özeti:\n{cv_text[:1500]}\n\n"
        "Kısa bir değerlendirme yap ve adayın gelişmesi gereken iki teknik alanı belirt."
    )
    return _call_openai([
        {"role": "system", "content": "Sen aday cevaplarını yapıcı şekilde değerlendiren bir teknik koçsun."},
        {"role": "user", "content": prompt},
    ])

def generate_report(conversation: str, domain: str) -> str:
    prompt = (
        "Aşağıdaki teknik mülakat oturumunu değerlendir ve kısa bir rapor hazırla.\n\n"
        f"Alan: {domain}\n\n"
        f"Mülakat kaydı:\n{conversation}\n\n"
        "Güçlü yönleri ve geliştirilmesi gereken alanları belirt."
    )
    return _call_openai([
        {"role": "system", "content": "Sen teknik mülakat sonrası rapor yazan bir uzmanısın."},
        {"role": "user", "content": prompt},
    ])