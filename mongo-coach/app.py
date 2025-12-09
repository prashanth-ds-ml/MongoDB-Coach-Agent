import gradio as gr

def home():
    return (
        "👋 Welcome to MongoCoach!\n\n"
        "The backend agents (scraper, tutor, planner, analytics) "
        "are under active development. This Space currently exposes "
        "only a simple placeholder interface."
    )

with gr.Blocks() as demo:
    gr.Markdown("# MongoCoach – MongoDB Associate Developer (Python)")
    gr.Markdown(
        "This Space will become an AI-powered exam coach using MongoDB, RAG, and agents."
    )
    btn = gr.Button("Say hi")
    out = gr.Textbox(label="Status")

    btn.click(fn=lambda: home(), outputs=out)

if __name__ == "__main__":
    demo.launch()
