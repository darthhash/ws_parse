

import os
import io
import base64
import numpy as np 
import pandas as pd
import flask
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import os
from selenium import webdriver
import random
import datetime
import retrying
import pytz
from time import sleep
import pandas as pd
import requests
import asyncio
import base64
import time
from python_rucaptcha import ImageCaptcha,  RuCaptchaControl
from python_rucaptcha import errors
from bs4 import BeautifulSoup 
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import datetime
from time import sleep
import pandas as pd
import requests
import asyncio
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC
import base64
import time
from python_rucaptcha import ImageCaptcha,  RuCaptchaControl
from python_rucaptcha import errors
from bs4 import BeautifulSoup 
from retrying import retry


app = flask.Flask(__name__)
app.config['EXPLAIN_TEMPLATE_LOADING¶']=True
# TODO: A secret key is included in the sample so that it works but if you
# use this code in your application please replace this with a truly secret
# key. See http://flask.pocoo.org/docs/0.12/quickstart/#sessions.


@app.route('/')
def index():
    return flask.render_template('calculate.html')
@app.route('/', methods=['POST'])
def get_csv():
    words = flask.request.form['words']
    words=str(words)
    words=words.replace(' ','')
    words=words.split(',')
    df=load_to_df(words)
    resp = flask.make_response(df.to_csv())
    resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp
def get_tables_massive(words):
    n=0
    while n<10:
        try:
            n=+1
            login = 'yegorkholin'
            password = '123bugorka123'
            options = webdriver.ChromeOptions()
            options.add_argument("--headless") # Runs Chrome in headless mode.
            #options.add_argument('--no-sandbox') # # Bypass OS security model
            #options.add_argument('start-maximized')
            options.add_argument('disable-infobars')
            options.add_argument("--disable-extensions")
            browser=webdriver.Chrome(r'/home/egorholin/wordstat/chromedriver.exe', options=options)  
            url = "https://wordstat.yandex.ru/#!/history?period=weekly"
            browser.get(url)
            elem=browser.find_element_by_xpath('//a[@href="' + 'https://passport.yandex.ru/passport?mode=auth&msg=&retpath=https%3A%2F%2Fwordstat.yandex.ru%2F' + '"]')
            elem.click()
            elem=browser.find_element_by_id('b-domik_popup-username')
            elem.send_keys(login)
            sleep(random.randint(5, 10)/10)
            elem=browser.find_element_by_id('b-domik_popup-password')
            elem.send_keys(password)
            sleep(random.randint(5, 10)/10)
            button = browser.find_element_by_css_selector('span.b-form-button_valign_middle:nth-child(1)')
            sleep(random.randint(5, 10)/10)
            button.click()
            sleep(random.randint(5, 10)/10) 
            captcha = browser.find_element_by_css_selector('td[class="b-popupa__image-td"]')
            sleep(random.randint(5, 10)/10)
            soup=BeautifulSoup(captcha.get_attribute('innerHTML'),'html.parser')
            print(captcha.get_attribute('innerHTML'))
            captcha_link='https:'+soup.img['src']
            print(captcha_link)
            user_answer_temp = ImageCaptcha.ImageCaptcha(
            rucaptcha_key='0854df904af0d822315b96b6b0d210ef', save_format="temp"
            ).captcha_handler(captcha_link=captcha_link)
            answer=str(user_answer_temp['captchaSolve'])
            sleep(random.randint(5, 10)/10)
            elem = browser.find_elements_by_css_selector('input[class="b-form-input__input"]')[1]
            elem.send_keys(answer)
            sleep(random.randint(5, 10)/5)
            button2=browser.find_elements_by_css_selector('input[class="b-form-button__input"]')[1]
            sleep(random.randint(5, 10)/5)
            button2.click()
            sleep(random.randint(5, 10)/5)
            sleep(random.randint(5, 10)/10)
