from flask import Flask, render_template, request, redirect
from wiki_linkify import wiki_linkify
import pg

db = pg.DB(dbname='wiki')
app = Flask('wikiApp')

@app.route('/<page_name>')
def display_page(page_name):
    query = db.query("select * from page where page_title = '%s'" % page_name)
    result = query.namedresult()
    if len(result) < 1:
        return render_template(
            'placeholder.html',
            page_name=page_name
        )
    else:
        query2 = db.query("select * from page where page_title = '%s'" % page_name)
        result2 = query2.namedresult()
        page_name = result2[0].page_title
        page_content = result2[0].content
        author = result2[0].author
        # wiki_content = wiki_linkify(page_content)
        return render_template(
            'pagename.html',
            page_name=page_name,
            content=page_content,
            author=author,
            result2 = query2.namedresult()
        )
            # redirect('%s.html' % page_name)

@app.route('/<page_name>/edit')
def edit_page(page_name):
    return render_template(
    'edit.html',
    page_name=page_name
    )

@app.route('/<page_name>/save', methods=['POST'])
def add_entry(page_name):
    page_title = request.form.get('name')
    content = request.form.get('page_content')
    author = request.form.get('Author')
    db.insert(
    'page',
    page_title=page_title,
    author=author,
    content=content
    )
    return redirect('/%s' % page_name)


if __name__ == '__main__':
    app.run(debug=True)
