""" Wifi Statistics """
from tkinter import Tk
from tkinter import messagebox
import tkinter.filedialog as fd
from multiprocessing import Pool
from shutil import copy2 as shcopy2
from functools import partial
from os import path, cpu_count, getcwd
#from sys import executable
from csv import reader as csv_reader
from openpyxl import load_workbook

def prep_excel_file(base_excelfile, log_file):
    """ copy the main excel file to the new file for calculations """
    file_basename = path.basename(log_file).split('.')[0]
    new_filepath = path.dirname(excel_file)+"/"+file_basename+"-calc.xlsx"
    shcopy2(base_excelfile, new_filepath)
    del base_excelfile
    return new_filepath

def ingest_logs(log_file):
    """ get all the log data from csv """
    log_data = []
    with open(log_file, "r", encoding="utf-8") as stats_file:
        log_reader = csv_reader(stats_file, delimiter="\t")
        for row in log_reader:
            log_data.append(row[3])
        stats_file.close()
    return log_data

def modify_workbook(calc_file, public_logs, staff_logs):
    """ add data to each worksheet in the workbook """
    work_book = load_workbook(calc_file)
    public_sheet = work_book["PublicCount"]
    staff_sheet = work_book["StaffCount"]
    def iterate_logs(sheet_name, log_list):
        """ iterate over a list and and modify worksheet"""
        index = 2
        for logs in log_list:
            cell_location = "A"+str(index)
            sheet_name[cell_location] = logs
            index += 1
    iterate_logs(public_sheet, public_logs)
    iterate_logs(staff_sheet, staff_logs)
    work_book.save(calc_file)
    del public_logs, staff_logs, work_book, staff_sheet, public_sheet


def get_stats(logs_list):
    """ parse the log data into different lists """
    public_stats = []
    staff_stats = []
    for logs in logs_list:
        if "remove cookie: user logged in" in logs:
            public_stats.append(logs)
        elif "add cookie: user logged in" in logs:
            public_stats.append(logs)
        elif "connected, signal strength" in logs:
            public_stats.append(logs)
        elif "dhcp-staff-wifi sending ack with id" in logs:
            staff_stats.append(logs)
        else:
            pass
    return public_stats, staff_stats

def main(base_excelfile, file_name):
    """ main logic for each thread created """
    calc_file = prep_excel_file(base_excelfile, file_name)
    parsed_logs = ingest_logs(file_name)
    stats_list = get_stats(parsed_logs)
    modify_workbook(calc_file, stats_list[0], stats_list[1])
    del calc_file, parsed_logs, stats_list

if __name__ == "__main__":
    current_dir = getcwd()
    excel_file = current_dir+"/wifi_calc.xlsx"
    log_files = fd.askopenfilenames(parent=Tk(), title='Choose file(s)')
    with Pool(int(round(cpu_count()/2))) as p:
        p.map(partial(main, excel_file), list(log_files))
    messagebox.showinfo("Wifi Stats", "Completed!")
