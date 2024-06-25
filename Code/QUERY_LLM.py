# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 15:28:30 2024

@author: 13419
"""
import json
#from configs import LLM_API_DETAILS
from FUNCTIONS import query_functions

def load_questions(file_path):
    with open(file_path, 'r' , encoding='utf-8') as file:
        questions = json.load(file)
    return questions

def query_llm(questions, model_name, num_questions_limit):
    
    query_model = query_functions[model_name]

    num_questions = 0;
    num_correct_answers = 0
    num_wrong_answers = 0
    correct_list = []
    wrong_list = []
    total_input_tokens = 0
    total_output_tokens = 0
    a = 1
 
    for question in questions:

        print(f"当前正在测试的题目是第{a}个题目,序号为：{question['question_number']}")
        a = a + 1
        #print(f"当前正在测试的题目序号为：{question['question_number']}")
        print(f"Question {question['question_text']}: ")
        
        options = question['choices']
        gtAnswer = question['correct_answer']
        
        model_answer, input_tokens, output_tokens = query_model(question['question_text'], options)
        
        total_input_tokens = total_input_tokens + input_tokens
        total_output_tokens = total_output_tokens + output_tokens

        print(f"Model answer: {model_answer} and ground truth: {gtAnswer}")
        print()


        if list(model_answer) == gtAnswer:
            num_correct_answers = num_correct_answers + 1
            #correct_list.append(int(question['question_number']))
            correct_dict = {}
            correct_dict["correct_index"] = question['question_number']
            correct_dict["model_answer"] = model_answer
            correct_dict["gt_answer"] = gtAnswer
            correct_list.append(correct_dict)
        else:
            num_wrong_answers = num_wrong_answers + 1
            wrong_dict = {}
            wrong_dict["wrong_index"] = question['question_number']
            wrong_dict["model_answer"] = model_answer
            wrong_dict["gt_answer"] = gtAnswer
            wrong_list.append(wrong_dict)
        num_questions = num_questions+1;
        if num_questions>= num_questions_limit:
            break

    print(f"Total input_tokens is {total_input_tokens} and total output_tokens is {total_output_tokens}")
    print('total, correct, wrong: ', num_questions, num_correct_answers, num_wrong_answers)
    
    with open('output.txt', 'a') as file:
        file.write('\n')
        file.write(str(model_name)) 
        file.write('\n')
        file.write(str(total_output_tokens))  # 写入变量1的内容
        file.write('\n') 
        file.write(str(total_input_tokens))  # 写入变量2的内容
        file.write('\n')  # 写入换行符
        file.write(str(num_questions))
        file.write('\n') 
        file.write(str(num_correct_answers))
        file.write('\n') 
    
    return wrong_list, correct_list









