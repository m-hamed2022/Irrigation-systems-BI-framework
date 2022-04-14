import pandas as pd
import streamlit as st
from numerize import numerize

from matplotlib.pyplot import axes, text
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go



df = pd.read_csv("Data.csv")

st.set_page_config(layout="wide")


df = df[['Crop_Name','Category_Name','Season_name','Government_name','Region_name','Land size','production','Immersion','Sprinkler','Drip']]



def filter_rows_by_values(df, col, values):
    return df[~df[col].isin(values)]
def filter_rows_by_valuesN(df, col, values):
    return df[df[col].isin(values)]
# df = filter_rows_by_values(df,str(irrigation),[0,'0','NO'])
df = filter_rows_by_values(df,'production',[0])
df = df.reset_index(drop=True)
with st.container():
        
        a,b = st.columns(2)
        with a:
            
            
            dataRegion = df['Region_name'].drop_duplicates().to_list()
            dataRegion.append('All')
            dataRegion.sort()
            Region = st.selectbox('Select Region ',dataRegion)

            if Region  != 'All':
                df = df.loc[df['Region_name'] == Region]
            
        with b:
            dataCategory = df['Category_Name'].drop_duplicates().to_list()
            dataCategory.append('All')
            dataCategory.sort()
            Category = st.selectbox('Select Category ',dataCategory)

            if Category  != 'All':
                df = df.loc[df['Category_Name'] == Category]
        

dataCuntry = df['Government_name'].drop_duplicates().to_list()
   
dataCuntry.sort()
Cuntry = pd.DataFrame(columns = ['CuntryName', 'WaterUse', 'LandSize'])


for name in dataCuntry:
    sumWater = df.loc[df['Government_name'].isin([name]) ]
    sumW = sumWater['Immersion'].sum()
    sumL = sumWater['Land size'].sum()
    Cuntry = Cuntry.append({'CuntryName' : str(name), 'WaterUse' : sumW, 'LandSize' : sumL}, 
                ignore_index = True)

    
st.dataframe(Cuntry)
options1 = st.multiselect('Select Government to irrigation plan',dataCuntry)

df = df.loc[df['Government_name'].isin(options1) ]
xx = df
st.dataframe(df)
Crops = filter_rows_by_valuesN(df,'Sprinkler',['NO'])
Crops = filter_rows_by_valuesN(Crops,'Drip',['NO'])

st.markdown(Crops.Crop_Name.tolist())

options1 = st.multiselect('Select Crop to irrigate with Immersion',df['Crop_Name'].drop_duplicates())
dataOfImmersion = df.loc[df['Crop_Name'].isin(options1) ]
dataOfImmersion=dataOfImmersion[['Crop_Name','Category_Name','Season_name','Government_name','Region_name','Land size','production','Immersion']]
st.dataframe(dataOfImmersion)

sumW = dataOfImmersion['Immersion'].sum()
sumL = dataOfImmersion['Land size'].sum()
with st.container():
        
        a,b = st.columns(2)
        with a:
            st.markdown("**Sum of water used in Immersion**")
           
            st.markdown(f"<h1 style='text-align: center; color: red;'>{ str(numerize.numerize(int(sumW)))}</h1>", unsafe_allow_html=True)
        with b:
            st.markdown("**Sum of Land used in Immersion**")
            st.markdown(f"<h1 style='text-align: center; color: red;'>{ str(numerize.numerize(int(sumL)))}</h1>", unsafe_allow_html=True)

Crops = filter_rows_by_values(df,'Drip',['0',0,'NO'])

Crops =  Crops[~Crops['Crop_Name'].isin(options1)]
options2 = st.multiselect('Select Crop to irrigate with Drip',Crops['Crop_Name'].drop_duplicates())
dataOfDrip = df.loc[df['Crop_Name'].isin(options2) ]

dataOfAfter=dataOfDrip[['Crop_Name','Category_Name','Season_name','Government_name','Region_name','Land size','production','Drip','Immersion']]

dataOfDrip=dataOfDrip[['Crop_Name','Category_Name','Season_name','Government_name','Region_name','Land size','production','Drip']]
st.dataframe(dataOfDrip)

dataOfAfter["Drip"] = pd.to_numeric(dataOfAfter["Drip"])
cropName = dataOfAfter['Crop_Name'].drop_duplicates().to_list()
CropSum = pd.DataFrame(columns = ['Crop_Name', 'Immersion', 'Drip'])
for crop in cropName:
    sumCropWater = dataOfAfter.loc[dataOfAfter['Crop_Name'].isin([crop]) ]
    sumW = sumCropWater['Immersion'].sum()
    sumD = sumCropWater['Drip'].sum()
    CropSum = CropSum.append({'Crop_Name' : str(crop), 'Immersion' : sumW, 'Drip' : sumD}, 
                ignore_index = True)

 

