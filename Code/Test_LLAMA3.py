import time
import pandas as pd
import json
import transformers
import torch
from modelscope import snapshot_download

system_prompt = 'You are an experienced Officer of the Watch (OOW). You have the following two skills: (1)Extensive experience in ship navigation; (2)Skilled at selecting the most accurate option from multiple choices based on the question meaning. Now I ask you to answer multiple choice questions about the theory and experience of ship operation. These questions have multiple candidate answers, but only one is correct. Your answer should only include the letter representing the correct option, such as A or B. Do not add any additional explanation, repetition of the options, or punctuation; provide only the letter. Let me give you a question and the correct answer as an example for your reference. Question: You are making way in restricted visibility when you hear the sound of a fog signal forward of your beam. You are required to reduce speed to; Options: A. a moderate speed commensurate with conditions; B. the minimum where your vessel can be kept on course; C. half speed if proceeding at a higher speed; D. a safe speed in relation stopping distance; <Assistant answer> B'
#system_prompt = '你是一个经验丰富的船舶值班驾驶员，现在我需要你去回答一些船舶操纵、值班、避碰、信号等方面的题目，这些题目有多个候选答案，但是仅有一个答案是正确的'
#system_prompt = system_prompt + '你必须牢牢记住，你的回答只需要包含候选答案的首字母，例如A或B，不要增加任何额外的解释或者复述选项内容，也不要添加任何标点符号，仅需要输出候选答案的首字母，请牢记这一点'


def load_questions(file_path):
    with open(file_path, 'r' , encoding='utf-8') as file:
        questions = json.load(file)
    return questions

def ask_llama3_70B_instruct(question, options):
    prompt = f"{question}\nOptions:\n"
    for i, option in enumerate(options):
        prompt += f"{chr(65 + i)}. {option['choice_text']} \n"

    #print(prompt)
    prompt += "Answer: "

    pipeline = transformers.pipeline(
    "text-generation",
    model="/root/.cache/modelscope/hub/LLM-Research/Meta-Llama-3-70B-Instruct/",
    model_kwargs={"torch_dtype": torch.bfloat16},
    device="cuda",
    )
    messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": prompt},
    ]

    prompt = pipeline.tokenizer.apply_chat_template(
		messages, 
		tokenize=False, 
		add_generation_prompt=True
    )
    terminators = [
    pipeline.tokenizer.eos_token_id,
    pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    outputs = pipeline(
    prompt,
    max_new_tokens=256,
    eos_token_id=terminators,
    do_sample=True,
    temperature=0.5,
    top_p=0.9,
    )
    #print(outputs[0]["generated_text"][len(prompt):])
    answer = outputs[0]["generated_text"][len(prompt):]
    total_tokens = 2
    output_tokens = 1
    input_tokens = total_tokens - output_tokens
    
    return answer, input_tokens, output_tokens

def ask_llama3_8B_instruct(question, options):
    prompt = f"{question}\nOptions:\n"
    for i, option in enumerate(options):
        prompt += f"{chr(65 + i)}. {option['choice_text']} \n"

    #print(prompt)
    prompt += "Answer: "

    pipeline = transformers.pipeline(
    "text-generation",
    model="/root/.cache/modelscope/hub/LLM-Research/Meta-Llama-3-8B-Instruct/",
    model_kwargs={"torch_dtype": torch.bfloat16},
    device="cuda",
    )
    messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": prompt},
    ]

    prompt = pipeline.tokenizer.apply_chat_template(
		messages, 
		tokenize=False, 
		add_generation_prompt=True
    )
    terminators = [
    pipeline.tokenizer.eos_token_id,
    pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    outputs = pipeline(
    prompt,
    max_new_tokens=256,
    eos_token_id=terminators,
    do_sample=True,
    temperature=0.5,
    top_p=0.9,
    )
    print(outputs[0]["generated_text"][len(prompt):])
    answer = outputs[0]["generated_text"][len(prompt):]
    total_tokens = 2
    output_tokens = 1
    input_tokens = total_tokens - output_tokens
    
    return answer, input_tokens, output_tokens

def ask_questions(questions, model_name):

    num_questions = 0;
    num_correct_answers = 0
    num_wrong_answers = 0
    correct_list = []
    wrong_list = []
    total_input_tokens = 0
    total_output_tokens = 0
    a = 1

    for question in questions:
        # print(f"Question {question['number']}: {question['stem']}")
        print(f"当前正在测试的题目是第{a}个题目,序号为：{question['question_number']}")
        a = a + 1
        #print(f"Question {question['question_text']}: ")

        #withFigure = question['figure']
        #if withFigure == 'Y':
        #    continue
        #  question = questions[2]
        options = question['choices']
        gtAnswer = question['correct_answer']
        
        model_answer, input_tokens, output_tokens = model_name(question['question_text'], options)
        total_input_tokens = total_input_tokens + input_tokens
        total_output_tokens = total_output_tokens + output_tokens
        # print(f"ChatGPT's answer is: {chatgpt_answer}")
        # print('model_answer')
        #print(f"Model answer: {model_answer} and ground truth: {gtAnswer}")
        print()
        
        #print(chatgpt_answer)

        if list(model_answer) == gtAnswer:
            num_correct_answers = num_correct_answers + 1
            #correct_list.append(int(question['question_number']))
            correct_dict = {}
            correct_dict["correct_index"] = question['question_number']
            correct_dict["model_answer"] = list(model_answer)
            correct_dict["gt_answer"] = gtAnswer
            correct_list.append(correct_dict)
        else:
            num_wrong_answers = num_wrong_answers + 1
            wrong_dict = {}
            wrong_dict["wrong_index"] = question['question_number']
            wrong_dict["model_answer"] = list(model_answer)
            wrong_dict["gt_answer"] = gtAnswer
            wrong_list.append(wrong_dict)
        num_questions = num_questions+1;
        if num_questions>= num_questions_to_ask:
            break
    
    #print(f"Total input_tokens is {total_input_tokens} and total output_tokens is {total_output_tokens}")
    #print('total, correct, wrong: ', num_questions, num_correct_answers, num_wrong_answers)
    with open('output.txt', 'a') as file:
        #file.write('\n')
        #file.write(str(model_name)) 
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

questionJsonFile = 'UK_THEORY_TEST.json'
questions = load_questions(questionJsonFile)
num_questions_to_ask = 1000
###################################################################
#################### 记得改模型名，GPT太贵了，破产了 #################
###################################################################
start_time = time.perf_counter() 
wrong_list, correct_list = ask_questions(questions, ask_llama3_8B_instruct)
end_time = time.perf_counter()  # 记录结束时间
elapsed_time = end_time - start_time  # 计算运行时间
print(f"程序运行时间：{elapsed_time}秒")
####################################################################
df_wrong = pd.DataFrame(wrong_list, columns=['wrong_index', 'model_answer', 'gt_answer'])
df_correct = pd.DataFrame(correct_list, columns=['correct_index', 'model_answer', 'gt_answer'])
# 将DataFrame保存到Excel文件
df_wrong.to_excel('wronglist.xlsx', index=False)
df_correct.to_excel('correctlist.xlsx', index=False)

