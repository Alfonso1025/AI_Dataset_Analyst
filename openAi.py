import openai
import pandas as pd
import os
openai.api_key=  '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'
 

class Chatbot:
    def __init__(self, dataset: str, filename:str, colsNames: str, numRows) -> None:
        self.file = dataset
        self.filename = filename
        self.colsNames = colsNames
        self.numRows = numRows
       
        

    def get_completion_from_messages(self, messages, model="gpt-3.5-turbo", temperature=0):
        response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature
        )

        return response.choices[0].message["content"]

    def collect_messages(self, prompt):
            max_token_size = 4096
            text = self.file
            title = self.filename
            cols_names = self.colsNames
            num_rows = self.numRows
            if len(text) > max_token_size:
                 text = text[:max_token_size]
	        

            context = [{'role' : 'system', 'content':f""" You will be fed a daset in text format
             delimited below by middle dashes -. You will read and analyse the dataset to form conclusions about it.
             You will be given the title of the dataset, delimited below by question marks ?.
             You will be given a list of the names of each column in the dataset, delimited by low dashes _.
             You will be given the number of rows in the dataset, delimited below by plus sign +. 
             You will also recibe a propmt from a user asking 
             you to analyse the dataset and provide useful information about the dataset
             The user may ask you to perform operations on the dataset. For example, 
             the user may ask you to add all the values in a column or the user may ask you to 
             calculate a mean etc.
             This is the dataset that you must analyze.  ---{text}---
             This is the title ??{title}??
             this is the lsit of column names __{cols_names}
             this is the number of rows ++{num_rows}++

           
   
             """}]
            context.append({'role':'user', 'content':f"{prompt}"})
            response = self.get_completion_from_messages(context) 
            context.append({'role':'assistant', 'content':f"{response}"})
            
            return response