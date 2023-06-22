from dash import Dash,html,Input,Output,callback,dcc
import mysql
from mysql.connector import connect
from PIL import Image
import dash_auth


USER_PASS_MAPPING={'admin':'1234'}
#connecton details
host='localhost'
user='root'
password='chatme@2023'
database='mydb'


app=Dash(__name__)


image_path=Image.open("C:\\Users\\Admin\\Desktop\\DSAIL\\assets\\rashes.jpg")
video1="./assets/static/How to tell if a rash needs medical attention.mp4"
image2_path= Image.open("C:\\Users\\Admin\\Desktop\\DSAIL\\assets\\heart failure.jpg")
image3_path= Image.open("C:\\Users\\Admin\\Desktop\\DSAIL\\assets\\DDA1.jpg")
video2="./assets/static/pop_up.mp4"



auth=dash_auth.BasicAuth(app,USER_PASS_MAPPING)

app.layout = html.Div(style={'background-color':'#3F000F'},
    children=[
        html.Div(
            id="image-div",
            style={"margin-left":'30%',"margin-right":'30%'},
            
            children=[
                
                
                html.Img(src=image_path, width="500", height="280"),
                html.Iframe(src=video1, width="560", height="280", style={"display": "none"}),
                html.Img(src=image2_path, width="500", height="280"),
                html.Img(src=image3_path, width="500", height="280"),
                html.Img(src=image3_path, width="500", height="280"),
                html.Iframe(src=video2, width="560", height="280", style={"display": "none"}),
            ],
        ),
        html.Div(
            id="dropdown-textarea-div",
            children=[
                html.Div(
                    [
                        html.Label('Symptoms',style={'color':'#FFE4E1'}),
                        dcc.Dropdown(
                            options=['skin rashes','jaundice(yellow eyes)','pale hands','edema','swollen legs','facial edema','hepatomegaly'],
                            value='hepatomegaly',
                            id='symptoms',
                            style={'background-color': 'lightgray','margin-right':'40%'},
                            multi=True,
                        ),
                        html.Label('Disease',style={'color':'#FFE4E1'}),
                        dcc.Dropdown(
                            options=['skin cancer','liver disease ','blood disorder','Sinusitis','anemia','heart failure',' Hepatitis'],
                            value='blood disorder',
                            id="disease",
                            style={'background-color': 'lightgray','margin-right':'40%',},
                            multi=True),
                        html.Label ('Comment',style={'color':'#FFE4E1'}),
                        dcc.Textarea(
                             id='textarea',
                            placeholder='Enter your comment',
                            style={'height': '100px','margin-right':'50%','width':'60%'},
                              )]  
)]  
        ),
        html.Br(),
        html.Button("SAVE",id="save-button",n_clicks=0,style={"color":"black"}),
        html.Button("NEXT", id="play_button", n_clicks=0,style={"margin-left":"15px","color":"black"}),
        
        html.Div(id='container', children=[],style={'color':'blue'}),
    ]
)


@app.callback(
    Output("image-div", "children"),
    [Input("play_button", "n_clicks")],
)
def play_video(n_clicks):
    if n_clicks ==0:
        return html.Div([
            html.Img(src=image3_path, width="500", height="280")
        ])
        
        
    elif n_clicks==1:
        return html.Div([
            html.Img(src=image2_path, width="500", height="280", style={"display": "block"})
        ])
    elif n_clicks==2:
        return html.Div([
            html.Img(src=image_path, width="500", height="280"),
        ])
    elif n_clicks==3:
        return html.Div([
            html.Iframe(src=video1, width="560", height="280", style={"display": "block"})
            ])
    else:
        return html.Div([
           html.Iframe(src=video2, width="560", height="280", style={"display": "none"})
        ])
@callback(
    Output('container','children'),
    [Input('symptoms','value'),
     Input('disease','value'),
     Input('save-button','n_clicks')]
)

def update_database(symptoms,disease,n_clicks):
    if n_clicks>=1:
        conn=mysql.connector.connect(host=host, user=user, password=password, database=database)
        cursor=conn.cursor()
        
        add_database="""INSERT INTO diagnosis1
        (filename,symptoms,disease)
        VALUES(%s,%s,%s)"""
        
        filename = "diagnosis"
        filename = str(filename)
        symptoms = str(symptoms)
        disease= str(disease)
        values = (filename,) + (symptoms,) + (disease,) 
        
        cursor.execute(add_database,values)
        
        print(' labels saved to database!')
        
        conn.commit()
        cursor.close()
        conn.close()
        
        

    

if __name__=='__main__':
  app.run_server(debug=True)      
