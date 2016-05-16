from bokeh.embed import components
from flask import Flask, render_template, request, redirect, abort, url_for
# from flask.ext.sqlalchemy import SQLAlchemy


### Unused imports ###
# import pandas as pd
# import datetime
# #import pygal
# # from bokeh.charts import Line, output_file
# from bokeh.models import HoverTool
#
#
# from bokeh.plotting import figure
# import pandas.io.data as web
# from bokeh.models.sources import ColumnDataSource
###           ###                 ###



app = Flask(__name__)

try:
    @app.route('/static/')
    def static():
        return render_template('index.html')
except:

    pass



@app.route('/', methods = ['GET', 'POST'])
def homepage():
    title = 'home'

    if request.method == 'POST':
        f= request.files['the_file']
        f.save('C:\Users\levan\Desktop')


    return render_template('index.html', title = title)

@app.route('/coutinho/')
def pandasPage():
    title = 'Liverpool YNWA'

    from my_func.my_plots import liverpool as lp

    l = lp()
    script, div = components(l)


    return render_template('football/en/epl/liverpool/coutinho.html',
                           title = title, script = script, div = div)

@app.route('/charts/')
def charts():
    title = 'Charts'

    from my_func.my_plots import HLevelLine as hl
    p = hl()
    script, div = components(p)

    #########################################################

    from my_func.my_plots import PygalLine as pgl

    line_chart = pgl()
    graph_data = line_chart.render_data_uri()


    return render_template('charts.html', title = title, graph_data = graph_data, script = script, div = div,)

@app.route('/finance/', methods = ["GET", "POST"])
def finance():
    title = 'finance'

    from my_func.my_plots import finance, info

    f = finance()
    info = info()
    info  = info.to_html(classes='info_table')

    script, div = components(f)

    return render_template('finance.html', title = title, script = script, div = div, info = info)


# with app.test_request_context():
#     print (url_for('static'  css/'))



if __name__ == "__main__":
    app.run(debug=True)





