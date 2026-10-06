from flask import Flask, render_template
import os, sys
import pandas as pd
from bokeh.plotting import figure 
from bokeh.models import ColumnDataSource
from bokeh.io import show
from bokeh.models import TapTool, CustomJS, HoverTool, Div, Row, Column
from bokeh.tile_providers import Vendors, get_provider
from bokeh.embed import components
from bokeh.resources import CDN

app = Flask(__name__)



def mapper(disease="All", color="#040a42"):  

    map_dat = pd.read_csv(os.getcwd() + "/d_dat" + disease + ".csv", index_col=0)

    tile_provider = get_provider(Vendors.CARTODBPOSITRON)

    title = "Data Map of UK " + disease + " Clinical Trial Research and Collaboration"

    tools= ['pan,wheel_zoom,zoom_in,zoom_out,save,reset,tap', HoverTool(tooltips=[('Organisation', '@place'), ('No. Studies', '@number')])]
    bok_map = figure(x_range=(-1500000, 350000), y_range=(6500000, 8000000), title=title, tools=tools, active_scroll = "wheel_zoom",
               x_axis_type="mercator", y_axis_type="mercator", sizing_mode='stretch_both')
    bok_map.add_tile(tile_provider)

    source = ColumnDataSource(
        data=dict(lat=list(map_dat["merclat"]),
                  lon=list(map_dat["merclng"]),
                  size=list(map_dat["radius"]),
                  number=list(map_dat["number"]),
                  place=list(map_dat['locations']),
                  HTML=list(map_dat["HTML"])))


    circles = bok_map.circle(x="lon", y="lat", size="size", line_color=color, fill_color=color, fill_alpha=0.5, source=source)

    div = Div(text = '<div id="tooltip" style="position:relative; display:none"></div>', name = 'tooltip')


    TOOLTIPS = """
    <div class="tbl">
        <div>
         
            <span style="font-size: 16px; font-weight: bold;">@place</span>
        </div>
        <div>
            <span>@HTML{safe}</span>
        </div>
    </div> """


    code = '''  if (cb_data.source.selected.indices.length > 0){
                    var selected_index = cb_data.source.selected.indices[0];
                    var tooltip = document.getElementById("tooltip");

                    tooltip.style.display = 'block';
                    

                    tp = tp.replace('@place', cb_data.source.data.place[selected_index]);
                    tp = tp.replace('@HTML{safe}', cb_data.source.data.HTML[selected_index]);
                    tooltip.innerHTML = tp;
              } '''
    bok_map.select(TapTool).callback = CustomJS(args = {'circles': circles, 'plot': bok_map, 'tp': TOOLTIPS}, code = code)
    source.selected.js_on_change('indices', CustomJS(code = 'if (cb_obj.indices.length == 0) document.getElementById("tooltip").style.display = \"none\"'))
    layout = Row(bok_map, div, sizing_mode="scale_both")


    script1, div1 = components(layout)
    cdn_js=CDN.js_files
    cdn_js0 = cdn_js[0]
    cdn_js1 = cdn_js[1]
    cdn_js2 = cdn_js[2]
    cdn_js3 = cdn_js[3]
    return script1, div1, cdn_js0, cdn_js1, cdn_js2, cdn_js3


@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/")
def plot():
    script1, div1, cdn_js0, cdn_js1, cdn_js2, cdn_js3 = mapper()
    return render_template("plot.html", script1=script1, div1=div1, cdn_js0=cdn_js0, cdn_js1=cdn_js1, cdn_js2=cdn_js2, cdn_js3=cdn_js3)

@app.route("/Cancer/")
def Cancer():
    script1, div1, cdn_js0, cdn_js1, cdn_js2, cdn_js3 = mapper("Cancer", "pink")
    return render_template("plot.html", script1=script1, div1=div1, cdn_js0=cdn_js0, cdn_js1=cdn_js1, cdn_js2=cdn_js2, cdn_js3=cdn_js3)

@app.route("/Circulatory_System/")
def Circulatory_System():
    script1, div1, cdn_js0, cdn_js1, cdn_js2, cdn_js3 = mapper("Circulatory System", "#fc0303")
    return render_template("plot.html", script1=script1, div1=div1, cdn_js0=cdn_js0, cdn_js1=cdn_js1, cdn_js2=cdn_js2, cdn_js3=cdn_js3)

