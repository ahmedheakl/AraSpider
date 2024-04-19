import re

EASY = "easy"
MEDIUM = "medium"
HARD = "hard"
EXTRA_HARD = "extra"

def num_of_agg(sql_query: str) -> int:
    sql_query = sql_query.upper()
    aggregation_functions = ["SUM", "AVG", "MIN", "MAX", "COUNT"]
    aggregation_pattern = re.compile(
        r"\b(" + "|".join(aggregation_functions) + r")\s*\(", re.IGNORECASE
    )
    aggregation_matches = aggregation_pattern.findall(sql_query)

    return len(aggregation_matches)


def num_select_cols(sql_query: str) -> int:
    sql_query = sql_query.upper()
    select_pattern = re.compile(r"\bSELECT\b(.*?)\bFROM\b", re.IGNORECASE | re.DOTALL)

    select_match = select_pattern.search(sql_query)
    if " * " in select_match.group(0).strip():
        return 100
    if select_match:
        return select_match.group(0).strip().count(",") + 1
    return 0


def num_where_conditions(sql_query: str) -> int:
    sql_query = sql_query.upper()
    where_count = 0

    if " WHERE " in sql_query:
        inner_conditions = sql_query.split(" WHERE ")[1].split(
            " AND "
        ) + sql_query.split(" WHERE ")[1].split(" OR ")
        where_count += (
            len(inner_conditions) - 1
        )

    return where_count


def num_group_by_clauses(sql_query: str) -> int:
    sql_query = sql_query.upper()
    max_columns_per_clause = 0
    ignore_keywords = ["ORDER BY", "LIMIT", "HAVING"]

    clauses = sql_query.split(" GROUP BY ")
    for clause in clauses[1:]:
        for kw in ignore_keywords:
            clause = clause.split(kw)[0]

        columns = clause.strip().split(",")
        max_columns_per_clause = max(max_columns_per_clause, len(columns))

    return max_columns_per_clause


def count_query_comp1(sql_query: str) -> int:
    keywords = [
        "WHERE",
        "GROUP BY",
        "ORDER BY",
        "LIMIT",
        "JOIN",
        " OR ",
        "LIKE",
        "HAVING",
    ]
    return sum(sql_query.count(keyword) for keyword in keywords)


def count_query_comp2(sql_query: str) -> int:
    keywords = ["EXCEPT", "UNION", "INTERSECT", "NESTED"]
    return sum(sql_query.count(keyword) for keyword in keywords)


def count_others(sql_query: str) -> int:
    num_agg = num_of_agg(sql_query)
    num_select = num_select_cols(sql_query)
    num_where = num_where_conditions(sql_query)
    num_group_by = num_group_by_clauses(sql_query)

    return (num_agg > 1) + (num_select > 1) + (num_where > 1) + (num_group_by > 1)


def classify_sql_query(sql_query: str) -> str:
    sql_query = sql_query.upper()

    comp1 = count_query_comp1(sql_query)
    comp2 = count_query_comp2(sql_query)
    others = count_others(sql_query)

    easy_conditions = comp1 <= 1 and others == 0 and comp2 == 0
    medium_conditions = (
        (others <= 2 and comp1 <= 1 and comp2 == 0) 
        or (others < 2 and comp1 == 2 and comp2 == 0)
    )
    hard_conditions = (
        (others > 2 and comp1 <= 2 and comp2 == 0)
        or (comp1 > 2 and comp1 <= 3 and others <= 2 and comp2 == 1)
        or (comp1 <= 1 and others == 0 and comp2 == 1)
    )

    if easy_conditions:
        return EASY
    if medium_conditions:
        return MEDIUM
    if hard_conditions:
        return HARD
    return EXTRA_HARD