# fig.add_trace(go.Bar(x=CropSum['Crop_Name'], y=CropSum['Drip'], name="Drip"),secondary_y=False)
# fig.add_trace(go.Bar(x=CropSum['Crop_Name'], y=CropSum['Immersion'], name='Immersion'),secondary_y=True,)
# fig.update_layout(
#             title_text='Defrance'
#             )

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Bar(x=CropSum['Crop_Name'],
                     y=CropSum['Drip'],
                     name="Drip",text=CropSum['Drip'])) 
fig.add_trace(go.Bar(x=CropSum['Crop_Name'],
                     y=CropSum['Immersion'],
                     name="Immersion",text=CropSum['Immersion']))

fig.update_layout(
            title_text='Defrance'
            )
st.plotly_chart(fig)




dataOfAfter['Immersion'] = pd.to_numeric(dataOfAfter['Immersion'])
dataOfDrip["Drip"] = pd.to_numeric(dataOfDrip["Drip"])
sumW = dataOfDrip['Drip'].sum()
sumWAfter = dataOfAfter['Immersion'].sum()
sumL = dataOfDrip['Land size'].sum()
st.markdown("**Sum of water used in Drip**")
with st.container():
        
        a,b = st.columns(2)
        with a:
            
            st.markdown(f"<h1 style='text-align: center; color: red;'>After :{ str(numerize.numerize(int(sumWAfter)))}</h1>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center; color: red;'>Before :{ str(numerize.numerize(int(sumW)))}</h1>", unsafe_allow_html=True)
            
        with b:
            if sumWAfter == 0:
                sumWAfter=1
            saved = int(sumW)/int(sumWAfter)*100
            st.markdown(f"<h1 style='text-align: center; color: red;'>Saved :{ str((100-int(saved)))}%</h1>", unsafe_allow_html=True)
            
            st.markdown(f"<h1 style='text-align: center; color: red;'>Land used :{ str(numerize.numerize(int(sumL)))}</h1>", unsafe_allow_html=True)

Crops = filter_rows_by_values(xx,'production',[0])
Last =  Crops[~Crops['Crop_Name'].isin(options2+options1)]
options3 = st.multiselect('Select Crop to irrigate with Sprinkler',Last['Crop_Name'].drop_duplicates())

Sprinkler = df.loc[df['Crop_Name'].isin(options3) ]
dataOfAfter=Sprinkler[['Crop_Name','Category_Name','Season_name','Government_name','Region_name','Land size','production','Sprinkler','Immersion']]
Sprinkler=Sprinkler[['Crop_Name','Category_Name','Season_name','Government_name','Region_name','Land size','production','Sprinkler']]

st.dataframe(Sprinkler)



dataOfAfter["Sprinkler"] = pd.to_numeric(dataOfAfter["Sprinkler"])
cropName = dataOfAfter['Crop_Name'].drop_duplicates().to_list()
CropSum = pd.DataFrame(columns = ['Crop_Name', 'Immersion', 'Sprinkler'])
for crop in cropName:
    sumCropWater = dataOfAfter.loc[dataOfAfter['Crop_Name'].isin([crop]) ]
    sumW = sumCropWater['Immersion'].sum()
    sumD = sumCropWater['Sprinkler'].sum()
    CropSum = CropSum.append({'Crop_Name' : str(crop), 'Immersion' : sumW, 'Sprinkler' : sumD}, 
                ignore_index = True)

 




fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Bar(x=CropSum['Crop_Name'],
                     y=CropSum['Immersion'],
                     name="Immersion",text=CropSum['Immersion'])) 
fig.add_trace(go.Bar(x=CropSum['Crop_Name'],
                     y=CropSum['Sprinkler'],
                     name="Sprinkler" ,text=CropSum['Sprinkler']))

fig.update_layout(
            title_text='Defrance'
            )
st.plotly_chart(fig)


Sprinkler["Sprinkler"] = pd.to_numeric(Sprinkler["Sprinkler"])
sumW = Sprinkler['Sprinkler'].sum()
sumWAfter = dataOfAfter['Immersion'].sum()
sumL = Sprinkler['Land size'].sum()

st.markdown("**Sum of water used in Sprinkler**")
with st.container():
        
        a,b = st.columns(2)
        with a:
            
            st.markdown(f"<h1 style='text-align: center; color: red;'>After :{ str(numerize.numerize(int(sumWAfter)))}</h1>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center; color: red;'>Before :{ str(numerize.numerize(int(sumW)))}</h1>", unsafe_allow_html=True)
            
        with b:
           
            if not sumWAfter:
               sumWAfter = 1 
            saved = int(sumW)/int(sumWAfter)*100
            st.markdown(f"<h1 style='text-align: center; color: red;'>Saved :{ str((100-int(saved)))}%</h1>", unsafe_allow_html=True)
            
            st.markdown(f"<h1 style='text-align: center; color: red;'>Land used :{ str(numerize.numerize(int(sumL)))}</h1>", unsafe_allow_html=True)