@app.route("/Digestive_System/")
def Digestive_System():
    script1, div1, cdn_js0, cdn_js1, cdn_js2, cdn_js3 = mapper("Digestive System", "#77fc03")
    return render_template("plot.html", script1=script1, div1=div1, cdn_js0=cdn_js0, cdn_js1=cdn_js1, cdn_js2=cdn_js2, cdn_js3=cdn_js3)

@app.route("/Ear_Nose_and_Throat/")
def Ear_Nose_and_Throat():
    script1, div1, cdn_js0, cdn_js1, cdn_js2, cdn_js3 = mapper("Ear, Nose and Throat", "#9003fc")
    return render_template("plot.html", script1=script1, div1=div1, cdn_js0=cdn_js0, cdn_js1=cdn_js1, cdn_js2=cdn_js2, cdn_js3=cdn_js3)

@app.route("/Eye_Diseases/")
def Eye_Diseases():
    script1, div1, cdn_js0, cdn_js1, cdn_js2, cdn_js3 = mapper("Eye Diseases", "#03adfc")
    return render_template("plot.html", script1=script1, div1=div1, cdn_js0=cdn_js0, cdn_js1=cdn_js1, cdn_js2=cdn_js2, cdn_js3=cdn_js3)

@app.route("/Genetic_Diseases/")
def Genetic_Diseases():
    script1, div1, cdn_js0, cdn_js1, cdn_js2, cdn_js3 = mapper("Genetic Diseases", "red")
    return render_template("plot.html", script1=script1, div1=div1, cdn_js0=cdn_js0, cdn_js1=cdn_js1, cdn_js2=cdn_js2, cdn_js3=cdn_js3)

@app.route("/Haematological_Disorders/")
def Haematological_Disorders():
    script1, div1, cdn_js0, cdn_js1, cdn_js2, cdn_js3 = mapper("Haematological Disorders", "#8a0303")
    return render_template("plot.html", script1=script1, div1=div1, cdn_js0=cdn_js0, cdn_js1=cdn_js1, cdn_js2=cdn_js2, cdn_js3=cdn_js3)

@app.route("/Infections_and_Infestations/")
def Infections_and_Infestations():
    script1, div1, cdn_js0, cdn_js1, cdn_js2, cdn_js3 = mapper("Infections and Infestations", "#6e6e6e")
    return render_template("plot.html", script1=script1, div1=div1, cdn_js0=cdn_js0, cdn_js1=cdn_js1, cdn_js2=cdn_js2, cdn_js3=cdn_js3)

@app.route("/Injury_Occupational_Diseases_Poisoning/")
def Injury_Occupational_Diseases_Poisoning():
    script1, div1, cdn_js0, cdn_js1, cdn_js2, cdn_js3 = mapper("Injury, Occupational Diseases, Poisoning", "#00450b")
    return render_template("plot.html", script1=script1, div1=div1, cdn_js0=cdn_js0, cdn_js1=cdn_js1, cdn_js2=cdn_js2, cdn_js3=cdn_js3)

@app.route("/Mental_and_Behavioural_Disorders/")
def Mental_and_Behavioural_Disorders():
    script1, div1, cdn_js0, cdn_js1, cdn_js2, cdn_js3 = mapper("Mental and Behavioural Disorders", "#1300c1")
    return render_template("plot.html", script1=script1, div1=div1, cdn_js0=cdn_js0, cdn_js1=cdn_js1, cdn_js2=cdn_js2, cdn_js3=cdn_js3)

@app.route("/Musculoskeletal_Diseases/")
def Musculoskeletal_Diseases():
    script1, div1, cdn_js0, cdn_js1, cdn_js2, cdn_js3 = mapper("Musculoskeletal Diseases", "#ff0044")
    return render_template("plot.html", script1=script1, div1=div1, cdn_js0=cdn_js0, cdn_js1=cdn_js1, cdn_js2=cdn_js2, cdn_js3=cdn_js3)

