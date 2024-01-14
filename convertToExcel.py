import pandas as pd
from datetime import datetime,timedelta
import xlsxwriter



def converting_excel(data):
# Convert the dictionary to a DataFrame
    
    df = pd.DataFrame.from_dict(data, orient='index')

    # Create a list to store all viable connections
    connections_data = []

    for key, entry in data.items():
        for other_key, other_entry in data.items():
            if entry['Ziel'] == other_entry['Start']:

                if other_entry['Preis'] == "N/A" or entry['Preis'] == "N/A" :
                    gesamtpreis = "N/A"
                else:

                    gesamtpreis = float(other_entry['Preis'].replace(",",".")) + float(entry['Preis'].replace(",","."))
                
                if entry["Ankunft"] < other_entry["Abfahrt"]:                    
                    
                    # Create a new entry for the connection
                    connection = {
                        'Start1': entry['Start'],
                        'Ziel1': entry['Ziel'],
                        'Abfahrt1': entry['Abfahrt'].strftime('%Y-%m-%d %H:%M'),
                        'Ankunft1': entry['Ankunft'].strftime('%Y-%m-%d %H:%M'),                        
                        'Start2': other_entry['Start'],
                        'Ziel2': other_entry['Ziel'],
                        'Abfahrt2': other_entry['Abfahrt'].strftime('%Y-%m-%d %H:%M'),
                        'Ankunft2': other_entry['Ankunft'].strftime('%Y-%m-%d %H:%M'),
                        'Preis1': entry['Preis'],
                        'Zug1': entry['Zug'],
                        'Preis2': other_entry['Preis'],
                        'Zug2': other_entry['Zug'],
                        'Dauer': (other_entry["Ankunft"] - entry['Abfahrt']).total_seconds()/60,
                        'Gesamtpreis':gesamtpreis,
                        'URL1':entry['URL'],
                        'URL2':other_entry['URL'],
                        
                    }
                    connections_data.append(connection)

    # Convert the connections data to a DataFrame
    connections_df = pd.DataFrame(connections_data)
    
    # Get the current date and time
    current_datetime = datetime.now().strftime('%Y-%m-%d_%Hh-%Mm-%Ss')
    
    #convert date time column to readable dates.
    df['Abfahrt'] = df['Abfahrt'].dt.strftime('%Y-%m-%d %H:%M')
    df['Ankunft'] = df['Ankunft'].dt.strftime('%Y-%m-%d %H:%M')
    # Save both DataFrames to an Excel file with the current date and time
    excel_filename = f'output_{current_datetime}.xlsx'
    
    with pd.ExcelWriter(excel_filename, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='OriginalData', index_label='Connection')
        connections_df.to_excel(writer, sheet_name='Connections', index_label='Connection')


        #zooming in both sheets since the standart is slightly to small for me
        for sheet in writer.sheets.values():
            sheet.set_zoom(120)
            sheet.autofilter(0, 0, 0, 16)



    print(f"Data has been saved to {excel_filename}")
