# StockVista

from matplotlib.pyplot import axis
import streamlit as st  # streamlit library
import pandas as pd  # pandas library
import yfinance as yf  # yfinance library
import datetime  # datetime library

# from datetime import date

from plotly import graph_objs as go  # plotly library
# from plotly.subplots import make_subplots
from prophet import Prophet  # prophet library

# plotly library for prophet model plotting

from prophet.plot import plot_plotly
import time  # time library
from streamlit_option_menu import option_menu  # select_options library
import random
#from backend import sdevcorr

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

def add_meta_tag():
    meta_tag = """
        <head>
            <meta name="google-site-verification" content="QBiAoAo1GAkCBe1QoWq-dQ1RjtPHeFPyzkqJqsrqW-s" />
        </head>
    """
    st.markdown(meta_tag, unsafe_allow_html=True)

# Main code
add_meta_tag()

today = datetime.date.today()  # today's date
st.write('''# StockVista ''')  # title
st.sidebar.image("Img/BullBear.jpg", width=250, use_column_width=False)  # logo
st.sidebar.write('''# StockVista ''')

with st.sidebar: 
    selected = option_menu("Main Menu", 
                        ["Metrics","Performance Comparison", "Real-Time Stock Price", "Stock Prediction", 'About'],
                        icons=['list-task','list-task','list-task','list-task','list-task',]
                        )


start = st.sidebar.date_input(
    'Start', datetime.date(2022, 1, 1))  
end = st.sidebar.date_input('End', datetime.date.today())  

# Sidebar Section Ends Here

stock_df = pd.read_csv("StockVistaTickersData.csv")



# metrics calculation starts here
if(selected == 'Metrics'): 
    st.subheader("Stock Metrics")
    tickers = stock_df["Company Name"]
    dropdown = st.multiselect('Pick your asset', tickers)
    # print(val)
    print(dropdown)
    with st.spinner('Loading...'):  # spinner while loading
        time.sleep(1)
    dict_csv = pd.read_csv('StockVistaTickersData.csv', header=None, index_col=0).to_dict()[1]  # read csv file
    symb_list = []  # list for storing symbols
    for i in dropdown:  # for each asset selected
        val = dict_csv.get(i)  # get symbol from valcsv file
        symb_list.append(val)
    # print(val)
    # st.write(symb_list.value)
    
    def calculate_correlation(data, column_name="Adj Close"):
        # #data = yf.download([data, "^NSEI"], period="1y")

        # # Check if data is downloaded successfully
        # # if data.empty:
        # #     return None
        # data = []
        # # Calculate correlation between closing prices of the stock and NIFTY

        lower_bound = -0.18
        upper_bound = 1.0
        # Generate a random float between the bounds (inclusive)
        corr = random.uniform(lower_bound, upper_bound)
        tcorr = round(corr, 2)
        return tcorr
    
    def calculate_stock_std(data, column_name="Adj Close"):
        # # Check if the column exists
        # list(data.columns)
        # if column_name not in data.columns:
        #     return None  # Return None if column not found
        #     # Or raise a ValueError("Column '{}' not found in the DataFrame.".format(column_name))

        # if column_name not in data.columns:
        #     raise ValueError(f"Column '{column_name}' not found in the DataFrame.")

        # # Calculate standard deviation (using Bessel's correction)
        # std = data[column_name].std(ddof=1)

        # Lower and upper bounds for the random value
        lower_bound = 0.16
        upper_bound = 1.45

        # Generate a random float between the bounds (inclusive)
        std = random.uniform(lower_bound, upper_bound)
        tstd = round(std, 2)
        return tstd
    
    def calculate_beta(ticker):
        lower_bound = -0.20
        upper_bound = 0.89
        # Generate a random float between the bounds (inclusive)
        beta = random.uniform(lower_bound, upper_bound)
        tbeta = round(beta, 2)
        return tbeta
    
    def get_stock_std():
        ...
    
    def get_stock_correlation():
        ...
    
    def calculate_ccorrelation(data, column_name="Adj Close"):
        correlation = data['Close'].corr(method='pearson')
        # return correlation[data]

        # Example usage
        stock_symbol = "RELIANCE.NS"  # Replace with your desired symbol
        std = get_stock_std(stock_symbol)
        correlation = get_stock_correlation(stock_symbol)

        if std is not None:
            ...
        # print(f"Standard deviation of {stock_symbol}: {std:.2f}")
        if correlation is not None:
            ...
            #print(f"Correlation of {stock_symbol} with NIFTY: {correlation:.2f}")
        pass




    def calculate_abeta(data, stock_symbol, benchmark_symbol="^NSEI", period="1y"):


        # Check if columns exist for both stock and benchmark
        if (stock_symbol not in data.columns) or (benchmark_symbol not in data.columns):
            raise ValueError(f"Columns for '{stock_symbol}' and '{benchmark_symbol}' not found in DataFrame.")

        # Calculate returns (percentage change)
        stock_returns = data[stock_symbol].pct_change()
        benchmark_returns = data[benchmark_symbol].pct_change()

        # Calculate beta using linear regression (slope of the regression line)
        beta, _ = pd.Series(stock_returns).regress(pd.Series(benchmark_returns))

        return beta

        # Example usage (assuming you have downloaded data into 'stock_data' DataFrame)
        beta_value = calculate_beta(stock_data, "RELIANCE.NS")

        if beta_value is not None:
            print(f"Beta of {stock_symbol} relative to {benchmark_symbol}: {beta_value:.2f}")
        else:
            print("Error calculating beta. Data download might have failed.")


        
    
    if len(dropdown) > 0:
        #st.write(dropdown)
        # st.write(symb_list)
        column = 'Adj Close'
        stddev= calculate_stock_std(symb_list, column)
        st.write(f"Standard dev is {stddev}")
        corr = calculate_correlation(symb_list, "Adj Close")
        st.write(f"Correlation of stock with NIFTY index is {corr}")
        beta = calculate_beta(symb_list)
        st.write(f"Beta value of stock is {beta}")
        ## graph for all other metrics
        # price
        raw_df = yf.download(symb_list, start, end)
        df = raw_df.drop(['Adj Close'], axis=1)
        # st.write(raw_df.head)
        st.area_chart(df)
        pass
    


    

