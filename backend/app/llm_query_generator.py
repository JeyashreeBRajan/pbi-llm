# app/llm_query_generator.py

def generate_dax_from_schema(question: str, schema: dict) -> dict:
    try:
        tables = [t["name"] for t in schema.get("tables", [])]
        relationships = schema.get("relationships", [])

        # Defaults
        sales_table = "Sales"
        geography_table = "Geography"
        city_column = "City"
        value_column = "SalesAmount"

        # Infer if Top N is requested
        is_topn = any(kw in question.lower() for kw in ["top", "highest", "most"])
        top_n = 5  # default

        # Try to detect grouping column
        if "region" in question.lower():
            group_col = "'Geography'[Region]"
        elif "city" in question.lower():
            group_col = "'Geography'[City]"
        else:
            group_col = "'Geography'[City]"

        # DAX measure
        dax_measure = f'SUM(\'{sales_table}\'[{value_column}])'

        # Base summarize
        summarize = f"""
SUMMARIZECOLUMNS(
    {group_col},
    "Total Sales", {dax_measure}
)
""".strip()

        # Wrap with TOPN if needed
        if is_topn:
            dax_query = f"""
EVALUATE
TOPN(
    {top_n},
    {summarize},
    [Total Sales],
    DESC
)
""".strip()
            answer = f"Showing top {top_n} groups based on total sales for your question: '{question}'"
        else:
            dax_query = f"""
EVALUATE
{summarize}
""".strip()
            answer = f"Showing total sales grouped by location for your question: '{question}'"

        return {
            "success": True,
            "answer": answer,
            "dax_query": dax_query
        }

    except Exception as e:
        return {
            "success": False,
            "answer": "Could not generate DAX query",
            "error": str(e)
        }
