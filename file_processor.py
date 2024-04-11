import os
import csv

def read_files_from_folder(input_folder):
    file_data = []
    for filename in os.listdir(input_folder):
        if filename.endswith(".dat"):
            with open(os.path.join(input_folder, filename), 'r') as file:
                data = file.readlines()
                file_data.extend(data)
    return file_data

def process_data(file_data):
    if not file_data:
        return None, None
    
    # Skip the header line if it exists
    if "id\tfirst_name\tlast_name\temail\tjob_title\tbasic_salary\tallowances" in file_data[0].lower():
        file_data = file_data[1:]
    
    salaries = []
    for line in file_data:
        columns = line.strip().split('\t')
        try:
            basic_salary = float(columns[-2]) 
            allowances = float(columns[-1])  
            total_salary = basic_salary + allowances
            salaries.append(total_salary)
        except (IndexError, ValueError):
            pass  # Ignore lines with missing or invalid salary data
    
    if len(salaries) < 2:
        return None, None
    salaries.sort(reverse=True)
    second_highest_salary = salaries[1]
    average_salary = sum(salaries) / len(salaries)
    return second_highest_salary, average_salary

def write_output_csv(output_folder, file_data, second_highest_salary, average_salary):
    if not file_data:
        return
    output_file = os.path.join(output_folder, "output.csv")
    
    unique_salaries = set()  # Set to store unique salaries
    
    with open(output_file, 'w') as file:
        writer = csv.writer(file)
        for salary in file_data:
            salary = salary.strip()
            if salary not in unique_salaries:
                writer.writerow([salary])
                unique_salaries.add(salary)
        
        writer.writerow(["Second Highest Salary", second_highest_salary])
        writer.writerow(["Average Salary", average_salary])
        

def main(input_folder, output_folder):
    file_data = read_files_from_folder(input_folder)
    second_highest_salary, average_salary = process_data(file_data)
    write_output_csv(output_folder, file_data, second_highest_salary, average_salary)

# Example usage:
input_folder = "input_files"
output_folder = "output_files"

try:
    main(input_folder, output_folder)
    print("Output CSV file generated successfully.")
except Exception as e:
    print("An error occurred:", e)