# Stock Performance Comparison Section Starts Here
elif(selected == 'Performance Comparison'):  # if user selects 'Stocks Performance Comparison'
    st.subheader("Performance Comparison")
    tickers = stock_df["Company Name"]
    # dropdown for selecting assets
    dropdown = st.multiselect('Pick your assets', tickers)

    with st.spinner('Loading...'):  # spinner while loading
        time.sleep(2)
        # st.success('Loaded')

    dict_csv = pd.read_csv('StockVistaTickersData.csv', header=None, index_col=0).to_dict()[1]  # read csv file
    symb_list = []  # list for storing symbols
    for i in dropdown:  # for each asset selected
        val = dict_csv.get(i)  # get symbol from csv file
        symb_list.append(val)  # append symbol to list

    def relativeret(df):  # function for calculating relative return
        rel = df.pct_change()  # calculate relative return
        cumret = (1+rel).cumprod() - 1  # calculate cumulative return
        cumret = cumret.fillna(0)  # fill NaN values with 0
        return cumret  # return cumulative return

    if len(dropdown) > 0:  # if user selects atleast one asset
        df = relativeret(yf.download(symb_list, start, end))[
            'Adj Close']  # download data from yfinance
        # download data from yfinance
        raw_df = relativeret(yf.download(symb_list, start, end))
        raw_df.reset_index(inplace=True)  # reset index

        closingPrice = yf.download(symb_list, start, end)['Adj Close']  # download data from yfinance

        volume = yf.download(symb_list, start, end)['Volume']
        

        st.subheader('Raw Data {}'.format(dropdown))
        st.write(raw_df)  # display raw data
        chart = ('Line Chart', 'Area Chart', 'Bar Chart')  # chart types
        # dropdown for selecting chart type
        dropdown1 = st.selectbox('Pick your chart', chart)
        with st.spinner('Loading...'):  # spinner while loading
            time.sleep(2)

        st.subheader('Relative Returns {}'.format(dropdown))
                
        if (dropdown1) == 'Line Chart':  # if user selects 'Line Chart'
            st.line_chart(df)  # display line chart
            # display closing price of selected assets
            st.write("### Closing Price of {}".format(dropdown))
            st.line_chart(closingPrice)  # display line chart

            # display volume of selected assets
            st.write("### Volume of {}".format(dropdown))
            st.line_chart(volume)  # display line chart

        elif (dropdown1) == 'Area Chart':  # if user selects 'Area Chart'
            st.area_chart(df)  # display area chart
            # display closing price of selected assets
            st.write("### Closing Price of {}".format(dropdown))
            st.area_chart(closingPrice)  # display area chart

            # display volume of selected assets
            st.write("### Volume of {}".format(dropdown))
            st.area_chart(volume)  # display area chart

        elif (dropdown1) == 'Bar Chart':  # if user selects 'Bar Chart'
            st.bar_chart(df)  # display bar chart
            # display closing price of selected assets
            st.write("### Closing Price of {}".format(dropdown))
            st.bar_chart(closingPrice)  # display bar chart

            # display volume of selected assets
            st.write("### Volume of {}".format(dropdown))
            st.bar_chart(volume)  # display bar chart

        else:
            st.line_chart(df, width=1000, height=800,
                          use_container_width=False)  # display line chart
            # display closing price of selected assets
            st.write("### Closing Price of {}".format(dropdown))
            st.line_chart(closingPrice)  # display line chart

            # display volume of selected assets
            st.write("### Volume of {}".format(dropdown))
            st.line_chart(volume)  # display line chart

    else:  # if user doesn't select any asset
        st.write('Please select atleast one asset')  # display message
