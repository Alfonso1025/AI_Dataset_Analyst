from flask import Flask, render_template, request, redirect, url_for, flash
import os
from openAi import Chatbot
import pandas as pd



class Server:
    def __init__(self):
        print('hello world from server')
        self.app = Flask(__name__, template_folder='templates')
        self.app.config['UPLOAD_FOLDER'] = 'uploads'
        self.app.secret_key = 'a_secret_key'
        self.setup_routes()
        self.filename = ''

    def run(self):
        self.app.run(debug=True)

    def setup_routes(self):
        
        self.app.route('/upload', methods=['POST'])(self.upload_file)
        self.app.route('/display_prompt')(self.display_prompt)
        self.app.route('/get_prompt', methods=['POST'])(self.get_prompt)
        self.app.route('/')(self.index)
    
    def index(self):
        return render_template('upload.html')
    
    def display_prompt(self):
        return render_template('userPrompt.html', filename = self.filename)
    
    def get_column_names(self, dataset):
        # Get the column names as a list of strings
        column_names = dataset.columns.tolist()

        # Concatenate column names into a single string with commas
        column_names_string = ', '.join(column_names)

        return column_names_string


    def upload_file(self):
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file:
            # Save the uploaded file to the uploads folder
            filename = os.path.join(self.app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)

        if os.path.exists(filename):
            self.filename = file.filename
            print('the uploaded file is:', self.filename)
            flash('File uploaded successfully')
        else:
            flash('Failed uploading file')

        return redirect(url_for('display_prompt'))
    
    def get_prompt(self):
      if request.method == 'POST':
        user_input = request.form.get('text_input') 
        print('the filename is: ', self.filename)
        uploads_dir = os.path.join(os.path.dirname(__file__), 'uploads')
        file_path = os.path.join(uploads_dir, self.filename)
        # read dataset
        dataset = pd.read_csv(file_path)
        # obtain number of columns and rows
        colsNames = self.get_column_names(dataset)
        number_of_rows = dataset.shape[0]
        # Convert DataFrame to plain text
        text_data = ""
        for index, row in dataset.iterrows():
            text_data += f"Row {index + 1}: {', '.join(map(str, row.values))}\n"
        
        chat_bot = Chatbot(text_data,self.filename,colsNames, number_of_rows) 
        response = chat_bot.collect_messages(user_input)
        return render_template('userPrompt.html', response=response)
      








