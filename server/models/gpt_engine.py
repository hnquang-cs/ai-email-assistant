from abc import ABC, abstractmethod
import os

from dotenv import load_dotenv
from openai import OpenAI
import torch
from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer

class GPTEngine(ABC):
    @abstractmethod
    def sentiment_analysis(self, mail_content):
        pass

    @abstractmethod
    def content_summary(self, mail_content):
        pass

    @abstractmethod
    def generate_reply(self, mail_content):
        pass

class ChatGPT(GPTEngine):
    def __init__(self):
        load_dotenv("models\\.env")
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)

    def sentiment_analysis(self, mail_content):
        instruction = f"""
        Dưới đây là nội dung email phản hồi từ khách hàng. Hãy phân loại cảm xúc khách hàng dựa trên nội dung email theo 3 mức độ: 1. Hài lòng, 2. Bình thường, 3. Tiêu cực.
        Chỉ trả lời: "Hài lòng", "Bình thường" hoặc "Tiêu cực", không phân tích gì thêm.
        Nội dung email:
        {mail_content}
        """

        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[
                {"role": "user", "content": instruction}
            ]
        )

        return completion.choices[0].message.content

    def content_summary(self, mail_content):
        instruction = f"""
        Tóm tắt nội dung email phản hồi từ khách hàng.
        Nội dung email:
        {mail_content}
        """

        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[
                {"role": "user", "content": instruction}
            ]
        )

        return completion.choices[0].message.content
    
    def generate_reply(self, mail_content):
        instruction = f"""
        Dưới đây là nội dung email phản hồi từ khách hàng. Hãy viết email trả lời khách hàng một cách chuyên nghiệp.
        Nội dung email của khách hàng:
        {mail_content}
        """

        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[
                {"role": "user", "content": instruction}
            ]
        )

        return completion.choices[0].message.content

class PhoGPT(GPTEngine):
    def __init__(self):
        model_path = "./phogpt-4b/"

        config = AutoConfig.from_pretrained(pretrained_model_name_or_path="vinai/PhoGPT-4B", trust_remote_code=True)  
        config.init_device = "cuda"
        self.model = AutoModelForCausalLM.from_pretrained(model_path, config=config, torch_dtype=torch.bfloat16, trust_remote_code=True)
        self.model.eval()
        self.model.to("cuda")

        # Tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    
    def sentiment_analysis(self, mail_content):
        PROMPT_TEMPLATE = "### Câu hỏi: {instruction}\n### Trả lời:"  

        instruction = f"""
        Dưới đây là nội dung email phản hồi từ khách hàng. Hãy phân loại cảm xúc khách hàng dựa trên nội dung email theo 3 mức độ: 1. Hài lòng, 2. Bình thường, 3. Tiêu cực.
        Chỉ trả lời: "Hài lòng", "Bình thường" hoặc "Tiêu cực", không phân tích gì thêm.
        Nội dung email:
        {mail_content}
        """
        input_prompt = PROMPT_TEMPLATE.format_map({"instruction": instruction})

        input_ids = self.tokenizer(input_prompt, return_tensors="pt")
        input_ids = {k: v.to("cuda") for k, v in input_ids.items()}  # Move input tensors to GPU

        outputs = self.model.generate(  
            inputs=input_ids["input_ids"],  
            attention_mask=input_ids["attention_mask"],  
            do_sample=True,  
            temperature=1.0,  
            top_k=50,  
            top_p=0.9,  
            max_new_tokens=1024,  
            eos_token_id=self.tokenizer.eos_token_id,  
            pad_token_id=self.tokenizer.pad_token_id
        )  

        response = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]  
        response = response.split("### Trả lời:")[1]
        return response
    
    def content_summary(self, mail_content):
        PROMPT_TEMPLATE = "### Câu hỏi: {instruction}\n### Trả lời:"  

        instruction = f"""
        Tóm tắt nội dung email phản hồi từ khách hàng.
        Nội dung email:
        {mail_content}
        """

        input_prompt = PROMPT_TEMPLATE.format_map({"instruction": instruction})

        input_ids = self.tokenizer(input_prompt, return_tensors="pt")
        input_ids = {k: v.to("cuda") for k, v in input_ids.items()}

        outputs = self.model.generate(  
            inputs=input_ids["input_ids"],  
            attention_mask=input_ids["attention_mask"],  
            do_sample=True,  
            temperature=1.0,  
            top_k=50,  
            top_p=0.9,  
            max_new_tokens=1024,  
            eos_token_id=self.tokenizer.eos_token_id,  
            pad_token_id=self.tokenizer.pad_token_id  
        )

        response = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
        response = response.split("### Trả lời:")[1]
        return response
    
    def generate_reply(self, mail_content):
        PROMPT_TEMPLATE = "### Câu hỏi: {instruction}\n### Trả lời:"  

        instruction = f"""
        Dưới đây là nội dung email phản hồi từ khách hàng. Hãy viết email trả lời khách hàng một cách chuyên nghiệp.
        Nội dung email của khách hàng:
        {mail_content}
        """
        
        input_prompt = PROMPT_TEMPLATE.format_map({"instruction": instruction})

        input_ids = self.tokenizer(input_prompt, return_tensors="pt")
        input_ids = {k: v.to("cuda") for k, v in input_ids.items()}

        outputs = self.model.generate(  
            inputs=input_ids["input_ids"],  
            attention_mask=input_ids["attention_mask"],  
            do_sample=True,  
            temperature=1.0,  
            top_k=50,  
            top_p=0.9,  
            max_new_tokens=1024,  
            eos_token_id=self.tokenizer.eos_token_id,  
            pad_token_id=self.tokenizer.pad_token_id  
        )

        response = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
        response = response.split("### Trả lời:")[1]
        return response