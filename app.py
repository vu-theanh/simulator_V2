import streamlit as st
#File processing
from PIL import Image
import pandas as pd
import docx2txt
from PyPDF2 import PdfReader as PdfFileReader
import pdfplumber
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
import streamlit.components.v1 as components
import plotly.figure_factory as ff
import plotly.express as px

Page_config = {"page_title": " THE ANH VU", "layout": "wide", "initial_sidebar_state": "auto"}
st.set_page_config(**Page_config)



def main():
	st.header("Trade Zooms: Pro Trading Simulator")
	components.html(
	    """
		<a href=https://tradezooms.net/ target="_blank">Home Page</a>

		<style>
		a:link, a:visited {
		background-color: #f44336;
		color: white;
		padding: 15px 25px;
		text-align: center;
		text-decoration: none;
		display: inline-block;
		}

		a:hover, a:active {
		  background-color: red;
		}
		</style>

		<a href=https://tradezooms.net/cong-cu-giao-dich/ target="_blank">Free Trading Tool for MT4</a>

	    """,
		height=60
	)
	menu = ["Home","About Us"]
	choice = st.sidebar.selectbox("Menu", menu)

	if choice == "Home":
		st.subheader("Provide input of your strategy to simulate")

		with st.form("my_form"):
			col1, col2, col3, col4, col5, col6 = st.columns(6)
			submitted = st.form_submit_button("Calculate Now")
			with col1:
				deposit = st.number_input("Deposit", value = 1000)
			with col2:
				winrate = st.number_input("Win Rate %",min_value=0, max_value=100, value = 55)
			with col3:
				Risk = st.number_input("Risk per Trade %", min_value=0, max_value=100, value = 10)
			with col4:
				RR = st.number_input("Reward/Risk",min_value=0.0, value = 1.5)
			with col5:
				DD = st.number_input("Expected Draw Down %", min_value=10, max_value=100, value = 30)
			with col6:
				Trade = st.number_input("Trade Number", min_value=100, max_value=1000, value = 100)
			Winrate_cal =(winrate*RR)/(winrate*RR+100-winrate)
			A = Winrate_cal - (1-Winrate_cal)
			RoR = pow((1-A)/(1 + A), (DD/Risk))*100
			RoR = round(RoR, 3)
			if RoR > 100:
				RoR = 100
			st.write("Calculated Risk of Ruin {} %".format(RoR))

		result = []*Trade
		balance_list = [deposit]*Trade
		profit_list = [0]*Trade
		drawdown_list = [0]*Trade
		numberList = [-1,1]
		result= random.choices(numberList, weights= [100 - winrate, winrate], k=Trade)
		if submitted:
			result= random.choices(numberList, weights= [100 - winrate, winrate], k=Trade)
		# profit = []*4
		# st.write(len(profit))
		# st.write(profit)

		balance = deposit
		for x in range(len(result)):
			if result[x]>0:
				profit=result[x]*Risk/100*deposit*RR 
			else:
				profit=result[x]*Risk/100*deposit
			balance = balance + profit
			balance = round(balance,3)
			balance_list[x] = balance
			profit_list[x] = profit
			if x >=2 and (balance - max(balance_list[0:x]))/max(balance_list[0:x])*100 <0:
				
				drawdown_list[x] = (balance - max(balance_list[0:x]))/max(balance_list[0:x])*100
			else:
				drawdown_list[x]  = None

		df = pd.DataFrame(list(zip(result, balance_list, profit_list, drawdown_list)), columns = ["Win/Loose", "Balance", "Proft per Trade","Relative Drawdown"])



		if len(df) >0:
			st.subheader("Blance from Simulation Results")
			st.area_chart(df["Balance"], use_container_width=True)

			new_drawdown = list(filter(None, drawdown_list))
			maxdrawdown = min(new_drawdown)
			maxdrawdown = round(maxdrawdown, 2)
			st.subheader("Max calculated drawdown: {} %".format(maxdrawdown))

			

			drawdown_df = pd.DataFrame(new_drawdown, columns = ["Relative Drawdown"])
			fig = px.histogram(drawdown_df, x="Relative Drawdown")
			st.plotly_chart(fig, use_container_width=True)
			st.dataframe(df, use_container_width=True)





		# for i in range(len(result[0])):
		# 	st.write(result.iloc[0,i])



	components.html(
	    """
		<a href=https://tradezooms.net/cong-cu-giao-dich/ target="_blank">Come back to Home Page</a>

		<style>
		a:link, a:visited {
		background-color: #f44336;
		color: white;
		padding: 15px 25px;
		text-align: center;
		text-decoration: none;
		display: inline-block;
		}

		a:hover, a:active {
		  background-color: red;
		}
		</style>

	    """,
		height=60
	)

	st.write("Disclaimer: This tool provide you a quick estimate of your earnings, losses, risk of ruin and optimize risk per trade. But the result might be diferent from actual trades since trading fee and other inputs vary by brokers.")


if __name__ == '__main__':
	main()