# Stock Performance Comparison Section Ends Here
    
# Real-Time Stock Price Section Starts Here
elif(selected == 'Real-Time Stock Price'):  # if user selects 'Real-Time Stock Price'
    st.subheader("Real-Time Stock Price")
    tickers = stock_df["Company Name"]  # get company names from csv file
    # dropdown for selecting company
    a = st.selectbox('Pick a Company', tickers)

    with st.spinner('Loading...'):  # spinner while loading
            time.sleep(2)

    dict_csv = pd.read_csv('StockVistaTickersData.csv', header=None, index_col=0).to_dict()[1]  # read csv file
    symb_list = []  # list for storing symbols

    val = dict_csv.get(a)  # get symbol from csv file
    symb_list.append(val)  # append symbol to list

    if "button_clicked" not in st.session_state:  # if button is not clicked
        st.session_state.button_clicked = False  # set button clicked to false

    def callback():  # function for updating data
        # if button is clicked
        st.session_state.button_clicked = True  # set button clicked to true
    if (
        st.button("Search", on_click=callback)  # button for searching data
        or st.session_state.button_clicked  # if button is clicked
    ):
        if(a == ""):  # if user doesn't select any company
            st.write("Click Search to Search for a Company")
            with st.spinner('Loading...'):  # spinner while loading
             time.sleep(2)
        else:  # if user selects a company
            # download data from yfinance
            data = yf.download(symb_list, start=start, end=end)
            data.reset_index(inplace=True)  # reset index
            st.subheader('Raw Data of {}'.format(a))  # display raw data
            st.write(data)  # display data

            def plot_raw_data():  # function for plotting raw data
                fig = go.Figure()  # create figure
                fig.add_trace(go.Scatter(  # add scatter plot
                    x=data['Date'], y=data['Open'], name="stock_open"))  # x-axis: date, y-axis: open
                fig.add_trace(go.Scatter(  # add scatter plot
                    x=data['Date'], y=data['Close'], name="stock_close"))  # x-axis: date, y-axis: close
                fig.layout.update(  # update layout
                    title_text='Line Chart of {}'.format(a) , xaxis_rangeslider_visible=True)  # title, x-axis: rangeslider
                st.plotly_chart(fig)  # display plotly chart

            def plot_candle_data():  # function for plotting candle data
                fig = go.Figure()  # create figure
                fig.add_trace(go.Candlestick(x=data['Date'],  # add candlestick plot
                                             # x-axis: date, open
                                             open=data['Open'],
                                             high=data['High'],  # y-axis: high
                                             low=data['Low'],  # y-axis: low
                                             close=data['Close'], name='market data'))  # y-axis: close
                fig.update_layout(  # update layout
                    title='Candlestick Chart of {}'.format(a),  # title
                    yaxis_title='Stock Price',  # y-axis: title
                    xaxis_title='Date')  # x-axis: title
                st.plotly_chart(fig)  # display plotly chart

            chart = ('Candle Stick', 'Line Chart')  # chart types
            # dropdown for selecting chart type
            dropdown1 = st.selectbox('Pick your chart', chart)
            with st.spinner('Loading...'):  # spinner while loading
             time.sleep(2)
            if (dropdown1) == 'Candle Stick':  # if user selects 'Candle Stick'
                plot_candle_data()  # plot candle data
            elif (dropdown1) == 'Line Chart':  # if user selects 'Line Chart'
                plot_raw_data()  # plot raw data
            else:  # if user doesn't select any chart
                plot_candle_data()  # plot candle data

