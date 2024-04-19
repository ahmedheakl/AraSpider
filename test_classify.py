import json


from classify_query import (
    count_query_comp1,
    count_query_comp2,
    num_select_cols,
    num_of_agg,
    num_where_conditions,
    num_group_by_clauses,
    count_others,
    classify_sql_query,
)

from classify_query import EASY, MEDIUM, HARD, EXTRA_HARD

TESTS_PATH = "tests.json"


def test_counting():
    

    with open(TESTS_PATH, "r") as f:
        count_tests = json.load(f)

    for test in count_tests:
        if test.get("sql", None) is None:
            continue

        sql = test["sql"]
        comp1 = count_query_comp1(sql)
        comp2 = count_query_comp2(sql)
        select = num_select_cols(sql)
        agg = num_of_agg(sql)
        where = num_where_conditions(sql)
        group_by = num_group_by_clauses(sql)
        others = count_others(sql)
        classification = classify_sql_query(sql)

        comp1_msg = f"Expec. comp1 {test['comp1']} but got {comp1} in {sql}"
        comp2_msg = f"Expec. comp2 {test['comp2']} but got {comp2} in {sql}"
        select_cols_msg = f"Expec. cols {test['select_cols']} but got {select} in {sql}"
        agg_msg = f"Expec. agg {test['agg']} but got {agg} in {sql}"
        where_msg = f"Expec. where {test['where_cond']} but got {where} in {sql}"
        group_by_msg = f"Expec. group {test['group_by']} but got {group_by} in {sql}"
        others_msg = f"Expec. others {test['others']} but got {others} in {sql}"
        class_msg = f"Expec. class {test['class']} but got {classification} in {sql}"

        assert comp1 == test["comp1"], comp1_msg
        assert comp2 == test["comp2"], comp2_msg
        assert select == test["select_cols"], select_cols_msg
        assert agg == test["agg"], agg_msg
        assert where == test["where_cond"], where_msg
        assert group_by == test["group_by"], group_by_msg
        assert others == test["others"], others_msg
        assert classification == test["class"], class_msg
