import pkgutil
import base64
import itertools
import gradio as gr

counter = itertools.count()

class MarkdownFile:
  def __init__(self, path):
    self.path = path

  def render(self):
    with open(self.path) as fin:
      content = fin.read()
      content = content.split('\n---\n')[-1]
      return gr.Markdown(value=content)

class Demo:
  def __init__(self, predict, input, settings=[], scale=1):
    self.predict = predict
    self.input = input
    self.settings = settings
    self.scale = scale
    self.i = next(counter)

  def render(self):
    output = self.predict(self.input, *[s.value for s in self.settings])
    inputs, outputs = [], []
    with gr.Row().style(equal_height=False):
      with gr.Column(scale=self.scale):
        with gr.Tab('Pipeline Input'):
          inputs.append(gr.Dataframe(
            headers=list(self.input.columns),
            datatype=[{'i': 'number', 'f': 'number', 'O': 'str'}[t.kind] for t in self.input.dtypes],
            col_count=(len(self.input.columns), 'fixed'),
            wrap=True,
            value=self.input,
          ))
        if self.settings:
          with gr.Tab('Settings'):
            for setting in self.settings:
              inputs.append(setting)
              setting.render()
        submit_btn = gr.Button("Transform", variant="primary")
      with gr.Column(scale=1):
        with gr.Tab('Pipeline Output'):
          outputs.append(gr.Dataframe(
            headers=list(output[0].columns),
            datatype=[{'i': 'number', 'f': 'number', 'O': 'str'}[t.kind] for t in output[0].dtypes],
            wrap=True,
            value=output[0],
          ))
        if len(output) > 1:
          with gr.Tab('Code'):
            outputs.append(gr.Markdown(value=output[1]))
        if len(output) > 2:
          with gr.Tab('Visualisation'):
            outputs.append(gr.HTML(value=output[2]))
    submit_btn.click(self.predict, inputs, outputs, api_name=f"predict_{self.i}", scroll_to_output=True)

def interface(*items):
  style = pkgutil.get_data('pyterrier_gradio', 'style.css').decode()
  with gr.Blocks(css=style) as app:
    for item in items:
      item.render()
  return app


def df2code(df):
  rows = []
  for row in df.itertuples(index=False):
    rows.append(f'  {dict(row._asdict())},')
  rows = '\n'.join(rows)
  return f'''pd.DataFrame([
{rows}
])'''


def code2colab(code, COLAB_INSTALL, COLAB_NAME):
  enc_code = base64.b64encode((COLAB_INSTALL + '\n\n' + code.strip()).encode()).decode()
  url = f'https://colaburl.macavaney.us/?py64={enc_code}&name={COLAB_NAME}'
  return f'<div style="text-align: center; margin-bottom: -16px;"><a href="{url}" rel="nofollow" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab" style="margin: 0; display: inline-block;" /></a></div>'


def code2md(code, COLAB_INSTALL, COLAB_NAME):
  return f'''
{code2colab(code, COLAB_INSTALL, COLAB_NAME)}

```python
{code.strip()}
```
'''
