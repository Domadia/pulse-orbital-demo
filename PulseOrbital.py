import requests
import json
import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt

container = st.container()
container.header("PulseOrbital")
container.write("Note: Fetch the maximum desired cloud coverage based on latitude and longitude. Enter the details and submit form to obtain the result.")

with st.form("required_data"):
    input_cloudiness = st.slider("Cloudiness",min_value=0,max_value=100)
    input_longitude = st.number_input("Longitude",min_value=-180.0,max_value=180.0,step=0.000001,format="%.2f",value=0.0)
    input_latitude = st.number_input("Latitude",min_value=-90.0,max_value=90.0,step=0.0000001,format="%.2f",value=0.0)
    st.form_submit_button('Submit')

st.text("Showing results for latitude : "+str(input_latitude)+" & longitude :"+str(input_longitude))
web_response = requests.get("https://api.openweathermap.org/data/2.5/forecast?lat="+str(input_latitude)+"&lon="+str(input_longitude)+"&appid=6ee9587e880bd7100185d0f840b6fb8e")
json_response = json.loads(json.dumps(web_response.json()))

derived_json_response = json_response["list"]

date_and_time = []
cloudiness = []
for key in derived_json_response:
    if (key["clouds"])["all"] <= input_cloudiness :
      cloudiness.append((key["clouds"])["all"])
      date_and_time.append(key["dt_txt"])

data_df = pd.DataFrame(
    {
        "Date/Time": date_and_time,
        "cloudiness" : cloudiness 

    }
)

df = pd.DataFrame({
    "col1": [input_latitude],
    "col2": [input_longitude]
})

col1, col2 = st.columns([3, 5])

with col1:
   st.dataframe(
    data_df,
    column_config={
        "Date/Time": st.column_config.DatetimeColumn(
            "Date/Time",
            format="D MMM YYYY, h:mm a",
            step=60,
        ),
        "cloudiness": st.column_config.NumberColumn()
    },
    hide_index=True,
)
   
with col2:
    st.map(df,latitude='col1', longitude='col2',zoom=2)
