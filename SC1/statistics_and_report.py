import pandas as pd
import numpy as np
import matplotlib.pyplot  as plt
plt.rcParams['font.size'] = 20
plt.rcParams['figure.figsize'] = [20, 10]
plt.rcParams['figure.dpi'] = 200
plt.rcParams['axes.grid'] = True
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

folder_path = os.getcwd()


def store_data(df1, data_start, data_end, mission_name):
    print('Storing data')
    results_dir = os.path.join(folder_path, 'Exports/', mission_name+'_'+data_start+'_to_'+data_end+'_export.csv')
    print('Success')
    df1.to_csv(results_dir, index=True)
    return results_dir


def get_sts(df1, all_point_export,valid_point_export, np_isc_ovg, sp_isc_ovg):
    print('Getting stats')
    str_max = df1[(df1['sun_lit']==True)]['sum_str'].max()
    str_min = df1[(df1['sun_lit']==True)]['sum_str'].min()
    voc_max = np.round(df1[(df1['sun_lit']==True)]['cell_temp'].max(),2)
    voc_min = np.round(df1[(df1['sun_lit']==True)]['cell_temp'].min(),2)
    df_exp = pd.DataFrame(columns=['Parameter', 'Min', 'Max'])
    df_exp.loc[len(df_exp.index)] = ['Strs on during sunlit', str_min, str_max] 
    df_exp.loc[len(df_exp.index)] = ['SAGS error (in %)', all_point_export[0], all_point_export[1]] 
    df_exp.loc[len(df_exp.index)] = ['SAGS error at non-polar points (in %)', valid_point_export[0], valid_point_export[1]]
    df_exp.loc[len(df_exp.index)] = ['Voc cell temp during sunlit', voc_min, voc_max] 
    df_exp.loc[len(df_exp.index)] = ['North pole Isc overgeneration (in mA)', np_isc_ovg[0], np_isc_ovg[1]]
    df_exp.loc[len(df_exp.index)] = ['South pole Isc overgeneration (in mA)', sp_isc_ovg[0], sp_isc_ovg[1]]
    print('Success')
    return df_exp


def draw_table(pdf_canvas, dataframe, x, y):
    # Convert DataFrame to list of lists
    table_data = [dataframe.columns.tolist()] + dataframe.values.tolist()

    # Create the table
    table = Table(table_data)

    # Add table style
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)

    # Calculate the table's size
    table_width, table_height = table.wrap(0, 0)

    # Draw the table on the canvas
    table.drawOn(pdf_canvas, x, y - table_height)


def generate_report(df_exp, data_start, data_end, mission_name, plot_1, plot_2, plot_3, plot_4, plot_5, plot_6, plot_7, plot_8, plot_9):
    print('Generating report')
    pdf_filename = os.path.join(folder_path, 'Exports/', mission_name + '_' + data_start + '_to_' + data_end + '_report.pdf')
    pdf_canvas = canvas.Canvas(pdf_filename, pagesize=letter)
    pdf_canvas.setFont("Helvetica-Bold", 16)
    pdf_canvas.drawString(230, 750, f'{mission_name} Report')
    pdf_canvas.drawString(180, 720, f'{data_start} to {data_end}')
    # Add the table at the start
    draw_table(pdf_canvas, df_exp, 200, 700)

    # Adjust position for the first plot
    pdf_canvas.translate(0, -250)

    # First plot
    pdf_canvas.drawInlineImage(plot_1, 25, 400, width=600, height=300)

   
    pdf_canvas.showPage()
    pdf_canvas.drawInlineImage(plot_2, 25, 400, width=600, height=300)
    pdf_canvas.translate(0, -25)
    pdf_canvas.drawInlineImage(plot_3, 25, 100, width=600, height=300)
    pdf_canvas.showPage()
 
    pdf_canvas.drawInlineImage(plot_4, 25, 400, width=600, height=300)
    pdf_canvas.translate(0, -25)
    pdf_canvas.drawInlineImage(plot_5, 25, 100, width=600, height=300)
    pdf_canvas.showPage()
    pdf_canvas.drawInlineImage(plot_6, 25, 400, width=600, height=300)
    pdf_canvas.translate(0, -25)
    pdf_canvas.drawInlineImage(plot_7, 25, 100, width=600, height=300)
    pdf_canvas.showPage()
    pdf_canvas.drawInlineImage(plot_8, 25, 400, width=600, height=300)
    pdf_canvas.translate(0, -25)
    pdf_canvas.drawInlineImage(plot_9, 25, 100, width=600, height=300)
    
    # Save
    pdf_canvas.save()
    print('Success')
    return pdf_filename