@app.route("/Neonatal_Diseases/")
def Neonatal_Diseases():
    script1, div1, cdn_js0, cdn_js1, cdn_js2, cdn_js3 = mapper("Neonatal Diseases", "#4c3c90")
    return render_template("plot.html", script1=script1, div1=div1, cdn_js0=cdn_js0, cdn_js1=cdn_js1, cdn_js2=cdn_js2, cdn_js3=cdn_js3)

@app.route("/Nervous_System_Diseases/")
def Nervous_System_Diseases():
    script1, div1, cdn_js0, cdn_js1, cdn_js2, cdn_js3 = mapper("Nervous System Diseases", "#00ff95")
    return render_template("plot.html", script1=script1, div1=div1, cdn_js0=cdn_js0, cdn_js1=cdn_js1, cdn_js2=cdn_js2, cdn_js3=cdn_js3)

@app.route("/Nutritional_Metabolic_Endocrine/")
def Nutritional_Metabolic_Endocrine():
    script1, div1, cdn_js0, cdn_js1, cdn_js2, cdn_js3 = mapper("Nutritional, Metabolic, Endocrine", "#ff9900")
    return render_template("plot.html", script1=script1, div1=div1, cdn_js0=cdn_js0, cdn_js1=cdn_js1, cdn_js2=cdn_js2, cdn_js3=cdn_js3)

@app.route("/Oral_Health/")
def Oral_Health():
    script1, div1, cdn_js0, cdn_js1, cdn_js2, cdn_js3 = mapper("Oral Health", "#99fffc")
    return render_template("plot.html", script1=script1, div1=div1, cdn_js0=cdn_js0, cdn_js1=cdn_js1, cdn_js2=cdn_js2, cdn_js3=cdn_js3)

@app.route("/Pregnancy_and_Childbirth/")
def Pregnancy_and_Childbirth():
    script1, div1, cdn_js0, cdn_js1, cdn_js2, cdn_js3 = mapper("Pregnancy and Childbirth", "#590052")
    return render_template("plot.html", script1=script1, div1=div1, cdn_js0=cdn_js0, cdn_js1=cdn_js1, cdn_js2=cdn_js2, cdn_js3=cdn_js3)

@app.route("/Respiratory/")
def Respiratory():
    script1, div1, cdn_js0, cdn_js1, cdn_js2, cdn_js3 = mapper("Respiratory", "#0972eb")
    return render_template("plot.html", script1=script1, div1=div1, cdn_js0=cdn_js0, cdn_js1=cdn_js1, cdn_js2=cdn_js2, cdn_js3=cdn_js3)

@app.route("/Signs_and_Symptoms/")
def Signs_and_Symptoms():
    script1, div1, cdn_js0, cdn_js1, cdn_js2, cdn_js3 = mapper("Signs and Symptoms", "#f2ff00")
    return render_template("plot.html", script1=script1, div1=div1, cdn_js0=cdn_js0, cdn_js1=cdn_js1, cdn_js2=cdn_js2, cdn_js3=cdn_js3)

@app.route("/Skin_and_Connective_Tissue_Diseases/")
def Skin_and_Connective_Tissue_Diseases():
    script1, div1, cdn_js0, cdn_js1, cdn_js2, cdn_js3 = mapper("Skin and Connective Tissue Diseases", "#2bff00")
    return render_template("plot.html", script1=script1, div1=div1, cdn_js0=cdn_js0, cdn_js1=cdn_js1, cdn_js2=cdn_js2, cdn_js3=cdn_js3)

@app.route("/Surgery/")
def Surgery():
    script1, div1, cdn_js0, cdn_js1, cdn_js2, cdn_js3 = mapper("Surgery", "#964B00")
    return render_template("plot.html", script1=script1, div1=div1, cdn_js0=cdn_js0, cdn_js1=cdn_js1, cdn_js2=cdn_js2, cdn_js3=cdn_js3)

@app.route("/Urological_and_Genital_Diseases/")
def Urological_and_Genital_Diseases():
    script1, div1, cdn_js0, cdn_js1, cdn_js2, cdn_js3 = mapper("Urological and Genital Diseases", "#ff5e00")
    return render_template("plot.html", script1=script1, div1=div1, cdn_js0=cdn_js0, cdn_js1=cdn_js1, cdn_js2=cdn_js2, cdn_js3=cdn_js3)




