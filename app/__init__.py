import sys
sys.path.append('C:/Users/levan/Dropbox/PyCharmProjects/flaskapp')
from bokeh.embed import components
from flask import Flask, render_template, request, redirect
from flask_mail import Mail

# MySQL connection
# Warning! the password import must be above the connection import!!
from passwords import *
app = Flask(__name__)
mail = Mail()

# Blueprints import
from app.views.charts import charts_blueprint
from app.views.finance import finance_blueprint
from app.views.football import football_blueprint
from app.views.contact import contact_blueprint
from app.views.bio import bio_blueprint
from app.views.contact import contact_success_blueprint
from app.views.leo_markt import leo_markt_blueprint

# Tell flask you use the configuration from  config
app.config.from_object('config')

mail.init_app(app)

# Blueprints registers
app.register_blueprint(charts_blueprint)
app.register_blueprint(football_blueprint)
app.register_blueprint(finance_blueprint)
app.register_blueprint(contact_blueprint)
app.register_blueprint(bio_blueprint)
app.register_blueprint(contact_success_blueprint)
app.register_blueprint(leo_markt_blueprint)

# TODO Hide Static File
# TODO make Saridis Travel page


@app.route('/', methods = ['GET', 'POST'])
def homepage():
    title = 'Kelesidis Levan'
    from my_func.my_plots import coutinho, info ,finance

    p = coutinho()
    script, div = components(p)

    # Define the default chart ( 'TSLA' )
    f = finance('TSLA')
    info = info('TSLA')
    info = info.to_html(classes='info_table')
    script2, div2 = components(f)

    if request.method == 'POST':
        fin = str(request.form.get('chart')).upper()

        # open chart in a new window & redirect the page to the selected chart
        # otherwise it will returned to the top of index page
        return redirect('http://kelesidis.de/historical_data/%s' % fin)
        # return redirect('http://kelesidis.de/#finance_chart_index')

    # To prevent the loading of bokeh plots i add the next Jscript (check_width) which check if the screen
    # is less than 729px and if that is true stop Bokeh from loadig.

    # TODO make the bokeh func to start and stop interactive (screen size changes) 
    check_width = """
        var min_width = window.matchMedia( "(min-width: 729px)" );
        min_width.addListener(sizeChange);
        sizeChange(min_width);
            if(!min_width.matches) {
                console.log('Try to stop Bokeh');
                console.log('removed')
                return;
            }
    """

    script = script[:59] + check_width + script[60:]
    script2 = script2[:59] + check_width + script2[60:]

    return render_template('index.html', title = title, script2 = script2, div2 = div2,
 script = script, div = div, info = info)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
