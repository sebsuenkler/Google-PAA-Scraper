from transformers import pipeline

question_answerer = pipeline("question-answering")

context = r"""
Extractive Question Answering is the task of extracting an answer from a text given a question. An example of a
question answering dataset is the SQuAD dataset, which is entirely based on that task. If you would like to fine-tune
a model on a SQuAD task, you may leverage the examples/pytorch/question-answering/run_squad.py script.
"""

result = question_answerer(question="What is extractive question answering?", context=context)
print(
    f"Answer: '{result['answer']}', score: {round(result['score'], 4)}, start: {result['start']}, end: {result['end']}"
)

result = question_answerer(question="What is a good example of a question answering dataset?", context=context)
print(
    f"Answer: '{result['answer']}', score: {round(result['score'], 4)}, start: {result['start']}, end: {result['end']}"
)


qa_model = pipeline("question-answering")
question = "Where do I live?"
context = "My name is Merve and I live in İstanbul."
context_2 = "My name is Sebastian and I live in Berlin"
print(qa_model(question = question, context = context))
print(qa_model(question = question, context = context_2))


qa_model = pipeline("question-answering")
question = "Who is Harry Potter?"
google = "Harry Potter is a wizard, the only child of James and Lily Potter. He is famous for having survived an attack by Lord Voldemort when he was a baby. He is also sometimes known as 'The Boy Who Lived'. For the first eleven years of his life Harry lives with his mean aunt and uncle and is unaware of his wizarding roots."
bing = "Harry James Potter is a fictional character and the titular protagonist in J. K. Rowling 's series of eponymous novels. The majority of the books' plot covers seven years in the life of the orphan Harry, who, on his eleventh birthday, learns he is a wizard."
print(qa_model(question = question, context = google))
print(qa_model(question = question, context = bing))


from sentence_transformers import SentenceTransformer, util
sentences = ["I'm happy", "I'm full of happiness"]

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

#Compute embedding for both lists
embedding_1= model.encode(sentences[0], convert_to_tensor=True)
embedding_2 = model.encode(sentences[1], convert_to_tensor=True)

print(util.pytorch_cos_sim(embedding_1, embedding_2))