@app.route("/Behavioural/")
def Behavioural():
    script1, div1, cdn_js0, cdn_js1, cdn_js2, cdn_js3 = mapper("Behavioural", "#ff5e00")
    return render_template("plot.html", script1=script1, div1=div1, cdn_js0=cdn_js0, cdn_js1=cdn_js1, cdn_js2=cdn_js2, cdn_js3=cdn_js3)


@app.route("/Biological_and_Vaccine/")
def Biological_and_Vaccine():
    script1, div1, cdn_js0, cdn_js1, cdn_js2, cdn_js3 = mapper("Biological and Vaccine", "#ff5e00")
    return render_template("plot.html", script1=script1, div1=div1, cdn_js0=cdn_js0, cdn_js1=cdn_js1, cdn_js2=cdn_js2, cdn_js3=cdn_js3)


@app.route("/Device/")
def Device():
    script1, div1, cdn_js0, cdn_js1, cdn_js2, cdn_js3 = mapper("Device", "#ff5e00")
    return render_template("plot.html", script1=script1, div1=div1, cdn_js0=cdn_js0, cdn_js1=cdn_js1, cdn_js2=cdn_js2, cdn_js3=cdn_js3)


@app.route("/Drug/")
def Drug():
    script1, div1, cdn_js0, cdn_js1, cdn_js2, cdn_js3 = mapper("Drug", "#ff5e00")
    return render_template("plot.html", script1=script1, div1=div1, cdn_js0=cdn_js0, cdn_js1=cdn_js1, cdn_js2=cdn_js2, cdn_js3=cdn_js3)


@app.route("/Genetic/")
def Genetic():
    script1, div1, cdn_js0, cdn_js1, cdn_js2, cdn_js3 = mapper("Genetic", "#ff5e00")
    return render_template("plot.html", script1=script1, div1=div1, cdn_js0=cdn_js0, cdn_js1=cdn_js1, cdn_js2=cdn_js2, cdn_js3=cdn_js3)


@app.route("/Mixed/")
def Mixed():
    script1, div1, cdn_js0, cdn_js1, cdn_js2, cdn_js3 = mapper("Mixed", "#ff5e00")
    return render_template("plot.html", script1=script1, div1=div1, cdn_js0=cdn_js0, cdn_js1=cdn_js1, cdn_js2=cdn_js2, cdn_js3=cdn_js3)


@app.route("/Procedure_and_Surgery/")
def Procedure_and_Surgery():
    script1, div1, cdn_js0, cdn_js1, cdn_js2, cdn_js3 = mapper("Procedure and Surgery", "#ff5e00")
    return render_template("plot.html", script1=script1, div1=div1, cdn_js0=cdn_js0, cdn_js1=cdn_js1, cdn_js2=cdn_js2, cdn_js3=cdn_js3)

@app.route("/Supplement/")
def Supplement():
    script1, div1, cdn_js0, cdn_js1, cdn_js2, cdn_js3 = mapper("Supplement", "#ff5e00")
    return render_template("plot.html", script1=script1, div1=div1, cdn_js0=cdn_js0, cdn_js1=cdn_js1, cdn_js2=cdn_js2, cdn_js3=cdn_js3)

"""
Cancer
Circulatory_System
Digestive_System
Ear_Nose_and_Throat
Eye_Diseases
Genetic_Diseases
Haematological_Disorders
Infections_and_Infestations
Injury_Occupational_Diseases_Poisoning
Mental_and_Behavioural_Disorders
Musculoskeletal_Diseases
Neonatal_Diseases
Nervous_System_Diseases
Nutritional_Metabolic_Endocrine
Oral_Health
Pregnancy_and_Childbirth
Respiratory
Signs_and_Symptoms
Skin_and_Connective_Tissue_Diseases
Surgery
Urological_and_Genital_Diseases


Behavioural
Biological_and_Vaccine
Device
Drug
Genetic
Mixed
Other
Procedure_and_Surgery
Supplement

"""
if __name__ == "__main__":
    app.run(debug=True)