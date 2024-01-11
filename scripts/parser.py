import os
from hunter.prsemaster import convert_html_to_text, get_basic_info_from_html


def read_html_file(folder_path, filename):
    with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as f:
        return f.read()


def write_to_ouput_file(output_folder, output_filename, combined_text):
    with open(os.path.join(output_folder, output_filename), "w", encoding="utf-8") as outfile:
        outfile.write(combined_text)


def extract_text_from_html_folder(folder_path, output_folder):
    for filename in os.listdir(folder_path):
        if filename.endswith(".html"):
            html_content = read_html_file(folder_path, filename)
            basic_info = get_basic_info_from_html(html_content)
            if basic_info['name']:
                resume_text = convert_html_to_text(html_content)
                json_str = ""
                for key, value in basic_info.items():
                    json_str += f"{key}: {value},\n"

                output_filename = f"{filename[:-5]}_{basic_info['name']}.txt"
                write_to_ouput_file(output_folder, output_filename, resume_text[0])
