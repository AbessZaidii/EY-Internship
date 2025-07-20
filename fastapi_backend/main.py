from fastapi import FastAPI, Response, Query
from fastapi.responses import StreamingResponse, HTMLResponse
import pandas as pd
from io import StringIO

app = FastAPI()
print("✅ main.py loaded")

# Dummy data tables
tables = {
    "public": pd.DataFrame({
        "ID": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "Name": ["Alice", "Bob", "Charlie", "Diana", "Ethan", "Fiona", "George", "Hannah", "Ian", "Julia"],
        "Age": [25, 30, 22, 28, 35, 27, 31, 29, 24, 26]
    }),
    "private": pd.DataFrame({
        "ProductID": [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
        "ProductName": ["Keyboard", "Mouse", "Monitor", "Laptop", "Printer", "Webcam", "Headphones", "Microphone", "Speakers", "USB Hub"],
        "Price": [999.99, 499.49, 7999.00, 1500.00, 300.00, 150.00, 120.00, 80.00, 200.00, 50.00]
    }),
    "archived": pd.DataFrame({
        "OrderID": [501, 502, 503, 504, 505, 506, 507, 508, 509, 510],
        "Customer": ["X Corp", "Y Ltd", "Z Inc", "A LLC", "B Co", "C GmbH", "D Enterprises", "E Solutions", "F Partners", "G Group"],
        "Status": ["Shipped", "Delivered", "Returned", "Processing", "Cancelled", "Delivered", "Shipped", "Delivered", "Processing", "Cancelled"]
    })
}

@app.get("/{table_name}")
def get_table(table_name: str, download: bool = Query(False, description="Download as CSV if true")):
    table = tables.get(table_name.lower())
    
    if table is None:
        return {"error": "Table not found. Try /public, /private or /archived"}

    if download:
        stream = StringIO()
        table.to_csv(stream, index=False)
        stream.seek(0)
        return StreamingResponse(
            stream,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={table_name}.csv"}
        )
    
    html_table = table.to_html(index=False)
    html_content = f"""
    <html>
        <head>
            <title>{table_name.capitalize()} Table</title>
        </head>
        <body>
            <h1>{table_name.capitalize()} Table</h1>
            {html_table}
            <p><a href="/{table_name}?download=true">Download CSV</a></p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)