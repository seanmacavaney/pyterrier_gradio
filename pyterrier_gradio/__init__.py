import pkgutil
import base64
import itertools
import gradio as gr
import pandas as pd

counter = itertools.count()

EX_Q = {
  'trec-dl-2019': pd.DataFrame([
    {"qid": "1108939", "query": "what slows down the flow of blood"},
    {"qid": "1112389", "query": "what is the county for grand rapids, mn"},
    {"qid": "792752", "query": "what is ruclip"},
  ]),
  'antique/train': pd.DataFrame([
    {"qid": "3097310", "query": "What causes severe swelling and pain in the knees?"},
    {"qid": "3910705", "query": "why don't they put parachutes underneath airplane seats?"},
    {"qid": "237390", "query": "how to clean alloy cylinder heads ?"},
  ]),
  "trec-robust-2004": pd.DataFrame([
    {"qid": "301", "query": "International Organized Crime"},
    {"qid": "302", "query": "Poliomyelitis and Post-Polio"},
    {"qid": "303", "query": "Hubble Telescope Achievements"},
  ]),
}

EX_D = {
  'msmarco-passage': pd.DataFrame([
    {"docno": "0", "text": "The presence of communication amid scientific minds was equally important to the success of the Manhattan Project as scientific intellect was. The only cloud hanging over the impressive achievement of the atomic researchers and engineers is what their success truly meant; hundreds of thousands of innocent lives obliterated."},
    {"docno": "100", "text": "Anton\u00edn Dvor\u00e1k (1841\u20131904) Antonin Dvorak was a son of butcher, but he did not follow his father's trade. While assisting his father part-time, he studied music, and graduated from the Prague Organ School in 1859."},
    {"docno": "1000", "text": "QuickFacts Matanuska-Susitna Borough, Alaska; UNITED STATES QuickFacts provides statistics for all states and counties, and for cities and towns with a population of 5,000 or more."},
  ]),
  'antique': pd.DataFrame([
    {"docno": "2020338_0", "text": "A small group of politicians believed strongly that the fact that Saddam Hussien remained in power after the first Gulf War was a signal of weakness to the rest of the world, one that invited attacks and terrorism. Shortly after taking power with George Bush in 2000 and after the attack on 9/11, they were able to use the terrorist attacks to justify war with Iraq on this basis and exaggerated threats of the development of weapons of mass destruction. The military strength of the U.S. and the brutality of Saddam's regime led them to imagine that the military and political victory would be relatively easy."},
    {"docno": "3174498_1", "text": "or else it would be bitter"},
    {"docno": "1593044_1", "text": "In politics, an independent is a politician who is not affiliated with any political party. In countries with a two-party system, independents may hold a centrist viewpoint between the two parties, or may feel that neither of the two parties adequately represents their viewpoint.. . Other independent candidates are associated with a political party and may be former members of it, but are not able to stand under its label. For instance, after being expelled from the Labour Party but before joining RESPECT, British MP George Galloway described himself as \"Independent Labour\".. . A third category of independents are those who may belong to a political party but believe they can gain an advantage by presenting themselves as being independent of it. This was common among Conservative Party candidates in British local government elections in the mid-twentieth century."},
  ]),
}

class MarkdownFile:
  def __init__(self, path):
    self.path = path

  def render(self):
    with open(self.path) as fin:
      content = fin.read()
      content = content.split('\n---\n')[-1]
      return gr.Markdown(value=content)

class Demo:
  def __init__(self, predict, inputs, settings=[], scale=1):
    self.predict = predict
    self.inputs = inputs
    if not isinstance(inputs, dict):
      self.inputs = {'': inputs}
    self.settings = settings
    self.scale = scale
    self.i = next(counter)

  def load_examples(self, ex_name):
    return self.inputs[ex_name]

  def render(self):
    input = next(iter(self.inputs.values()))
    output = self.predict(input, *[s.value for s in self.settings])
    inputs, outputs = [], []
    with gr.Row().style(equal_height=False):
      with gr.Column(scale=self.scale):
        with gr.Tab('Pipeline Input'):
          inputs.append(gr.Dataframe(
            headers=list(input.columns),
            datatype=[{'i': 'number', 'f': 'number', 'O': 'str'}[t.kind] for t in input.dtypes],
            col_count=(len(input.columns), 'fixed'),
            wrap=True,
            value=input,
          ))
          if len(self.inputs) > 1:
            examples = gr.Dropdown(choices=list(self.inputs), value=next(iter(self.inputs)), label='Example Inputs')
            examples.change(self.load_examples, inputs=[examples], outputs=inputs[0])
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
    submit_btn.click(self.predict, inputs, outputs, api_name=f"predict_{self.i}")

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
