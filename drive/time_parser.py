import re
import os
import json
import ast
import sys

def check_loops_for_time_calls(file_path):
    """
    Checks if self.play(..., run_time=...) or self.wait(...) are present within a for loop.
    If found, prints details and exits.
    """
    if not os.path.exists(file_path):
        return

    with open(file_path, 'r') as f:
        content = f.read()

    try:
        tree = ast.parse(content)
    except SyntaxError:
        print(f"Syntax error parsing {file_path}")
        return

    lines = content.splitlines()
    section_starts = []
    for i, line in enumerate(lines):
        match = re.search(r'## Section (\d+)', line)
        if match:
            section_starts.append((i + 1, int(match.group(1))))
    
    def get_section(line_no):
        sec = "Unknown"
        for start, s_num in section_starts:
            if line_no >= start:
                sec = s_num
            else:
                break
        return sec

    for node in ast.walk(tree):
        if isinstance(node, (ast.For, ast.AsyncFor)):
            for child in ast.walk(node):
                if isinstance(child, ast.Call):
                    func = child.func
                    if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name) and func.value.id == 'self':
                        is_violation = False
                        msg = ""
                        if func.attr == 'play':
                            for kw in child.keywords:
                                if kw.arg == 'run_time':
                                    is_violation = True
                                    msg = "self.play(..., run_time=...)"
                                    break
                        elif func.attr == 'wait':
                            if child.args or child.keywords:
                                is_violation = True
                                msg = "self.wait(...)"
                        
                        if is_violation:
                            sec = get_section(child.lineno)
                            print(f"Violation detected in {file_path}")
                            print(f"Section {sec}, Line {child.lineno}: {lines[child.lineno-1].strip()}")
                            print(f"Pattern: {msg} inside a loop.")
                            choice = input("To ignore. Press the key p. Press any other key to terminate and fix the code:")
                            if choice.lower() != 'p':
                                sys.exit(1)

def parse_manim_script_times(file_path):
    """
    Parses a Manim script to calculate the sum of run_time in self.play()
    and wait time in self.wait() for each section.

    Args:
        file_path (str): The absolute path to the Manim script file.

    Returns:
        dict: A dictionary with section numbers as keys and total times as values.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return {}

    with open(file_path, 'r') as f:
        script_content = f.read()

    # Regex to split the script into sections based on '## Section X' comments
    # The (?=...) is a positive lookahead to keep the delimiter
    sections = re.split(r'(?=## Section \d+)', script_content)
    
    section_times = {}

    # Regex to find run_time in self.play()
    play_time_regex = re.compile(r'self\.play\(.*?run_time\s*=\s*([\d.]+)', re.DOTALL)

    # Regex to find run_time in self.move_camera()
    camera_time_regex = re.compile(r'self\.move_camera\(.*?run_time\s*=\s*([\d.]+)', re.DOTALL)
    
    # Regex to find time in self.wait()
    wait_time_regex = re.compile(r'self\.wait\(\s*([\d.]+)\)')

    for section_text in sections:
        if not section_text.strip():
            continue

        # Find the section number
        section_header_match = re.search(r'## Section (\d+)', section_text)
        if not section_header_match:
            continue
        
        section_number = int(section_header_match.group(1))
        total_time = 0.0

        # Find all run_times in self.play calls
        for time_str in play_time_regex.findall(section_text):
            total_time += float(time_str)

        # Find all run_times in self.play calls
        for time_str in camera_time_regex.findall(section_text):
            total_time += float(time_str)

        # Find all wait times
        for time_str in wait_time_regex.findall(section_text):
            total_time += float(time_str)
        
        section_times[section_number] = round(total_time, 2)

    return section_times

cgi_input = "/Users/sathwikbadda/Assigment/Manim-Assignment/drive/CGI_Input.json"
with open(cgi_input,'r') as f:
    cgi_data = json.load(f)

for group,group_data in cgi_data.items():
    print(f"\n\n--------Group {group}:-----------\n")
    section_times = {i+1:section_item["run_time"] for i,section_item in enumerate(group_data)}
    target_file = '/Users/sathwikbadda/Assigment/Manim-Assignment/drive/group_'+str(group)+'.py'
    check_loops_for_time_calls(target_file)
    times = parse_manim_script_times(target_file)
    for section_no in times.keys():
        if os.path.exists(target_file):
            print(f"-------Section {section_no}---------\n")
            print(f"Video time:{times[section_no]}, Audio time:{section_times[section_no]}, delta:{times[section_no]-section_times[section_no]}")