DataFrame = pd.DataFrame(columns = ['waterWay', 'waterapmount','LandSize'])


sumS = Sprinkler['Sprinkler'].sum()
sumLand = Sprinkler['Land size'].sum()
DataFrame = DataFrame.append({'waterWay' :'Sprinkler', 'waterapmount' : sumS ,'LandSize':sumLand}, ignore_index = True)

sumD = dataOfDrip['Drip'].sum()
sumLand = dataOfDrip['Land size'].sum()
DataFrame = DataFrame.append({'waterWay' :'Drip', 'waterapmount' : sumD,'LandSize':sumLand}, ignore_index = True)

sumI = dataOfImmersion['Immersion'].sum()
sumLand = dataOfImmersion['Land size'].sum()
DataFrame = DataFrame.append({'waterWay' :'Immersion', 'waterapmount' : sumI,'LandSize':sumLand}, ignore_index = True)


dataOfImmersion.rename({'Immersion': 'Water'}, axis=1, inplace=True)
dataOfImmersion['iregationWay'] = "Immersion"

dataOfDrip.rename({'Drip': 'Water'}, axis=1, inplace=True)

dataOfDrip['iregationWay'] = "Drip"
Sprinkler.rename({'Sprinkler': 'Water'}, axis=1, inplace=True)
Sprinkler['iregationWay'] = "Sprinkler"


df3 = dataOfImmersion.append(dataOfDrip, ignore_index=True)

df3 = df3.append(Sprinkler, ignore_index=True)
with st.container():
        
        a,b = st.columns(2)
        with a:
            drip = st.text_input('Drip Cost')
        with b:
            sprinkler = st.text_input('Sprinkler Cost')

df3

def catValue(row):
            if row['waterWay'] == 'Drip':
                return int(row['LandSize']*int(drip))
            elif row['waterWay'] == 'Sprinkler':
                return int(row['LandSize']*int(sprinkler))
            else:
                return int(0)
            
if drip and sprinkler :
    

    DataFrame['Cost'] = DataFrame.apply(lambda row: catValue(row), axis=1)
else:
     DataFrame['Cost'] =  0 


DataFrame
sumCost = int(DataFrame['Cost'].sum())
st.write("Total Cost = "+str(numerize.numerize(sumCost))+' LE' )
pie_chart = px.pie(
        data_frame=DataFrame,
        values='waterapmount',
        names='waterWay',
        color='waterWay',                      #differentiate markers (discrete) by color
        color_discrete_sequence=["red","green","blue","orange"],     #set marker colors
        # color_discrete_map={"WA":"yellow","CA":"red","NY":"black","FL":"brown"},
                      #values appear in bold in the hover tooltip
        # hover_data=['positive'],            #values appear as extra data in the hover tooltip
        # custom_data=['total'],              #values are extra data to be used in Dash callbacks
             #figure title
        template='presentation',            #'ggplot2', 'seaborn', 'simple_white', 'plotly',
                                            #'plotly_white', 'plotly_dark', 'presentation',
                                            #'xgridoff', 'ygridoff', 'gridon', 'none'
        width=800,                          #figure width in pixels
        height=600,                         #figure height in pixels
        hole=0.5,                           #represents the hole in middle of pie
        )
pie_chart

pie_chart = px.pie(
        data_frame=DataFrame,
        values='LandSize',
        names='waterWay',
        color='waterWay',                      #differentiate markers (discrete) by color
        color_discrete_sequence=["red","green","blue","orange"],     #set marker colors
        # color_discrete_map={"WA":"yellow","CA":"red","NY":"black","FL":"brown"},
                      #values appear in bold in the hover tooltip
        # hover_data=['positive'],            #values appear as extra data in the hover tooltip
        # custom_data=['total'],              #values are extra data to be used in Dash callbacks
             #figure title
        template='presentation',            #'ggplot2', 'seaborn', 'simple_white', 'plotly',
                                            #'plotly_white', 'plotly_dark', 'presentation',
                                            #'xgridoff', 'ygridoff', 'gridon', 'none'
        width=800,                          #figure width in pixels
        height=600,                         #figure height in pixels
        hole=0.5,                           #represents the hole in middle of pie
        )

pie_chart



sumAll = xx['Immersion'].sum()
# print(sumAll)
# sumS
# sumD
# sumI
allSolution = (sumD+sumI+sumS)
if sumAll:
    st.write("sum of solution : "+ str(numerize.numerize(allSolution)) )
    st.write("sum of Immersion : "+ str(numerize.numerize(sumAll)) )

    st.write("sum of Saved : "+ str(numerize.numerize(int(sumAll)-int(allSolution))) )
    st.write("saved of all : "+ str(numerize.numerize(100-(allSolution/sumAll)*100))+"%" )

# st.markdown(df.index.tolist())




