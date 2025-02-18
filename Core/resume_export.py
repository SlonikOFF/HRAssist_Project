import requests

prompt_1_previous_jobs = """<s>[INST] <<SYS>> 
 
You are the system who does not tell the user ANYTHING except the answer. 
 
YOU MUST FOLLOW THE ANSWER PATTERN VERY PRECISELY: "Information: [topic 1], [topic 2], [topic 3]". 
 
ALWAYS answer exactly what is asked of you and don't take liberties. All answers must be sequentially written to the list in one line in the order specified by the user. IT IS VERY IMPORTANT THAT EACH PART OF THE ANSWER SHOULD BE ENCLOSED IN QUOTATION MARKS AND SHOULD NOT HAVE A TITLE. 
 
EACH TOPIC SHOULD BE SORTED BY IMPORTANCE. 
 
IF YOU THINK THAT YOU CANNOT FIND THE NECESSARY INFORMATION ON ONE OF THE TOPICS, BE SURE TO WRITE IN "null". FOLLOW THE USER'S REQUEST EXACTLY. 
 
<</SYS>> 
"""

prompt_2_previous_jobs = """
Question: Summarize the text, find in it all the words from 3 topics: "обязанности" (NO MAXIMUM), "Стек" (MAXIMUM OF 5 LINES), "Проекты" (MAXIMUM OF 3 LINES. WRITE DOWN ONLY THE NAMES OF IT TECHNOLOGIES). [/INST]"""

prompt_1_about = """<s>[INST] <<SYS>> 
 
You are the system who does not tell the user ANYTHING except the answer. 
 
YOU MUST FOLLOW THE ANSWER PATTERN VERY PRECISELY: "Information: [topic 1], [topic 2], [topic 3]". 
 
ALWAYS answer exactly what is asked of you and don't take liberties. All answers must be sequentially written to the list in one line in the order specified by the user. IT IS VERY IMPORTANT THAT EACH PART OF THE ANSWER SHOULD BE ENCLOSED IN QUOTATION MARKS AND SHOULD NOT HAVE A TITLE. 
 
EACH TOPIC SHOULD BE SORTED BY IMPORTANCE. 
 
IF YOU THINK THAT YOU CANNOT FIND THE NECESSARY INFORMATION ON ONE OF THE TOPICS, BE SURE TO WRITE IN "null". FOLLOW THE USER'S REQUEST EXACTLY. 
 
<</SYS>> 
"""

prompt_2_about = """
Question: Summarize the text, find in it all the words from 3 topics: "Чем занимается" (NO MAXIMUM), "Сертификаты" (MAXIMUM OF 5 LINES), "дополнительная информация" (MAXIMUM OF 3 LINES. WRITE DOWN ONLY THE NAMES OF IT TECHNOLOGIES). [/INST]"""


def call_llama_api(message_to_model):
    invoke_url = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/functions/e0bb7fb9-5333-4a27-8534-c6288f921d3f"
    fetch_url_format = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/status/"

    headers = {
        "Authorization": "Bearer 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",
        "Accept": "application/json",
    }

    payload = {
        "messages": [
            {
                "content": message_to_model,
                "role": "user"
            }
        ],
        "temperature": 0.2,
        "top_p": 0.2,
        "max_tokens": 1024,
        "seed": 42,
        "stream": False
    }

    session = requests.Session()

    response = session.post(invoke_url, headers=headers, json=payload)

    while response.status_code == 202:
        request_id = response.headers.get("NVCF-REQID")
        fetch_url = fetch_url_format + request_id
        response = session.get(fetch_url, headers=headers)

    response.raise_for_status()
    response_body = response.json()
    return response_body


def ai_parse_about(description):
    message_inside = prompt_1_about + "Context: "+ description + prompt_2_about
    response_resume = call_llama_api(message_inside)
    return response_resume["choices"][0]["message"]["content"]