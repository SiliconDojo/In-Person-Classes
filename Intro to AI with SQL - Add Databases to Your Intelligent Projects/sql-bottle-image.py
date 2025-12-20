import sqlite3

from bottle import post, request, route, run, static_file


class db:
    def create():
        conn = sqlite3.connect("ai-class.db")
        cursor = conn.cursor()
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS picture (
            path,
            description
        );
        """
        )
        conn.commit()
        conn.close()

    def find(query):
        conn = sqlite3.connect("ai-class.db")
        cursor = conn.cursor()
        sql = "select * from picture where description like ?"
        result = cursor.execute((sql), (f"%{query}%",))
        result = result.fetchall()
        conn.close()

        return result


def gallery():
    with open("gallery.csv", "r") as file:
        pictures = file.readlines()
    gallery = ""
    for image in pictures:
        item = image.split("|")
        gallery += f"""
                    <div style="display:inline-block; width:200px; height:auto;">
                        <img style="width:100%; height:auto;" src="{item[0]}">
                        <p>{item[1]}<p>
                    </div>
                    """

    return gallery


@route("/", method=["GET", "POST"])
def index():
    query = request.forms.get("query")
    # response = ''
    # # if query:
    response = db.find(query)

    gallery = '<div style="display: flex; flex-wrap: wrap;justify-content: flex-start;">'
    for item in response:
        gallery += f"""
                    <div style="border: 1px black solid; width:200px;">
                        <img style="width:200px; height:200px;" src="/pic/{item[0]}">
                        <p>{item[1]}</p>
                    </div>
                    """
    gallery += "</div>"
    page = f"""
            <h1>Web App</h1>
            <form action="/" method="post">
                Search: <input type="text" name="query">
                <br>
                <input type="submit">
            </form>
            <strong>{query}</strong><br>
            {gallery}
            """
    return page


@route("/pic/<filename:path>")
def serve_static(filename):
    return static_file(filename, root="./pic")


run(host="localhost", port=8080)
