# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 11:19:57 2024

@author: 13419
"""
import json
import requests


#system_prompt = 'You are an experienced Officer of the Watch (OOW). You have the following three skills: (1)Extensive experience in ship navigation; (2)Proficient in taking theoretical exams; (3)Skilled at selecting the most accurate option from multiple choices based on the question meaning. Now I ask you to answer multiple choice questions about the theory and experience of ship operation. These questions have multiple candidate answers, but only one is correct. Your answer should only include the letter representing the correct option, such as A or B. Do not add any additional explanation, repetition of the options, or punctuation; provide only the letter. Let me give you a question and the correct answer as an example for your reference. Question: You are making way in restricted visibility when you hear the sound of a fog signal forward of your beam. You are required to reduce speed to; Options: A. a moderate speed commensurate with conditions; B. the minimum where your vessel can be kept on course; C. half speed if proceeding at a higher speed; D. a safe speed in relation stopping distance; <Assistant answer>: B'
#system_prompt = "你是一个经验丰富的船舶值班驾驶员。你拥有如下三个技能：（1）拥有丰富的船舶驾驶经验（2）擅长根据题目的含义从多个候选答案中选出最正确的一个选项。现在，我要求你去回答一些船舶操纵理论和经验方面的选择题。这些题目有多个候选答案，但是仅有一个答案是正确的，你的回答只需要包含候选答案的首字母，例如A或B，不要增加任何额外的解释或者复述选项内容，也不要添加任何标点符号，仅需要输出候选答案的首字母。我给你提供一个题目和答案的例子供你参考；Question: 在海上，当你看到来船的号灯仅为红，白，红，白垂直四盏灯，则来船为；Options: A、从事捕鱼的船舶当渔具被障碍物挂住时; B、失去控制的船舶在航对水移动; C、除清除水雷作业的和拖带以外的操纵能力受到限制的船舶在航对水移动；D、除清除水雷作业的和拖带以外的操纵能力受到限制的船舶在航不对水移动；Assistant answer: C"
system_prompt = "You are an experienced ship officer on duty with the following skills: (1) extensive experience in ship navigation, and (2) proficiency in selecting the most accurate option from multiple candidates based on the question's meaning. Now, you are required to answer several multiple-choice questions related to ship handling theory and experience. These questions come with multiple candidate answers, but only one is correct. Remember, your response should only include the initial letter of the chosen option (e.g., A or B) and must not contain any additional content or symbols. Let me give you a question and the correct answer as an example for your reference. Question: You are making way in restricted visibility when you hear the sound of a fog signal forward of your beam. You are required to reduce speed to; Options: A. a moderate speed commensurate with conditions; B. the minimum where your vessel can be kept on course; C. half speed if proceeding at a higher speed; D. a safe speed in relation stopping distance; <Assistant answer>B"

# 用于Baidu鉴权，API Key和Secret Key可以在百度千帆大模型平台上获取

Baidu_url = "url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=[API Key]&client_secret=[Secret Key]"


def get_gemma_2b_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", Baidu_url, headers=headers, data=payload)
    return response.json().get("access_token")

def get_ERNIE_4_8K_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """
        
    url = Baidu_url
    
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")

def get_gemma_7b_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """
    
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", Baidu_url, headers=headers, data=payload)
    return response.json().get("access_token")

def get_Qianfan_Chinese_Llama_2_7B_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """
        
        
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", Baidu_url, headers=headers, data=payload)
    return response.json().get("access_token")

def get_Qianfan_Chinese_Llama_2_13B_v1_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """
        
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", Baidu_url, headers=headers, data=payload)
    return response.json().get("access_token")

def get_Qianfan_Chinese_Llama_2_70B_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """
        

    
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", Baidu_url, headers=headers, data=payload)
    return response.json().get("access_token")

def get_Meta_Llama_3_8B_Instruct_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """
      
    
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")

def get_Meta_Llama_3_70B_Instruct_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """
    
    
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", Baidu_url, headers=headers, data=payload)
    return response.json().get("access_token")

def get_ERNIE_40_8K_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """
    
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", Baidu_url, headers=headers, data=payload)
    return response.json().get("access_token")