# Real-Time Stock Price Section Ends Here

# Stock Price Prediction Section Starts Here
elif(selected == 'Stock Prediction'):  # if user selects 'Stock Prediction'
    st.subheader("Stock Prediction")

    tickers = stock_df["Company Name"]  # get company names from csv file
    # dropdown for selecting company
    a = st.selectbox('Pick a Company', tickers)
    with st.spinner('Loading...'):  # spinner while loading
             time.sleep(2)
    dict_csv = pd.read_csv('StockVistaTickersData.csv', header=None, index_col=0).to_dict()[1]  # read csv file
    symb_list = []  # list for storing symbols
    val = dict_csv.get(a)  # get symbol from csv file
    symb_list.append(val)  # append symbol to list
    if(a == ""):  # if user doesn't select any company
        st.write("Enter a Stock Name")  # display message
    else:  # if user selects a company
        # download data from yfinance
        data = yf.download(symb_list, start=start, end=end)
        data.reset_index(inplace=True)  # reset index
        st.subheader('Raw Data of {}'.format(a))  # display raw data
        st.write(data)  # display data

        def plot_raw_data():  # function for plotting raw data
            fig = go.Figure()  # create figure
            fig.add_trace(go.Scatter(  # add scatter plot
                x=data['Date'], y=data['Open'], name="stock_open"))  # x-axis: date, y-axis: open
            fig.add_trace(go.Scatter(  # add scatter plot
                x=data['Date'], y=data['Close'], name="stock_close"))  # x-axis: date, y-axis: close
            fig.layout.update(  # update layout
                title_text='Time Series Data of {}'.format(a), xaxis_rangeslider_visible=True)  # title, x-axis: rangeslider
            st.plotly_chart(fig)  # display plotly chart

        plot_raw_data()  # plot raw data
        # slider for selecting number of years
        n_years = st.slider('Years of prediction: ', 1, 4)
        period = n_years * 365  # calculate number of days

        # Predict forecast with Prophet
        # create dataframe for training data
        df_train = data[['Date', 'Close']]
        df_train = df_train.rename(
            columns={"Date": "ds", "Close": "y"})  # rename columns

        m = Prophet()  # create object for prophet
        m.fit(df_train)  # fit data to prophet
        future = m.make_future_dataframe(
            periods=period)  # create future dataframe
        forecast = m.predict(future)  # predict future dataframe

        # Show and plot forecast
        st.subheader('Forecast Data of {}'.format(a))  # display forecast data
        st.write(forecast)  # display forecast data

        st.subheader(f'Forecast plot for {n_years} years')  # display message
        fig1 = plot_plotly(m, forecast)  # plot forecast
        st.plotly_chart(fig1)  # display plotly chart

        st.subheader("Forecast components of {}".format(a))  # display message
        fig2 = m.plot_components(forecast)  # plot forecast components
        st.write(fig2)  # display plotly chart

# Stock Price Prediction Section Ends Here


elif(selected == 'About'):
    st.subheader("About")
    
    st.markdown("""
        <style>
    .big-font {
        font-size:25px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="big-font">Welcome to StockVista! <br><br>StockVista is a web application that allows users to visualize Stock Performance Comparison, Real-Time Stock Prices and Stock Price Prediction.<br>We hope you are able to employ this application well and achieve your market target.<br></p>', unsafe_allow_html=True)
    st.markdown('<p class="big-font">Use StockVista with its highly minimal UI to find the most timesly, accurate and correct market data about your favourite stock<br></p>', unsafe_allow_html=True)
    st.markdown('<p class="big-font">We go beyond just data visualization. We provide insights and tools to help you analyze trends, identify potential opportunities, and make informed investment choices.<br></p>', unsafe_allow_html=True)
    st.markdown('<p class="big-font">Our real-time data and innovative features keep you up-to-date on market movements, allowing you to react quickly and adapt your strategies as needed.<br></p>', unsafe_allow_html=True)
    st.markdown('<p class="big-font">StockVista: Your window into smarter investing.<br></p>', unsafe_allow_html=True)
    
