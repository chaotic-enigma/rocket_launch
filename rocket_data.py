import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Event, Input, Output
import plotly.graph_objs as go
import random
import time
from collections import deque

app = dash.Dash(__name__)

colors = {
    'background': '#424949',
    'text': '#7FDBFF'
}

optimality = 50
time_rate = deque(maxlen=optimality)
rate_acceleration = deque(maxlen=optimality)
gyroscopic_rate = deque(maxlen=optimality)
magnitude_rate = deque(maxlen=optimality)
velocity_rate = deque(maxlen=optimality)
pressure_rate = deque(maxlen=optimality)
temperature_c = deque(maxlen=optimality)

rocket_sensors = {'Acceleration' : rate_acceleration,
						'Gyroscope' : gyroscopic_rate,
						'Magnitude' : magnitude_rate,
						'Velocity' : velocity_rate,
						'Pressure' : pressure_rate,
						'Temperature' : temperature_c}

def rocket_data_updation(time_rate,rate_acceleration,gyroscopic_rate,magnitude_rate,velocity_rate,pressure_rate,temperature_c):

	time_rate.append(time.time()) # record the current time
	# random_data
	if len(time_rate) == 1:
		rate_acceleration.append(random.randrange(300,450))
		gyroscopic_rate.append(random.randrange(120,180))
		magnitude_rate.append(random.randrange(200,350))
		velocity_rate.append(random.randrange(4250,5250))
		pressure_rate.append(random.randrange(690,880))
		temperature_c.append(random.randrange(-10,10))
	else:
		for rate_data in [rate_acceleration,gyroscopic_rate,magnitude_rate,velocity_rate,pressure_rate,temperature_c]:
			rate_data.append(rate_data[-1]+rate_data[-1]*random.uniform(-0.00001,0.00001))

	return time_rate,rate_acceleration,gyroscopic_rate,magnitude_rate,velocity_rate,pressure_rate,temperature_c

time_rate,rate_acceleration,gyroscopic_rate,magnitude_rate,velocity_rate,pressure_rate,temperature_c = rocket_data_updation(time_rate,rate_acceleration,gyroscopic_rate,magnitude_rate,velocity_rate,pressure_rate,temperature_c)

app.layout = html.Div([
		html.Div([
				html.H3('Rocket Sensors Testing',style={'color' : colors['text'],'textAlign' : 'center'})
			]),
		dcc.Dropdown(id='sensors',
						options=[{'label' : s,'value' : s} for s in rocket_sensors.keys()],
						value=['Pressure'],
						multi=False
						),
		html.Div(id='output-container'),
		html.Div(children=html.Div(id='graphs'),className='row'),
		dcc.Interval(id='sensor_updation',interval=1000)
	],
	# laying out the content
	className='container',style={'backgroundColor' : colors['background'],'width' : '98%','margin-left' : 10,'margin-right' : 10,'max-width' : 50000})

@app.callback(
		Output('graphs','children'),
		[Input('sensors','value')],
		events=[Event('sensor_updation','interval')]
	)

def sensor_plotting(sensors):

	graphs = []
	rocket_data_updation(time_rate,rate_acceleration,gyroscopic_rate,magnitude_rate,velocity_rate,pressure_rate,temperature_c)

	for each_sensor in sensors:
		data = go.Scatter(
				x=list(time_rate),
				y=list(rocket_sensors[each_sensor]),
				name=str(each_sensor),
				fill='tozeroy',
				fillcolor='#99a3a4'
			)
		graphs.append(html.Div(dcc.Graph(
				id=str(each_sensor),
				animate=True,
				figure={'data' : [data],'layout' : go.Layout(xaxis=dict(range=[min(time_rate),max(time_rate)]),
							yaxis=dict(range=[min(rocket_sensors[each_sensor]),max(rocket_sensors[each_sensor])]),
							margin={'l' : 50,'r' : 1,'t' : 45,'b' : 1},
							title='{}'.format(str(each_sensor)),

						)}
			)))

		return graphs

# external scripts
external_css = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css']
for css in external_css:
	app.css.append_css({'external_url' : css})							

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_js:
	app.scripts.append_script({'external_url' : js})



if __name__ == '__main__':
	app.run_server(debug=True)