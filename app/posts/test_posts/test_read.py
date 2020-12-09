from database.read_sql import collect_sql_queries, fetch_sql_files, parse_sql_batch


def test_fetch_sql_files():
    files = fetch_sql_files()
    assert files is not None
    assert files[0].split(".")[1] == "sql"


def test_collect_sql_queries():
    queries = collect_sql_queries()
    assert type(queries) == dict


def test_select_query(rdbms):
    files = fetch_sql_files(subdirectory="/posts/selects")
    parsed_sql = parse_sql_batch(files)
    query_result = rdbms.execute_query(parsed_sql[0], "hackers_prod")
    assert len(files) == 1
    assert type(parsed_sql[0]) == str
    print(query_result.rowcount)
