# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 11:30:45 2024

@author: 13419
"""
import time
import pandas as pd
from QUERY_LLM import load_questions
from QUERY_LLM import query_llm

# 请求函数根据名称选择适当的API调用格式和参数
def main():
        
    models = ["Gemma-7B-it", "Gemma-2B-it", "Meta-Llama-3-8B-Instruct", 
              "Meta-Llama-3-70B-Instruct","OpenAI-GPT-3", "OpenAI-GPT-4", 
              "OpenAI-GPT-4o","glm4", "glm3turbo", "ERNIE-4.0-8K", 
              "Qwen-turbo", "Qianfan_Chinese_Llama_2_7B", 
              "Qianfan_Chinese_Llama_2_70B", "Qianfan_Chinese_Llama_2_13B"]
##############################################################################
#### 选择想要调用的LLM模型 #####################################################
    model_name = "Gemma-7B-it"
##############################################################################    
    questionJsonFile = 'C:\\Users\\13419\OneDrive\\桌面\\避碰交规\\ZH_THEORY_TEST.json'
    questions = load_questions(questionJsonFile)

    try:
        if model_name in models:
            
            print("into main")
            ##################################################################
            ## 设置测试的题目数量 ##############################################
            num_questions_limit = 1000
            ##################################################################
            start_time = time.perf_counter() 
            wrong_list, correct_list = query_llm(questions, model_name, num_questions_limit)
            end_time = time.perf_counter()  # 记录结束时间
            elapsed_time = end_time - start_time  # 计算运行时间
            print(f"程序运行时间：{elapsed_time}秒")
            ##################################################################
            with open('output.txt', 'a') as file:
                file.write(str(elapsed_time))
                file.write('\n')
            df_wrong = pd.DataFrame(wrong_list, columns=['wrong_index', 'model_answer', 'gt_answer'])
            df_correct = pd.DataFrame(correct_list, columns=['correct_index', 'model_answer', 'gt_answer'])
            df_wrong.to_excel('wronglist.xlsx', index=False)
            df_correct.to_excel('correctlist.xlsx', index=False)
            ##################################################################
        else:
            raise ValueError(f"Model {model_name} is not supported.")
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(e)



if __name__ == "__main__":
    main()