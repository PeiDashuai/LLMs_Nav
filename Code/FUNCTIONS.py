# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 12:11:42 2024

@author: 13419
"""
import json
import requests
from openai import OpenAI
from configs import system_prompt
from configs import get_gemma_2b_access_token
from configs import get_gemma_7b_access_token
from configs import get_Qianfan_Chinese_Llama_2_7B_access_token
from configs import get_Qianfan_Chinese_Llama_2_13B_v1_access_token
from configs import get_Qianfan_Chinese_Llama_2_70B_access_token
from configs import get_Meta_Llama_3_8B_Instruct_access_token
from configs import get_Meta_Llama_3_70B_Instruct_access_token
from configs import get_ERNIE_40_8K_access_token
from configs import get_gemma_7b_access_token
from zhipuai import ZhipuAI
from GetAccessToken import GetBaiduAccessToken
import dashscope
from dashscope import Generation

#在阿里大模型平台上获取API KEY
dashscope.api_key = ''

def ask_wenxinyiyan(question, options):
    #    #  question = question['question_text']
    ####   百度千帆大模型 ERNIE-4.0-8K
    #model_url = 'https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-4.0-8k-preview'
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + get_gemma_7b_access_token()
    prompt = f"{question}\nOptions:\n"
    for i, option in enumerate(options):
        prompt += f"{chr(65 + i)}. {option['choice_text']} \n"

    print(prompt)
    prompt += "Answer: "
    try:
        #url = "{}?access_token=".format(model_url) + access_token
        payload = json.dumps({
            "temperature": 0.5,
            "top_p": 0.7,
            "max_tokens": 100,
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        content = response.text
        content = json.loads(content)
        input_tokens = content["usage"]["prompt_tokens"]
        output_tokens = content["usage"]["total_tokens"] - content["usage"]["prompt_tokens"]
        resultContent = content["result"]
        
        return resultContent, input_tokens, output_tokens
    except Exception as e:
        print(e)
        return str(e)

def ask_chatgpt4o(question, options): 
    openai_client = OpenAI(api_key= "在openai获取apikey")
    prompt = f"{question}\nOptions:\n"
    for i, option in enumerate(options):
        prompt += f"{chr(65 + i)}. {option['choice_text']} \n"
        
    print(prompt)
    prompt += "Answer: "
    
    response = openai_client.chat.completions.create(
        model = "gpt-4o",
        messages = [{ 'role': 'system','content' : system_prompt},
                    {'role': 'user', 'content': prompt}],
        max_tokens = 100,
        top_p = 1.0,
        temperature = 0.0,
    )
    answer = response.choices[0].message.content.strip()
    total_tokens = response.usage.total_tokens
    output_tokens = response.usage.completion_tokens
    input_tokens = total_tokens - output_tokens
    
    return answer, input_tokens, output_tokens

def ask_chatgpt4(question, options):
    openai_client = OpenAI(api_key= "在openai获取apikey")
    prompt = f"{question}\nOptions:\n"
    for i, option in enumerate(options):
        prompt += f"{chr(65 + i)}. {option['choice_text']} \n"
        
    print(prompt)
    prompt += "Answer: "
    
    response = openai_client.chat.completions.create(

        model = "gpt-4",
        messages = [{ 'role': 'system','content' : system_prompt},
                    {'role': 'user', 'content': prompt}],
        max_tokens = 100,
        top_p = 1.0,
        temperature = 0.0,
    )

    answer = response.choices[0].message.content.strip()
    total_tokens = response.usage.total_tokens
    output_tokens = response.usage.completion_tokens
    input_tokens = total_tokens - output_tokens
    
    return answer, input_tokens, output_tokens

def ask_chatgpt3(question, options):
    openai_client = OpenAI(api_key= "在openai获取apikey")
    prompt = f"{question}\nOptions:\n"
    for i, option in enumerate(options):
        prompt += f"{chr(65 + i)}. {option['choice_text']} \n"
        
    print(prompt)
    prompt += "Answer: "
    
    response = openai_client.chat.completions.create(

        model = "gpt-3.5-turbo",
        messages = [{ 'role': 'system','content' : system_prompt},
                    {'role': 'user', 'content': prompt}],
        max_tokens = 100,
        top_p = 1.0,
        temperature = 0.0,
    )

    answer = response.choices[0].message.content.strip()
    total_tokens = response.usage.total_tokens
    output_tokens = response.usage.completion_tokens
    input_tokens = total_tokens - output_tokens
    
    return answer, input_tokens, output_tokens

def ask_glm3turbo(question, options):
    client_glm3turbo = ZhipuAI(api_key="填写您自己的APIKey，在zhipu ai模型平台上获取") # 
    prompt = f"{question}\nOptions:\n"
    for i, option in enumerate(options):
        prompt += f"{chr(65 + i)}. {option['choice_text']} \n"

    print(prompt)
    prompt += "Answer: "

    tools_web_search = [
        {
            "type": "web_search",
            "web_search": {
                "enable": False,
            }
        }
    ]
    response = client_glm3turbo.chat.completions.create(
        model="glm-3-turbo",  # 填写需要调用的模型名称
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
            ],
        tools=tools_web_search,
        top_p=0.7,
        temperature=0.5
    )
    output_tokens = response.usage.completion_tokens
    input_tokens = response.usage.prompt_tokens
    answer = str(response.choices[0].message.content.strip())
    
    return answer, input_tokens, output_tokens

def ask_glm4air(question, options):
    client_glm3turbo = ZhipuAI(api_key="填写您自己的APIKey，在zhipu ai模型平台上获取") # 填写您自己的APIKey
    print("Into glm-4air-turbo")
    
    prompt = f"{question}\nOptions:\n"
    for i, option in enumerate(options):
        prompt += f"{chr(65 + i)}. {option['choice_text']} \n"

    print(prompt)
    prompt += "Answer: "

    tools_web_search = [
        {
            "type": "web_search",
            "web_search": {
                "enable": False,
            }
        }
    ]
    response = client_glm3turbo.chat.completions.create(
        model="glm-4-air",  # 填写需要调用的模型名称
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
            ],
        tools=tools_web_search,
        top_p=0.7,
        temperature=0.5
    )
    output_tokens = response.usage.completion_tokens
    input_tokens = response.usage.prompt_tokens
    answer = str(response.choices[0].message.content.strip())
    
    return answer, input_tokens, output_tokens


def ask_tongyiqianwen(question, options):
    prompt = f"{question}\nOptions:\n"
    for i, option in enumerate(options):
        prompt += f"{chr(65 + i)}. {option['choice_text']} \n"

    print(prompt)
    prompt += "Answer: "
    messages = [{'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt}]

    response = Generation.call(model="qwen-turbo",
                               messages=messages,
                               # 将输出设置为"message"格式
                               result_format='message',
                               temperature = 0.0,
                               max_tokens = 100)
    input_tokens = response.usage["input_tokens"]
    output_tokens = response.usage["output_tokens"]
    data = response.output.choices
    resultContent = data[0].message['content']
    
    return resultContent, input_tokens, output_tokens

def ask_glm4(question, options):
    client_glm4 = OpenAI(
        api_key="填写您自己的APIKey，在zhipu ai模型平台上获取",
        base_url="https://open.bigmodel.cn/api/paas/v4/"
        ) 
    prompt = f"{question}\nOptions:\n"
    for i, option in enumerate(options):
        prompt += f"{chr(65 + i)}. {option['choice_text']} \n"
    print(prompt)
    prompt += "Answer: "
    tools_web_search = [
        {
            "type": "web_search",
            "web_search": {
                "enable": False,
            }
        }
    ]
    completion = client_glm4.chat.completions.create(
        model="glm-4", 
        messages=[    
            {"role": "system", "content": system_prompt},    
            {"role": "user", "content": prompt} 
        ],
        top_p=0.7,
        tools=tools_web_search,
        temperature=0.5
        ) 
    answer = str(completion.choices[0].message.content.strip())
    output_tokens = completion.usage.completion_tokens
    input_tokens = completion.usage.prompt_tokens
    
    return answer, input_tokens, output_tokens



def ask_llama3_8b(question, options):
    prompt = f"{question}\nOptions:\n"
    for i, option in enumerate(options):
        prompt += f"{chr(65 + i)}. {option['choice_text']} \n"

    print(prompt)
    prompt += "Answer: "
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/llama_3_8b?access_token=" + get_Meta_Llama_3_8B_Instruct_access_token()
    try:
        payload = json.dumps({
            "temperature": 0.5,
            "top_p": 0.7,
            "max_tokens": 100,
            #"system": system_prompt,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user","content": prompt}
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        content = response.text
        content = json.loads(content)
        input_tokens = content["usage"]["prompt_tokens"]
        output_tokens = content["usage"]["total_tokens"] - content["usage"]["prompt_tokens"]
        resultContent = content["result"]
        
        return resultContent, input_tokens, output_tokens
    except Exception as e:
        print(e)
        return str(e)

def ask_llama3_70b(question, options):
    prompt = f"{question}\nOptions:\n"
    for i, option in enumerate(options):
        prompt += f"{chr(65 + i)}. {option['choice_text']} \n"

    print(prompt)
    prompt += "Answer: "
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/llama_3_70b?access_token=" + get_Meta_Llama_3_70B_Instruct_access_token()
    try:
        payload = json.dumps({
            "temperature": 0.5,
            "top_p": 0.7,
            "max_tokens": 100,
            "system": system_prompt,
            "messages": [
                #{"role": "system", "content": system_prompt},
                {"role": "user","content": prompt}
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        content = response.text
        content = json.loads(content)
        input_tokens = content["usage"]["prompt_tokens"]
        output_tokens = content["usage"]["total_tokens"] - content["usage"]["prompt_tokens"]
        resultContent = content["result"]
        
        return resultContent, input_tokens, output_tokens
    except Exception as e:
        print(e)
        return str(e)


def ask_gemma_2b(question, options):

    url =  "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/gemma_2b_it?access_token=" + get_gemma_2b_access_token()
    prompt = f"{question}\nOptions:\n"
    for i, option in enumerate(options):
        prompt += f"{chr(65 + i)}. {option['choice_text']} \n"

    print(prompt)
    prompt += "Answer: "
    try:
        payload = json.dumps({
            "temperature": 0.5,
            "top_p": 0.7,
            "max_tokens": 100,
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        content = response.text
        content = json.loads(content)
        input_tokens = content["usage"]["prompt_tokens"]
        output_tokens = content["usage"]["total_tokens"] - content["usage"]["prompt_tokens"]
        resultContent = content["result"]
        
        return resultContent, input_tokens, output_tokens
    except Exception as e:
        print(e)
        return str(e)

def ask_gemma_7b(question, options):

    url =  "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/gemma_7b_it?access_token=" + get_gemma_7b_access_token()
    prompt = f"{question}\nOptions:\n"
    for i, option in enumerate(options):
        prompt += f"{chr(65 + i)}. {option['choice_text']} \n"

    print(prompt)
    prompt += "Answer: "
    try:
        payload = json.dumps({
            "temperature": 0.5,
            "top_p": 0.7,
            "max_tokens": 100,
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        content = response.text
        content = json.loads(content)
        input_tokens = content["usage"]["prompt_tokens"]
        output_tokens = content["usage"]["total_tokens"] - content["usage"]["prompt_tokens"]
        resultContent = content["result"]
        
        return resultContent, input_tokens, output_tokens
    except Exception as e:
        print(e)
        return str(e)



def ask_Qianfan_Chinese_Llama_2_7B(question, options):

    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/qianfan_chinese_llama_2_7b?access_token=" + get_Qianfan_Chinese_Llama_2_7B_access_token()
    prompt = f"{question}\nOptions:\n"
    for i, option in enumerate(options):
        prompt += f"{chr(65 + i)}. {option['choice_text']} \n"

    print(prompt)
    prompt += "Answer: "
    try:
        payload = json.dumps({
            "temperature": 0.5,
            "top_p": 0.7,
            "max_tokens": 100,
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        content = response.text
        content = json.loads(content)
        input_tokens = content["usage"]["prompt_tokens"]
        output_tokens = content["usage"]["total_tokens"] - content["usage"]["prompt_tokens"]
        resultContent = content["result"]
        
        return resultContent, input_tokens, output_tokens
    except Exception as e:
        print(e)
        return str(e)

def ask_Qianfan_Chinese_Llama_2_13B_v1(question, options):

    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/qianfan_chinese_llama_2_13b?access_token=" + get_Qianfan_Chinese_Llama_2_13B_v1_access_token()
    prompt = f"{question}\nOptions:\n"
    for i, option in enumerate(options):
        prompt += f"{chr(65 + i)}. {option['choice_text']} \n"

    print(prompt)
    prompt += "Answer: "
    try:
        payload = json.dumps({
            "temperature": 0.5,
            "top_p": 0.7,
            "max_output_tokens": 30,
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        content = response.text
        content = json.loads(content)
        input_tokens = content["usage"]["prompt_tokens"]
        output_tokens = content["usage"]["total_tokens"] - content["usage"]["prompt_tokens"]
        resultContent = content["result"]
        
        return resultContent, input_tokens, output_tokens
    except Exception as e:
        print(e)
        return str(e)

def ask_Qianfan_Chinese_Llama_2_70B(question, options):

    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/qianfan_chinese_llama_2_70b?access_token=" + get_Qianfan_Chinese_Llama_2_70B_access_token()
    prompt = f"{question}\nOptions:\n"
    for i, option in enumerate(options):
        prompt += f"{chr(65 + i)}. {option['choice_text']} \n"

    print(prompt)
    prompt += "Answer: "
    try:
        payload = json.dumps({
            "temperature": 0.5,
            "top_p": 0.7,
            "max_output_tokens": 10,
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        content = response.text
        content = json.loads(content)
        input_tokens = content["usage"]["prompt_tokens"]
        output_tokens = content["usage"]["total_tokens"] - content["usage"]["prompt_tokens"]
        resultContent = content["result"]
        
        return resultContent, input_tokens, output_tokens
    except Exception as e:
        print(e)
        return str(e)

def ask_ERNIE_4_8K(question, options):

    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + get_ERNIE_40_8K_access_token()

    prompt = f"{question}\nOptions:\n"
    for i, option in enumerate(options):
        prompt += f"{chr(65 + i)}. {option['choice_text']} \n"

    print(prompt)
    prompt += "Answer: "
    try:
        payload = json.dumps({
            "temperature": 0.5,
            "top_p": 0.7,
            "max_tokens": 100,
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        content = response.text
        content = json.loads(content)
        input_tokens = content["usage"]["prompt_tokens"]
        output_tokens = content["usage"]["total_tokens"] - content["usage"]["prompt_tokens"]
        resultContent = content["result"]
        
        return resultContent, input_tokens, output_tokens
    except Exception as e:
        print(e)
        return str(e)


query_functions = {
    "glm-3-turbo": ask_glm3turbo,
    "OpenAI-GPT-3": ask_chatgpt3,
    "OpenAI-GPT-4": ask_chatgpt4,
    "OpenAI-GPT-4o": ask_chatgpt4o,
    "ERNIE-4.0-8K": ask_ERNIE_4_8K,
    "Qwen-turbo": ask_tongyiqianwen,
    "glm-4": ask_glm4,
    "glm-4-air": ask_glm4air,
    "Meta-Llama-3-8B-Instruct": ask_llama3_8b,
    "Meta-Llama-3-70B-Instruct": ask_llama3_70b,
    "Gemma-2B-it": ask_gemma_2b,
    "Gemma-7B-it": ask_gemma_7b,
    "Qianfan_Chinese_Llama_2_7B": ask_Qianfan_Chinese_Llama_2_7B,
    "Qianfan_Chinese_Llama_2_70B": ask_Qianfan_Chinese_Llama_2_70B,
    "Qianfan_Chinese_Llama_2_13B": ask_Qianfan_Chinese_Llama_2_13B_v1
}

















