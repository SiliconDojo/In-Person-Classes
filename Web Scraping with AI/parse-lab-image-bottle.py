import sqlite3

from bottle import post, request, route, run, static_file


class db:
    def create():
        conn = sqlite3.connect("image.db")
        cursor = conn.cursor()
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS image(
            pic,
            filename,
            description
        );
        """
        )
        conn.commit()
        conn.close()

    def find(query):
        conn = sqlite3.connect("image.db")
        cursor = conn.cursor()
        sql = "select * from image where description like ? order by rowid desc"
        result = cursor.execute(sql, (f"%{query}%",))
        result = result.fetchall()
        conn.close()
        return result


@route("/", method=["GET", "POST"])
def index():
    query = request.forms.get("query")
    if not query:
        query = ""

    response = db.find(query)
    posts = ""
    for item in response:
        posts += f"""
                    <img style="height:200px;width:auto;" src="/pics/{item[1]}">
                    <p>{item[0]}<p>
                    <p>{item[2]}</p>
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


@route("/pics/<filename:path>")
def serve_static(filename):
    return static_file(filename, root="./pics")


run(host="localhost", port=8080)
