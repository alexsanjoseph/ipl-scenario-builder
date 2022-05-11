def create_footer(text: str):
    return """<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
# position: fixed;
# right: 0;
# bottom: 0px;
# width: 100%;
# background-color: white;
# color: black;
text-align: center;
padding-right: 3rem;
padding-top: 3rem;
}
</style>
<div class="footer">
<p>"""+text+"""</p>
</div>
    """


def hide_row_headers():
    return """
<style>
tbody th {display:none}
.blank {display:none}
</style>
            """


def hide_full_screen():
    return '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''


def reduce_whitespace():
    return """
<style>
.block-container {
    margin-top: -8rem;
}
</style>
        """


def highlighter(x):
    return ['background-color: darkgoldenrod' if x['predicted'] is True else '' for s in x]
