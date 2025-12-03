# pdf_exporter.py
# (Предполагается, что установлена библиотека fpdf2: pip install fpdf2)
from fpdf import FPDF

def export_to_pdf(data_lines, output_filename="output.pdf"):
    """
    Создает PDF-файл из списка строк.
    """
    if not data_lines:
        print("⚠️ Нет данных для экспорта в PDF.")
        return

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Настройка шрифта
    pdf.set_font("Arial", size=12)
    
    for line in data_lines:
        pdf.cell(0, 10, txt=line, ln=1) # ln=1 переводит курсор на следующую строку

    pdf.output(output_filename)
    print(f"✅ Данные успешно экспортированы в PDF: {output_filename}")