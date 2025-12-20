import sqlite3

from bottle import post, request, route, run, static_file


class db:
    def create():
        conn = sqlite3.connect("autoblog.db")
        cursor = conn.cursor()
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS blog (
            title,
            url,
            post_original,
            title_ai,
            post_ai
        );
        """
        )
        conn.commit()
        conn.close()

    def new(title, url):
        conn = sqlite3.connect("autoblog.db")
        cursor = conn.cursor()
        sql = "insert into blog(title, url) values(?,?)"
        cursor.execute(sql, (title, url))
        conn.commit()
        conn.close()

    def find(query):
        conn = sqlite3.connect("autoblog.db")
        cursor = conn.cursor()
        sql = "select * from blog where post_ai like ? order by rowid desc"
        result = cursor.execute(sql, (f"%{query}%",))
        result = result.fetchall()
        conn.close()
        return result

    def index():
        conn = sqlite3.connect("autoblog.db")
        cursor = conn.cursor()
        sql = "select * from blog where post_ai IS NULL"
        result = cursor.execute(sql)
        result = result.fetchall()
        conn.close()

        return result

    def update_original(url, text, text_ai, title_ai):
        conn = sqlite3.connect("autoblog.db")
        cursor = conn.cursor()
        sql = """
            update blog set post_original = ?,
            post_ai = ?,
            title_ai = ?
            where url = ?
            """
        cursor.execute(sql, (text, text_ai, title_ai, url))
        conn.commit()
        conn.close()


@route("/", method=["GET", "POST"])
def index():
    query = request.forms.get("query")
    if not query:
        query = ""

    response = db.find(query)
    posts = ""
    for item in response:
        lines = item[4].split("\n")
        text = ""
        for line in lines:
            text += f"<p>{line}</p>"
        posts += f"""
                    <h1>{item[3]}</h1>
                    <p>{text}</p>
                    """
    page = f"""
            <h1>Web App</h1>
            <form action="/" method="post">
                Search: <input type="text" name="query">
                <br>
                <input type="submit">
            </form>
            <strong>{query}</strong><br>
            {posts}
            """
    return page


@route("/pic/<filename:path>")
def serve_static(filename):
    return static_file(filename, root="./pic")


run(host="localhost", port=8080)
