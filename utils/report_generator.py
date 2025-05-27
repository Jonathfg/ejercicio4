import io
from typing import List, Dict
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa

# Excel y CSV

def create_dataframe(records: List[Dict]) -> pd.DataFrame:
    df = pd.DataFrame(records)
    # convierte columna time a datetime
    df["time"] = pd.to_datetime(df["time"])
    return df

def generate_csv(df: pd.DataFrame) -> io.BytesIO:
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    return buffer

def generate_excel(df: pd.DataFrame) -> io.BytesIO:
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Weather")
    buffer.seek(0)
    return buffer

# PDF

def generate_pdf(df: pd.DataFrame) -> io.BytesIO:
    # Carga plantilla Jinja2
    env = Environment(loader=FileSystemLoader("views"))
    template = env.get_template("pdf_template.html")
    html = template.render(records=df.to_dict(orient="records"))
    buffer = io.BytesIO()
    pisa.CreatePDF(io.StringIO(html), dest=buffer)
    buffer.seek(0)
    return buffer