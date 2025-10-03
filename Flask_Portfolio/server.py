from flask import Flask,render_template,jsonify
import os
import requests
import json
import base64

PORT = 8080

OWNER = "Mulzin"
REPO = "portfolio-jesus-lomeli"
URL = f"https://api.github.com/repos/{OWNER}/{REPO}/contents"
THUMBNAIL_FOLDER_PATH = f'static/images/project_thumbnail'

projects = []
app = Flask(__name__)

def reset_projects():
    clear_thumbnail_folder()
    update_projects_list()
    return

def clear_thumbnail_folder():
    for item in os.listdir(THUMBNAIL_FOLDER_PATH):
        item_path = os.path.join(THUMBNAIL_FOLDER_PATH, item)
    try:     
        os.remove(item_path)          
    except Exception as e:
        #error handling 
        #print so it goes to the aws logs
        #this way i remember to read the logs
        #dont stop the server
        return
    return

def update_projects_list():
    project_list = get_project_list()  
    
    for project in project_list:
        project_path = project['path'] 
        thumbnail_path = f"{project_path}.png"

        project_info = get_project_info(project_path)   
        project_info.append(thumbnail_path)
        project_info.append(project['html_url'])

        projects.append(project_info)   

        download_project_thumbnail(project_path)
    return     

def get_project_list():
    projects_url = f"{URL}/"
    data = pull_data_from_repo(projects_url).json()
    return data

def pull_data_from_repo(data_url):
    response = requests.get(data_url)

    if response.status_code == 200:
        return response
    else:
        print(response.status_code)
        #WIP, find a way to stop this chain of methods
        #without shuting down the server
        return None
    
def get_project_info(project_path):
    json_url = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/refs/heads/main/{project_path}/info.json"
    data = pull_data_from_repo(json_url)
    info_json = json.loads(data.text) #try catch here

    title =         info_json['title']
    summary =       info_json['summary']
    summary_spa =   info_json['resumen']
    area =          info_json['area']

    return [title,summary,summary_spa,area]

def download_project_thumbnail(project_path):
    img_name = "thumbnail.png" 
    img_path = f"{URL}/{project_path}/{img_name}"    
    
    data = pull_data_from_repo(img_path).json()
    base64img = data['content']
    img = base64.b64decode(base64img)

    filename = f'{THUMBNAIL_FOLDER_PATH}/{project_path}.png'

    with open(filename, "wb") as f:
        f.write(img)    
    return

@app.route("/")
def root():    
    return render_template('/english/home.html')

@app.route("/home") 
def home():     
    return render_template('/english/home.html')

@app.route("/portfolio")
def portfolio():
    print(32)
    return render_template('/english/portfolio.html')

@app.route("/inicio") 
def inicio():     
    return render_template('/espanol/inicio.html')

@app.route("/get_projects")
def get_projects():   
    return jsonify(projects)

if __name__ == "__main__":
  reset_projects()
  app.run(debug=True, host="0.0.0.0", port=PORT)  