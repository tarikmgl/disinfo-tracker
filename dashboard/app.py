import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import requests

app = dash.Dash(__name__, title="Disinfo Tracker")

app.layout = html.Div([
    html.H1("Disinfo Tracker", style={"textAlign": "center", "marginBottom": "30px"}),

    html.Div([
        dcc.Input(
            id="query-input",
            type="text",
            placeholder="Konu gir (örn. Ukraine, AI, climate)...",
            style={"width": "70%", "padding": "10px", "fontSize": "16px"}
        ),
        html.Button(
            "Analiz Et",
            id="analyze-btn",
            n_clicks=0,
            style={"padding": "10px 20px", "marginLeft": "10px", "fontSize": "16px"}
        ),
    ], style={"textAlign": "center", "marginBottom": "30px"}),

    html.Div(id="summary-cards", style={"textAlign": "center", "marginBottom": "30px"}),

    html.Div([
        dcc.Graph(id="sentiment-chart", style={"width": "50%", "display": "inline-block"}),
        dcc.Graph(id="source-chart", style={"width": "50%", "display": "inline-block"}),
    ]),

    html.H3("Benzerlik Tablosu", style={"textAlign": "center", "marginTop": "30px"}),
    html.Div(id="similarity-table", style={"padding": "0 40px"}),

], style={"fontFamily": "Arial", "maxWidth": "1200px", "margin": "0 auto"})


@app.callback(
    Output("summary-cards", "children"),
    Output("sentiment-chart", "figure"),
    Output("source-chart", "figure"),
    Output("similarity-table", "children"),
    Input("analyze-btn", "n_clicks"),
    Input("query-input", "value"),
    prevent_initial_call=True
)
def update_dashboard(n_clicks, query):
    if not query:
        return "", {}, {}, ""

    requests.get(f"http://127.0.0.1:8000/analyze?query={query}")

    sentiment_data = requests.get("http://127.0.0.1:8000/sentiment").json()
    summary_data = requests.get("http://127.0.0.1:8000/summary").json()
    similarity_data = requests.get("http://127.0.0.1:8000/similarity").json()

    df = pd.DataFrame(sentiment_data)

    # Summary cards
    cards = html.Div([
        html.Span(f"Toplam: {summary_data['total']}", style={"margin": "10px", "padding": "10px 20px", "background": "#eee", "borderRadius": "8px"}),
        html.Span(f"Pozitif: {summary_data['positive']}", style={"margin": "10px", "padding": "10px 20px", "background": "#d4edda", "borderRadius": "8px"}),
        html.Span(f"Negatif: {summary_data['negative']}", style={"margin": "10px", "padding": "10px 20px", "background": "#f8d7da", "borderRadius": "8px"}),
    ])

    # Sentiment dağılımı
    sentiment_fig = px.pie(
        df, names="sentiment",
        title="Sentiment Dağılımı",
        color="sentiment",
        color_discrete_map={"POSITIVE": "#28a745", "NEGATIVE": "#dc3545"}
    )

    # Kaynak bazlı sentiment
    source_counts = df.groupby(["source", "sentiment"]).size().reset_index(name="count")
    source_fig = px.bar(
        source_counts, x="source", y="count",
        color="sentiment",
        title="Kaynak Bazlı Sentiment",
        color_discrete_map={"POSITIVE": "#28a745", "NEGATIVE": "#dc3545"},
        barmode="group"
    )
    source_fig.update_layout(xaxis_tickangle=-45)

    # Benzerlik tablosu
    if similarity_data:
        sim_df = pd.DataFrame(similarity_data)
        table = html.Table([
            html.Thead(html.Tr([html.Th("Kaynak A"), html.Th("Kaynak B"), html.Th("Benzerlik")])),
            html.Tbody([
                html.Tr([
                    html.Td(row["source_a"]),
                    html.Td(row["source_b"]),
                    html.Td(f"{row['similarity']:.2f}")
                ]) for _, row in sim_df.iterrows()
            ])
        ], style={"width": "100%", "borderCollapse": "collapse", "textAlign": "left"})
    else:
        table = html.P("Yeterli benzerlik bulunamadı.")

    return cards, sentiment_fig, source_fig, table


if __name__ == "__main__":
    app.run(debug=True, port=8050)