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

EX_R = {
  '': pd.DataFrame([
     ['1108939', '4069373', 0, 36.19, 'what slows down the flow of blood', '  As all blood flows back to the heart, clamping down on blood vessels is very important in open heart surgery. Clamping down on blood vessels will slow down blood flow so … that while in surgry, the blood wouldn\'t come in, as it naturally would, and flood the chambers of the heart.'],
     ['1108939', '4744533', 1, 35.87, 'what slows down the flow of blood', 'Several factors combine to bring on an occlusion. The usual situation is that the blood flow in a retinal vein is slowed down and a clot forms. The clot prevents blood from flowing freely. The blood is back logged and spills into the retina. The most common reason for slowed venous blood flow is a hardened artery (arteriosclerosis).'],
     ['1108939', '7454708', 2, 34.21, 'what slows down the flow of blood', 'Congenital heart defects can disrupt the normal flow of blood through the heart. The defect may cause the blood flow to slow down, go in the wrong direction, go to the wrong place, or it may block the flow completely.'],
     ['1108939', '7724054', 3, 33.89, 'what slows down the flow of blood', 'Such discharges occur during a woman’s period and consist of blood that has been either in the vagina or in the uterus. It is normal when these discharges occur closer to the end of a woman’s period when blood flow slows down, or at the beginning, just before blood flow picks up.'],
     ['1108939', '841975', 4, 33.76, 'what slows down the flow of blood', 'Back to TopSymptoms ». Hardening of the arteries does not cause symptoms until blood flow to part of the body becomes slowed or blocked. If the arteries to the heart become narrow, blood flow to the heart can slow down or stop. This can cause chest pain (stable angina), shortness of breath, and other symptoms.'],
     ['1112389', '4337251', 0, 35.4, 'what is the county for grand rapids, mn', 'Find Grand Rapids, MN clerk, including county, city, and circuit clerk, and clerk of court. Clerks x Minnesota x Itasca County x Grand Rapids x.'],
     ['1112389', '4931198', 1, 35.39, 'what is the county for grand rapids, mn', 'Portions of 55744 are also located in Aitkin County. The official US Postal Service name for 55744 is GRAND RAPIDS, Minnesota. Portions of zip code 55744 are contained within or border the city limits of Grand Rapids, MN, Cohasset, MN, La Prairie, MN, and Coleraine, MN. The area code for zip code 55744 is 218.'],
     ['1112389', '8060375', 2, 33.85, 'what is the county for grand rapids, mn', 'Grand Forks Township is a township in Polk County, Minnesota, United States. It is part of the Grand Forks-ND-MN Metropolitan Statistical Area.'],
     ['1112389', '8138768', 3, 33.51, 'what is the county for grand rapids, mn', 'Location. 1  Grand Rapids, MN (83) 2  Deer River, MN (3) 3  Cohasset, MN (3) 4  Remer, MN (2) 5  Warba, MN (1) 6  Hill City, MN (1) 7  Coleraine, MN (1) 8  Itasca County, Mn jobs nationwide.'],
     ['1112389', '8138765', 4, 33.05, 'what is the county for grand rapids, mn', 'Applebee\'s | Apple American Group - 7,516 reviews - Grand Rapids, MN 55744. 1  2083 - Pokegama - Grand Rapids, MN. 2840 S Hwy 169 Grand Rapids, MN - 55744. 2  We have immediate Part Time opportunities available in Grand Rapids, MN .'],
     ['792752', '6571521', 0, 33.05, 'what is ruclip', 'WE WORKED SO HARD FOR THIS GAMEPLAY, PLEASE LEAVE US A LIKE 😭😂 Subscribe for more: ruclip.com/user/tmartn2 Fortnite Battle Royal Playlist: ruclip.com/p/PLwiTZDxPg_I3t0JKZCC5mpVGyPn0b5VKA Expand the description for more Friends in the video: Jimmy: ruclip.com/user/chaosxsilencer Hollow: ruclip.com/user/hollowpoiint Check out my vlog channel: ruclip.com/user/trevandchels Check out my COD channel: ruclip.com/user/TmarTn Follow my primary twitter: twitter.com/TmarTn Follow the TmarTn2 ...'],
     ['792752', '8803596', 1, 31.51, 'what is ruclip', 'Is ruclip.net Safe? Reviews & Ratings ruclip.net Site owners click here. Скачать бесплатно и без регистрации музыкальные клипы, тексты песен звезд Российского шоубизнеса. Site owners click here'],
     ['792752', '8803599', 2, 30.27, 'what is ruclip', 'Ruclip is a fast Youtube video downloader service. Now download videos in all formats from Youtube using Ruclip video downloader. Using Ruclip you can download any type of videos from the Youtube. Using it you can search the videos also and can play them too before downloading. You can even search the episodes and movies and download them.'],
     ['792752', '8803595', 3, 29.17, 'what is ruclip', 'ruclip.net Site owners click here Скачать бесплатно и без регистрации музыкальные клипы, тексты песен звезд Российского шоубизнеса'],
     ['792752', '8803603', 4, 27.59, 'what is ruclip', 'Ruclip is based on super fast script which can handle a number of downloads simultaneously. So you will never any downloading speed issue. So enjoy downloading videos from Youtube using Ruclip and showcase, watch and listen to the ocean of never ending digital video download stream.'],
  ], columns=['qid', 'docno', 'rank', 'score', 'query', 'text'])
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


def code2md(code, COLAB_INSTALL, COLAB_NAME, colab=True):
  if colab:
    return f'''
{code2colab(code, COLAB_INSTALL, COLAB_NAME)}

```python
{code.strip()}
```
'''
  return f'''
```python
{code.strip()}
```
'''
