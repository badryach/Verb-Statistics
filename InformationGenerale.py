import spacy
from reportlab.lib.units import inch
from verbecc import Conjugator
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Flowable
from reportlab.lib.pagesizes import letter
import ImportationFichier as LireFichier
from reportlab.platypus import Table, PageBreak, Spacer
from reportlab.platypus import TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import (ParagraphStyle, getSampleStyleSheet)

#Class to draw a line after a paragraphe
class DessinLigne(Flowable):

    def __init__(self, width, height=0):
        Flowable.__init__(self)
        self.width = width
        self.height = height
    def __repr__(self):
        return "Line(w=%s)" % self.width
    def draw(self):

        self.canv.line(0, self.height, self.width, self.height)


# Dictionary of each group
premierGroupe = {}
deuxiemeGroupe = {}
troisiemeGroupe = {}
lg = Conjugator(lang='fr')

# Method  detects conjugation time
def detecterTemps(verbe,verbeRechercher):
        temps = ""
        congugation = lg.conjugate(verbe)
        trouve = False
        for i in congugation.values():
            if type(i) is dict:
                for j in i.values():
                    if type(j) is dict:
                        for k in j.items():
                            if type(k) is tuple:
                                for x in k:
                                    if type(x) is list:
                                        for m in x:
                                            word = str(m).split()
                                            if trouve is not True:
                                                if verbeRechercher == word[-1]:
                                                    trouve = True
                                                    temps = list(j.keys())[list(j.values()).index(x)]
        return temps

