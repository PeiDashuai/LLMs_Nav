
import json
import re
from docx import Document

doc = Document('5_ZH_THEORY_TEST.docx')  # 在这里插入你的文件路径和名称
questions = []  # 存储题目的列表
question = None  # 当前处理的题目

for para in doc.paragraphs:
    text = para.text.strip()
    # 匹配题目
    match_question = re.match(r'(\d+)\.(.+)', text)
    if match_question:
        # 如果之前有题目在处理中，将其添加到questions列表
        if question is not None:
            questions.append(question)
        # 开始处理新题目
        question_number, question_text = match_question.groups()
        question = {'question_number': question_number, 'question_text': question_text, 'choices': []}
        continue
    # 匹配选项
    match_choice = re.match(r'([A-D])、(.+)', text)
    if match_choice:
        choice_letter, choice_text = match_choice.groups()
        choice = {'choice_letter': choice_letter, 'choice_text': choice_text}
        question['choices'].append(choice)
    # 匹配正确答案
    match_answer = re.match(r'【正确答案】：([A-D])', text)
    if match_answer:
        correct_answer = match_answer.groups()
        question['correct_answer'] = correct_answer

# 不要忘记添加最后一题
if question is not None:
    questions.append(question)

# 保存为JSON格式
with open('5_ZH_THEORY_TEST.json', 'w', encoding='utf-8') as file:
    json.dump(questions, file, ensure_ascii=False, indent=4)