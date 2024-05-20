    #DATA COLLECTION OF WEEKLY PRICES

import pandas as pd
from pyscript import when, display

    def testapp():
        # URL of the CSV file
        url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTXhlKNrUGCScq7nuJa81RJLGJ6KxuXyAi3fGA2a46gXYP9fhlG6Yi0GdUipZbAzYSQ4GqFsN_q67F8/pub?gid=1053518510&single=true&output=csv"

        # Send a GET request to the URL

        weekly_price = pd.read_csv("data.csv")
        weekly_price = weekly_price[::-1]
        weekly_price['Week'] = range(0, -len(weekly_price), -1)
        weekly_price.set_index('Week', inplace=True)
        weekly_price = weekly_price.drop(columns=['Date'])
        input_list = weekly_price.columns.values.tolist()
        input_list_df = pd.DataFrame(input_list, columns=['Stocks'])
        dfmain = pd.DataFrame()
        pd.options.mode.chained_assignment = None
        for i in range(len(weekly_price.columns)):
            stock_name = weekly_price.columns[i]
            data = weekly_price[[stock_name]]
    
            # Current Price of the Stock
            week_0 = data.iloc[0].values
    
            # Price of previous 6 weeks
            prev_6_weeks = data.iloc[0:7]
    
            # Percentage change
            prev_6_weeks = prev_6_weeks[::-1]
            prev_6_weeks['Percentage Change'] = prev_6_weeks[stock_name].pct_change()*100
            prev_6_weeks['Percentage Change'] = prev_6_weeks['Percentage Change']
            prev_6_weeks = prev_6_weeks[::-1]
            a = []
            b = []
            positive_change = 0
            negative_change = 0
            for o in range(0, len(prev_6_weeks), 1):
    
                price_temp = prev_6_weeks[[stock_name]].iloc[o].item()
                a.append(round(price_temp, 2))
                to_float = prev_6_weeks[['Percentage Change']].iloc[o].item()
                if (to_float > 0):
                    positive_change = positive_change + 1
                elif (to_float < 0):
                    negative_change = negative_change + 1
                else:
                    pass
                percent = str(round(to_float, 2)) + "%"
                b.append(percent)
            total_change = a[0] - a[len(prev_6_weeks)-1]
    
            # The maximum & minimum price in the entire year
            max_ey = data[stock_name].max()
            min_ey = data[stock_name].min()
            maxima_index = []
            minima_index = []
    
            # Relation of CP with Max/Min
            relation_max = (((max_ey-week_0)/week_0)*100).round(2)
            relation_min = (((min_ey-week_0)/week_0)*100).round(2)
            if (relation_max == 0):
                relation_max = "Equal to Maximum Price"
            if (relation_min == 0):
                relation_min = "Equal to Minimum Price"
    
            # Relation of CP with Maxima & Minima
            # Find all maxima and minima
            data["Maxima"] = ""
            data["Minima"] = ""
            for j in range(6, len(data)-6):
                if (data[stock_name].iloc[j] >= data[stock_name].iloc[j-6:j].max() and data[stock_name].iloc[j] >= data[stock_name].iloc[j:j+6].max()):
                    data['Maxima'].iloc[j] = True
                else:
                    data['Maxima'].iloc[j] = False
                if (data[stock_name].iloc[j] <= data[stock_name].iloc[j-6:j].min() and data[stock_name].iloc[j] <= data[stock_name].iloc[j:j+6].min()):
                    data['Minima'].iloc[j] = True
                else:
                    data['Minima'].iloc[j] = False
    
            # Store the indexes of Maxima and Minima
            for k in range(0, len(data)):
                if (data['Maxima'].iloc[k] == True):
                    maxima_index.append(k)
    
            for l in range(0, len(data)):
                if (data['Minima'].iloc[l] == True):
                    minima_index.append(l)
            max_differences = []
            min_differences = []
            # Find the closest maxima and minima to the current price
            import numpy as np
            for m in range(len(maxima_index)):
                max_differences.append(
                    np.abs(data[stock_name].iloc[maxima_index[m]] - week_0))
            if (len(maxima_index) != 0):
                closest_maxima_index = np.argmin(max_differences)
                closest_maxima = data[stock_name].iloc[maxima_index[closest_maxima_index]]
            for n in range(len(minima_index)):
                min_differences.append(
                    np.abs(data[stock_name].iloc[minima_index[n]] - week_0))
            if (len(minima_index) != 0):
                closest_minima_index = np.argmin(min_differences)
                closest_minima = data[stock_name].iloc[minima_index[closest_minima_index]]
    
            # Relation of CP with Closest Maxima & Minima
            if (len(maxima_index) == 0):
                relation_closest_maxima = "No Maxima"
            else:
                relation_closest_maxima = (((closest_maxima-week_0)/week_0)*100).round(2)
            if (len(minima_index) == 0):
                relation_closest_minima = "No Minima"
            else:
                relation_closest_minima = (((closest_minima-week_0)/week_0)*100).round(2)
    
            # Category 1 LP/SP/IP
            if (total_change > 0 and positive_change > 2):
                category1 = "LP"
            elif (total_change < 0 and negative_change > 2):
                category1 = "SP"
            else:
                category1 = "IP"
    
            # Category 2 L/S
            comp_max = 1.05*week_0
            comp_min = 0.95*week_0
            if (category1 != "IP"):
                if (category1 == "LP"):
                    if(week_0==max_ey):
                        category2 = "L"
                    elif(len(maxima_index)>0 and closest_maxima<=comp_max):
                        category2 = "Rejected LP"
                    else: category2 = "L"
                elif (category1 == "SP"):
                    if(week_0==min_ey):
                        category2 = "S"
                    elif(len(minima_index)>0 and closest_minima>=comp_min):
                        category2 = "Rejected SP"
                    else: category2 = "S"
    
            else:
                category2 = "N/A"
    
            # Create a DataFrame with the variables
            data1 = {
                'Stock_Name': stock_name,
                'Week 0 Price': week_0,
                'Week -1 Price': a[1],
                'Week -2 Price': a[2],
                'Week -3 Price': a[3],
                'Week -4 Price': a[4],
                'Week -5 Price': a[5],
                'Week -6 Price': a[6],
                'Week 0 Percent Change': b[0],
                'Week -1 Percent Change': b[1],
                'Week -2 Percent Change': b[2],
                'Week -3 Percent Change': b[3],
                'Week -4 Percent Change': b[4],
                'Week -5 Percent Change': b[5],
                'Maximum Price in a year': max_ey,
                'Minimum Price in a year': min_ey,
                'Closest Maxima': closest_maxima,
                'Closest Minima': closest_minima,
                'Relation of CP with Maximum Price': relation_max,
                'Relation of CP with Minimum Price': relation_min,
                'Relation of CP with Closest Maxima': relation_closest_maxima,
                'Relation of CP with Closest Minima': relation_closest_minima,
                'Category 1': category1,
                'Category 2': category2
    
    
            }
            df = pd.DataFrame(data1, index=[0])
            dfmain = pd.concat([dfmain, df])
    
        List_L = pd.DataFrame()
        List_S = pd.DataFrame()
        # Save the DataFrame to a CSV file
        # dfmain.to_csv('Report.csv', index=False)
        for i in range(0, len(dfmain)):
            if (dfmain['Category 2'].iloc[i] == 'L'):
                List_L = pd.concat([List_L, dfmain.iloc[[i]]])
                List_l_col = List_L[['Stock_Name']].reset_index(drop=True)
                list_l_col_df = pd.DataFrame(List_l_col)
            elif (dfmain['Category 2'].iloc[i] == 'S'):
                List_S = pd.concat([List_S, dfmain.iloc[[i]]])
                List_s_col = List_S[['Stock_Name']].reset_index(drop=True)
                list_s_col_df = pd.DataFrame(List_s_col)
    
        # List_l_col.to_csv('list_l_col.csv', index=False)
        # List_s_col.to_csv('list_s_col.csv', index=False)
        return list_l_col_df, list_s_col_df, input_list_df


    @when("click", "#us_show_input")
    def show_input_stock_list():
        List_L, List_S, input_list = testapp()
        display(input_list, append="False")
    @when("click", "#runEngineus")    
    def run_engine():
        List_L, List_S, input_list = testapp()
        display(List_L , append="False")
        display(List_S , append="False")
# # pyscript._generator.file_to_html("ind.py", "ind1.html",output_path="ind1.html")