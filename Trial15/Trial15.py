from flask import Flask, render_template, request
import os
import webbrowser
from waitress import serve
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    main_folder_path = r'C:\Users\vijay\OneDrive\Desktop\Trial15\AUTOMATION TEST REPORTS'

    if request.method == 'POST':
        selected_main_folder = request.form['main_folder']
        selected_subfolder = request.form.get('subfolder', '')

        subfolders = [folder for folder in os.listdir(os.path.join(main_folder_path, selected_main_folder)) if os.path.isdir(os.path.join(main_folder_path, selected_main_folder, folder))]

        return render_template('index.html', main_folders=[selected_main_folder], selected_main_folder=selected_main_folder, subfolders=subfolders, selected_subfolder=selected_subfolder)

    main_folders = [folder for folder in os.listdir(main_folder_path) if os.path.isdir(os.path.join(main_folder_path, folder))]

    return render_template('index.html', main_folders=main_folders, subfolders=[])

@app.route('/select_subfolder', methods=['POST'])
def select_subfolder():
    selected_main_folder = request.form['main_folder']
    selected_subfolder = request.form['subfolder']

    subfolder_path = os.path.join(r'C:\Users\vijay\OneDrive\Desktop\Trial15\AUTOMATION TEST REPORTS', selected_main_folder, selected_subfolder)
    sheets = [file for file in os.listdir(subfolder_path) if file.endswith('.xlsx')]

    return render_template('index.html', main_folders=[selected_main_folder], selected_main_folder=selected_main_folder, subfolders=[selected_subfolder], selected_subfolder=selected_subfolder, sheets=sheets)

@app.route('/display_sheet_data', methods=['POST'])
def display_sheet_data():
    selected_main_folder = request.form['main_folder']
    selected_subfolder = request.form['subfolder']

    excel_folder_path = os.path.join(r'C:\Users\vijay\OneDrive\Desktop\Trial15\AUTOMATION TEST REPORTS', selected_main_folder, selected_subfolder)
    excel_file_path = os.path.join(excel_folder_path, request.form['sheet_name'])

    xl = pd.ExcelFile(excel_file_path)
    sheets = xl.sheet_names

    all_data = {}

    for sheet_name in sheets:
        df = pd.read_excel(excel_file_path, sheet_name)
        all_data[sheet_name] = df.to_dict(orient='records')

    return render_template('display_sheet_data.html', main_folder=selected_main_folder, subfolder=selected_subfolder, sheets=sheets, all_data=all_data)

if __name__ == '__main__':
    webbrowser.open('http://localhost:5000')
    serve(app, host='localhost', port=5000)
