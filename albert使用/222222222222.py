from transformers import AutoTokenizer, AutoModelForQuestionAnswering

tokenizer = AutoTokenizer.from_pretrained("Nomi97/Chatbot_QA")

model = AutoModelForQuestionAnswering.from_pretrained("Nomi97/Chatbot_QA")


print(1)