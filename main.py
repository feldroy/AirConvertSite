import air
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
        code = air.BaseTag.from_html_to_source(code)
        html_code = highlight(code, lexer, formatter)
        return air.Div(
            air.Article(air.tags.Raw(html_code)),
            air.Button(
                air.svg.Svg(
                    air.svg.Rect(x="9", y="9", width="13", height="13", rx="2", ry="2"),
                    air.svg.Path(d="m5 15-4-4 4-4"),
                    air.svg.Path(d="M5 9V5a2 2 0 0 1 2-2h4"),
                    width="20",
                    height="20",
                    viewbox="0 0 24 24",
                    fill="none",
                    stroke="darkgrey",
                    stroke_width="2",
                ),
                onclick="copyArticleContent()",
                id="copy-btn",
                title="Copy to clipboard",
            ),            
            air.Style("""
            #copy-btn {
                position: absolute;
                top: 10px;
                right: 10px;
                background: rgba(255, 255, 255, 0.9);
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px;
                cursor: pointer;
                transition: all 0.2s;
                z-index: 10;
            }
            #copy-btn:hover {
                background: rgba(255, 255, 255, 1);
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            #copy-btn svg {
                display: block;
            }
        """),
            air.Script("""
            function copyArticleContent() {
                const article = document.getElementById('result') || document.getElementById('article');
                if (article) {
                    const text = article.innerText || article.textContent;
                    navigator.clipboard.writeText(text).then(() => {
                        const btn = document.getElementById('copy-btn');
                        btn.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="green" stroke-width="2"><polyline points="20,6 9,17 4,12"></polyline></svg>';
                        setTimeout(() => {
                            btn.innerHTML = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                                <path d="m5 15-4-4 4-4"></path>
                                <path d="M5 9V5a2 2 0 0 1 2-2h4"></path>
                            </svg>`;
                        }, 2000);
                    });
                }
            }
        """),
            id="result",
            hx_swap_oob="true",
            style="position: relative;",
        )
    return air.Children(
        air.Article("Nothing", hx_swap_oob="", id="result"),
    )


@app.page
async def index():
    title = "Convert HTML to Air Tags"
    return air.layouts.mvpcss(
        air.Title(title),
        air.Style(formatter.get_style_defs(".highlight")),
        air.H1(title),
        air.P(
            air.A(
                "A tool for the Air web framework",
                href="https://airdocs.fastapicloud.dev/",
            )
        ),
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
        air.Div(
            air.Article(air.Pre(air.Code("Code will go here")), id="result"),
        ),
    )
