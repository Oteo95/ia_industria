from langchain.docstore.document import Document
import pandas as pd

df  = pd.read_csv("/Users/m322550/Desktop/ia_industria/rag/cities.csv")
docs = []
for idx,   i in df.iterrows():
    docs.append(Document(page_content=f"city: {i['city']} description:{i['description']}", metadata={"source": "local", "reference": i['city']}))

from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

db = FAISS.from_documents(docs, HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5"))


retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 4})



import torch
#pip install bitsandbytes
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

model_name = "HuggingFaceH4/zephyr-7b-beta"

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True, bnb_4bit_use_double_quant=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.bfloat16
)

model = AutoModelForCausalLM.from_pretrained(model_name, quantization_config=bnb_config)
tokenizer = AutoTokenizer.from_pretrained(model_name)


from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from transformers import pipeline
from langchain_core.output_parsers import StrOutputParser

text_generation_pipeline = pipeline(
    model=model,
    tokenizer=tokenizer,
    task="text-generation",
    temperature=0.2,
    do_sample=True,
    repetition_penalty=1.1,
    return_full_text=True,
    max_new_tokens=400,
)

llm = HuggingFacePipeline(pipeline=text_generation_pipeline)

prompt_template = """
<|system|>
Answer the question based on your knowledge. Use the following context to help:

{context}

</s>
<|user|>
{question}
</s>
<|assistant|>

 """

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=prompt_template,
)

llm_chain = prompt | llm | StrOutputParser()


from langchain_core.runnables import RunnablePassthrough

retriever = db.as_retriever()

rag_chain = {"context": retriever, "question": RunnablePassthrough()} | llm_chain

question = "How do you combine multiple adapters?"

llm_chain.invoke({"context": "", "question": question})

