import air
import air_convert

app = air.Air()


@app.page
async def index():
    title = "Convert HTML to Air Tags"
    return air.layouts.mvpcss(
        air.Title(title),
        air.H1(title),
        air.Form(
            air.Textarea(
                id="code",
                name="code",
                rows="6",
                cols="60",
                placeholder="Paste HTML here...",
                autofocus=True,
            ),
            hx_post="/submit",
            hx_trigger="keyup",
            hx_swap="none",
        ),
        air.Article("Code will go here", id="result"),
    )


@app.post("/submit")
async def submit(request: air.Request):
    form = await request.form()
    if code := form.get("code"):
        code = air_convert.html_to_airtags(code)
        return air.Article(air.Pre(air.Code(code)), id="result", hx_swap_oob='true')
    return air.Children(air.Article("Nothing", id="result", hx_swap_oob=''))