#             elem=browser.find_elements_by_css_selector('input[class="b-form-input__input"]')[0]
#             sleep(random.randint(5, 10)/10)
#             elem.send_keys('test')
#             sleep(random.randint(5, 10)/10)
#             button3=browser.find_elements_by_css_selector('input[class="b-form-button__input"]')[0]
#             button3.click()
#             browser.find_elements_by_css_selector('input[class="b-form-input__input"]')[0].clear()
            print (' captcha has been solved ')
            for word in words:
                k=0
                while k<5:
                    try:
                        
                        sleep(random.randint(5, 10)/10)
                        elem=browser.find_elements_by_css_selector('input[class="b-form-input__input"]')[0]
                        sleep(random.randint(5, 10)/10)
                        elem.send_keys(word)
                        sleep(random.randint(5, 10)/10)
                        button3=browser.find_elements_by_css_selector('input[class="b-form-button__input"]')[0]
                        button3.click()
                        sleep(random.randint(5, 10)/15)
                        sleep(random.randint(5, 10)/6)
                        element=WebDriverWait(browser, 30).until_not(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.b-spin.b-spin_size_45.b-spin_theme_grey-45.b-spin_progress_yes.i-bem.b-spin_js_inited')))
                        sleep(random.randint(5, 10)/6)
                        content=browser.page_source
                        soup = BeautifulSoup(content, 'html.parser')
                        dates1=[]
                        numbers1 = []
                        for text in soup.find_all("tr", class_=["even","odd"]):
                            dates1.append(text.find("td").text)
                            numbers1.append(text.find("td", class_="b-history__value-td").text)
                        for n in range(len(numbers1)):
                            numbers1[n]=int(numbers1[n])
                        browser.find_elements_by_css_selector('input[class="b-form-input__input"]')[0].clear()
                        data=pd.DataFrame()
                        data['dates']=dates1
                        data[['First', 'Last']]=data.dates.str.split("-", n = 1, expand=True)
                        data['First']=pd.to_datetime(data['First'],dayfirst=True)
                        data['Last']=pd.to_datetime(data['Last'],dayfirst=True)
                        data=data.drop(columns='dates')
                        data['numbers']=numbers1
                        data['brand']=word
                        products[word]=data
                        print ('{} is parsed '.format(word))
                        print(data['numbers'][0])
                        break
                    except Exception as e:
                        print(e)
                        continue
            
            break
        except Exception as e:
            print(e)
            browser.quit()
            continue
    browser.quit()
    return products
def load_to_df(words):
    s=get_tables_massive(words)
    #products=s
    final=pd.DataFrame()
    #for n in products.keys():
    for n in s.keys():
        final=pd.concat([final, s[n]], sort=True)
    return final



# @app.route('/', methods=['POST'])
# # def my_form_post():
# #     c

# def plot_png():
#     confidence_level=float(flask.request.form['confidence_level'])
#     segment_size=float(flask.request.form['segment_size'])
#     coversion_rate=float(flask.request.form['coversion_rate'])
#     #return '<img width="600" height="600" src="data:image/png;base64,{}">'.format(plot_url)
#     return flask.redirect(flask.url_for('plot', cf=confidence_level, ss=segment_size,cr= coversion_rate))
#     # return flask.Response(output.getvalue(), mimetype='image/png')



# @app.route('/plot')
# def plot():
#     cf=float(flask.request.args.get('cf', None))
#     ss=float(flask.request.args.get('ss', None))
#     cr=float(flask.request.args.get('cr', None))
#     fig = plot_delta_and_sample(cf, ss, cr)
#     canvas = FigureCanvas(fig)
#     img = io.BytesIO()
#     fig.savefig(img, format='png')
#     img.seek(0)

#     plot_url = base64.b64encode(img.getvalue()).decode()
    
#     # return flask.render_template('result')
#     return flask.render_template('result.html', plot_url=plot_url, cf=cf, ss=ss, cr=cr)
#     # return '<img width="600" height="600" src="data:image/png;base64,{}">'.format(plot_url)
# def plot_delta_and_sample(p, s=1000000, t=0.0234):
#     fig = plt.Figure(figsize=[10,10])
#     axis = fig.add_subplot(1, 1, 1)
#     x = np.linspace(0,20000,100) 
#     z_test=norm.ppf(p)
#     y = z_test*np.sqrt(((0.5*0.5)/x)*(s-x)/(s-1))

#     _=axis.plot(x,y)
#     #plt.xlim(-3,3)
#     #plt.ylim(-3,3)

#     _=axis.set_xlabel("sample-size")
#     _=axis.set_ylabel("delta")
    
#     return fig

# @app.route('/download')
# def download():
#     cf=float(flask.request.args.get('cf', None))
#     ss=float(flask.request.args.get('ss', None))
#     cr=float(flask.request.args.get('cr', None))
#     final_df=dataframe(cf, ss, cr)
#     resp = flask.make_response(final_df.to_csv())
#     resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
#     resp.headers["Content-Type"] = "text/csv"
#     return resp
# def dataframe(p,s=1000000,baseline=0.0234, step=1000):
    
#     delta_min=[]
#     delta_max=[]
#     sample_size=[]
#     final_massive=[]
#     for x in np.arange(0,20000,step): #x - sample_size
#         z_test=norm.ppf(p) #ztest critical value
#         y = z_test*np.sqrt(((0.5*0.5)/x)*(s-x)/(s-1)) #y - delta
#         delta_min=baseline-baseline*y
#         delta_max=baseline+baseline*y
#         sample_size=x
#         final_massive.append([delta_min,delta_max,sample_size])
#     final_df=pd.DataFrame(final_massive)
#     final_df.columns=['CR_max', 'CR_min', 'sample_size']
#     return final_df





if __name__ == '__main__':
    # When running locally with Flask's development server this disables
    # OAuthlib's HTTPs verification. When running in production with a WSGI
    # server such as gunicorn this option will not be set and your application
    # *must* use HTTPS.
    
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run(host='0.0.0.0')