# Method returns the verbs of the first second and third group separate as well as the graphs
def detecterVerbe(fichier):

    # Import file
    f=LireFichier.RecupererTextTokenSansPonctuation(fichier)

    # Loading package contents all verbs
    nlp = spacy.load("fr_core_news_sm")
    doc = nlp(f)
    nbrPG=0
    nbrDG = 0
    nbrTG = 0
    frequencePG={}
    frequenceDG={}
    frequenceTG={}
    i=0

    # Method which finds the verbs and puts them in the infinitive to determine the group
    for token in doc:
            if(token.pos_=="VERB") and (token.lemma_[-2:]=="er" or token.lemma_[-2:] == "ir" or token.lemma_[-2:] == "re" \
                    or token.lemma_[-3:] == "oir"):
                congugation = lg.conjugate(token.lemma_)
                if token.lemma_[-2:]=="er":
                    premierGroupe.update({token.text:[token.text,token.lemma_,detecterTemps(token.lemma_,token.text)]})
                    nbrPG += 1
                if token.lemma_[-2:]=="ir" and ''.join(congugation['moods']['participe']['participe-présent'])[-6:] == "issant":
                    deuxiemeGroupe.update({token.text:[token.text,token.lemma_,detecterTemps(token.lemma_,token.text)]})
                    nbrDG += 1
                if (token.lemma_[-2:] == "ir" and ''.join(congugation['moods']['participe']['participe-présent'])[-6:] != "issant") or token.lemma_[-2:] == "re" or token.lemma_[-3:] == "oir":
                    troisiemeGroupe.update({token.text:[token.text,token.lemma_,detecterTemps(token.lemma_,token.text)]})
                    nbrTG += 1

    # Count the frequency of use of each verb in each group
    for elm in premierGroupe.values():
        if elm[1] in frequencePG.keys():
            frequencePG[elm[1]] += 1
        else:
             frequencePG[elm[1]] = 1
    for elm in deuxiemeGroupe.values():
        if elm[1] in frequenceDG.keys():
            frequenceDG[elm[1]] += 1
        else:
            frequenceDG[elm[1]] = 1
    for elm in troisiemeGroupe.values():
        if elm[1] in frequenceTG.keys():
            frequenceTG[elm[1]] += 1
        else:
            frequenceTG[elm[1]] = 1

    # first group graph
    plt.bar(frequencePG.keys(), frequencePG.values(),width = 0.6, color = 'blue',
  edgecolor = 'black', linewidth = 2,ecolor = 'magenta', capsize = 10)
    plt.title("Fréquence utilisation premier groupe")
    plt.xlabel('Verbe')
    plt.ylabel('Fréquence')
    plt.xticks(rotation='vertical')
    plt.tight_layout()
    plt.savefig('grapheP.jpeg')
    plt.clf()
    # Second group graph
    plt.bar(frequenceDG.keys(),frequenceDG.values(),width = 0.6, color = 'orange',
  edgecolor = 'black', linewidth = 2,ecolor = 'magenta', capsize = 10)
    plt.title("Fréquence d'utilisation deuxième groupe")
    plt.xlabel('Verbe')
    plt.ylabel('Fréquence')
    plt.xticks(rotation='vertical')
    plt.tight_layout()
    plt.savefig('grapheD.jpeg')
    plt.clf()

    #Third group graph
    plt.bar(frequenceTG.keys(),frequenceTG.values(), width = 0.6, color = 'green',
  edgecolor = 'black', linewidth = 2,ecolor = 'magenta', capsize = 10)
    plt.title("Fréquence d'utilisation troisième groupe")
    plt.xlabel('Verbe')
    plt.ylabel('Fréquence')
    plt.xticks(rotation='vertical')
    plt.tight_layout()
    plt.savefig('grapheT.jpeg')
    plt.clf()

    # Graph of all groups
    name = ['Premier groupe', 'Deuxième groupe', 'Troisième groupe']
    data = [nbrPG, nbrDG, nbrTG]
    plt.pie(data, labels=name, autopct='%1.1f%%', startangle=90, shadow=True)
    plt.title('Statistique globale')
    plt.axis('equal')
    plt.savefig('grapheG.jpeg')
    plt.clf()

    # save in pdf file
    nomFichier = 'Bilan.pdf'
    pdf = SimpleDocTemplate(
        nomFichier,
        pagesize=letter,
    )

    # table fillings
    colonne = [['verbe', 'infinitif','temps conjugaison']]
    tableColumn = Table(colonne)
    tableP = Table(list(premierGroupe.values()))
    tableD=Table(list(deuxiemeGroupe.values()))
    tableT = Table(list(troisiemeGroupe.values()))

    # add style
    style = TableStyle([
        ('BACKGROUND', (0, 0), (3, 0), colors.green),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

        ('FONTNAME', (0, 0), (-1, 0), 'Courier-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),

        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),

        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ("LINEBELOW", (0, 0), (-1, -1), 1, colors.black)
    ])
    style2 = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),

        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),

        ('BACKGROUND', (0, 0), (0, 0), colors.burlywood),
        ("LINEBELOW", (0, 0), (0, 0),1, colors.black)
    ])
    tableColumn.setStyle(style)
    tableP.setStyle(style2)
    tableD.setStyle(style2)
    tableT.setStyle(style2)

    # Alternate backgroud color
    rowNumbP = len(premierGroupe)
    for i in range(rowNumbP):
        if i % 2 == 0:
            bc = colors.burlywood
        else:
            bc = colors.beige

        tsP = TableStyle(
            [('BACKGROUND', (0, i), (-1, i), bc)]
        )
        tableP.setStyle(tsP)

    rowNumbD = len(deuxiemeGroupe)
    for i in range(rowNumbD):
        if i % 2 == 0:
            bc = colors.burlywood
        else:
            bc = colors.beige

        tsD = TableStyle(
            [('BACKGROUND', (0, i), (-1, i), bc)]
        )
        tableD.setStyle(tsD)

    rowNumbT = len(troisiemeGroupe)
    for i in range(rowNumbT):
        if i % 2 == 0:
            bc = colors.burlywood
        else:
            bc = colors.beige

        tsT = TableStyle(
            [('BACKGROUND', (0, i), (-1, i), bc)]
        )
        tableT.setStyle(tsT)

    # Add borders
    ts = TableStyle(
        [
            ('BOX', (0, 0), (-1, -1), 2, colors.black),

            ('LINEBEFORE', (0, 0), (-1, -1), 2, colors.red),
            ('LINEABOVE', (0, 0), (-1, -1), 2, colors.green),

            ('GRID', (0, 0), (-1, -1), 2, colors.black),
        ]
    )
    tableColumn.setStyle(ts)
    tableP.setStyle(ts)
    tableD.setStyle(ts)
    tableT.setStyle(ts)

    # Add style for title and parapraphe
    sample_style_sheet = getSampleStyleSheet()
    titreStyle = ParagraphStyle('Title',
                               textColor='Blue',
                               fontName="Helvetica-Bold",
                               fontSize=30,
                               parent=sample_style_sheet['Heading1'],
                               alignment=1,
                               spaceAfter=40)
    parapgrapheStyle=ParagraphStyle('Paragraph',
                               fontName="Helvetica",
                               fontSize=14,
                               parent=sample_style_sheet['Heading2'],
                               alignment=0,
                               spaceAfter=0)

    Titre =Paragraph("Statistique des verbes dans un texte ",titreStyle)
    paragraphe_0=Paragraph("Réaliser par : Badr-Eddine Yachou ",ParagraphStyle('Paragraph',
                               fontName="Helvetica",
                               fontSize=14,
                               parent=sample_style_sheet['Heading3'],
                               alignment=2,
                               spaceAfter=0,
                                spaceBefore=350))
    paragraphe_version=Paragraph("Version: 1.0 ",ParagraphStyle('Paragraph',
                               fontName="Helvetica",
                               fontSize=14,
                               parent=sample_style_sheet['Heading3'],
                               alignment=2,
                               spaceAfter=0,
                                spaceBefore=0))
    parapgraphe_presentation=Paragraph("Présentation Générale : ",ParagraphStyle('Paragraph',
                               fontName="Helvetica-Bold",
                               fontSize=20,
                               parent=sample_style_sheet['Heading2'],
                               alignment=0,
                               spaceAfter=5,
                               spaceBefore=0))
    paragraphe_1 = Paragraph("Bonjour à vous et merci d'avoir utilisé cette application "
                            "pour effectuer l'analyse de votre texte voici l'ensemble des verbes "
                            "employé dans le texte découpé dans les trois différents groupes "
                            "Vous trouvez les détails concernant chaque verbe ainsi que la fréquence "
                            "d'utilisation de chacun des verbes ",parapgrapheStyle)
    paragraph_premierG= Paragraph("La liste des verbes du premier groupe: ", parapgrapheStyle)
    paragraph_deuxiemeG = Paragraph("La liste des verbes du deuxième groupe: ", parapgrapheStyle)
    paragraph_troisiemeG = Paragraph("La liste des verbes du troisième groupe: ", parapgrapheStyle)

    # add logo and space
    spacer = Spacer(35, 0.25 * inch)
    logo = Image('logo.png', 2 * inch, 2 * inch)
    # draw a line
    ligne = DessinLigne(500)
    # Add all items to the list
    listeElement = []
    listeElement.append(logo)
    listeElement.append(Titre)
    listeElement.append(paragraphe_0)
    listeElement.append(paragraphe_version)
    listeElement.append(PageBreak())
    listeElement.append(parapgraphe_presentation)
    listeElement.append(ligne)
    listeElement.append(spacer)
    listeElement.append(paragraphe_1)
    listeElement.append(PageBreak())
    listeElement.append(paragraph_premierG)
    listeElement.append(ligne)
    listeElement.append(spacer)
    listeElement.append(tableColumn)
    listeElement.append(tableP)
    listeElement.append(paragraph_deuxiemeG)
    listeElement.append(ligne)
    listeElement.append(spacer)
    listeElement.append(tableColumn)
    listeElement.append(tableD)
    listeElement.append(paragraph_troisiemeG)
    listeElement.append(ligne)
    listeElement.append(spacer)
    listeElement.append(tableColumn)
    listeElement.append(tableT)
    listeElement.append(PageBreak())
    listeElement.append(Image('grapheP.jpeg'))
    listeElement.append(Image('grapheD.jpeg'))
    listeElement.append(Image('grapheT.jpeg'))
    listeElement.append(Image('grapheG.jpeg'))

    # Load the list
    pdf.build(listeElement)

