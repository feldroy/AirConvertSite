import air
import air_convert
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

app = air.Air()

lexer = PythonLexer()
formatter = HtmlFormatter()


@app.post("/submit")
async def submit(request: air.Request):
    form = await request.form()
    if code := form.get("code"):
        code = air_convert.html_to_airtags(code)
        html_code = highlight(code, lexer, formatter)
        return air.Article(air.tags.Raw(html_code), id="result", hx_swap_oob='true')
    return air.Children(air.Article("Nothing", id="result", hx_swap_oob=''))


@app.page
async def index():
    title = "Convert HTML to Air Tags"
    return air.layouts.mvpcss(
        air.Title(title),
        air.H1(title),
        air.Style(formatter.get_style_defs('.highlight')),
        air.Form(
            air.Textarea(
                id="code",
                name="code",
                rows="8",
                cols="80",
                placeholder="Paste HTML here...",
                autofocus=True,
            ),
            hx_post="/submit",
            hx_trigger="keyup",
            hx_swap="none",
        ),
        air.Article(air.Pre(air.Code('Code will go here')), id="result"),
    )

