#!/usr/bin/env python
import os
import logging
import argparse
import json
import numpy as np
import ROOT
import tdrstyle
ROOT.gROOT.SetBatch(True)

parser = argparse.ArgumentParser()
parser.add_argument("--process", type=str, required=True, help="Process name")
parser.add_argument("--debug", action="store_true", default=False, help="debugging mode")
args = parser.parse_args()
logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

WORKDIR = os.getenv("WORKDIR")
PROCESS = args.process

# Load the JSON file
with open(f"{WORKDIR}/results/EvtGen.json")as f:
    data = json.load(f)

# Filter out the process
dataset = {key: data[key] for key in data if PROCESS in key}
# Remove if "MULTIBACKEND" is in the key
dataset = {key: dataset[key] for key in dataset if "MULTIBACKEND" not in key}
logging.debug(f"dataset: {dataset}")

# Make a canvas
canvas = ROOT.TCanvas("canvas", "", 800, 800)
labels = list(dataset.keys())
colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue]
mg = ROOT.TMultiGraph()

for i, (label, dataset) in enumerate(dataset.items()):
    nevt_values = sorted(map(int, dataset.keys()))
    time_values = np.array([dataset[str(nevt)][0] for nevt in nevt_values], dtype='double')
    error_values = np.array([dataset[str(nevt)][1] for nevt in nevt_values], dtype='double')
    nevt_array = np.array(nevt_values, dtype='double')
    zero_array = np.zeros(len(nevt_values), dtype='double')
    
    graph = ROOT.TGraphErrors(len(nevt_values), nevt_array, time_values, zero_array, error_values)
    
    # Set graph style
    graph.SetTitle(label.split("-")[-1])
    graph.SetMarkerColor(colors[i])
    graph.SetMarkerStyle(20+i)
    graph.SetMarkerSize(1.5)
    graph.SetLineColor(colors[i])
    graph.SetLineWidth(2)
    
    mg.Add(graph)

# Set axis labels
mg.GetXaxis().SetTitle("Number of events")
mg.GetXaxis().SetRangeUser(0, 300000)
mg.GetXaxis().SetNoExponent()
mg.GetXaxis().SetMoreLogLabels()
#mg.GetXaxis().SetTitleOffset(1.1)
mg.GetYaxis().SetTitle("Avg. Time (sec)")
# find the maximum value of y
max_y = max([graph.GetY()[i] + graph.GetErrorYhigh(i) for graph in mg.GetListOfGraphs() for i in range(graph.GetN())])
mg.GetYaxis().SetRangeUser(0, max_y * 1.4)
mg.GetYaxis().SetTitleOffset(1.25)

tdrstyle.setTDRStyle()
ROOT.gStyle.SetAxisMaxDigits(3)
canvas.cd()
# Draw with line
mg.Draw("ALP")
legend = canvas.BuildLegend()
legend.SetBorderSize(0)
legend.SetFillStyle(0)
legend.SetX1(0.7)
legend.SetY1(0.75)
legend.SetX2(0.92)
legend.SetY2(0.92)

t = ROOT.gStyle.GetPadTopMargin()
tmpTextSize=0.75*t
latex = ROOT.TLatex()
latex.SetTextSize(tmpTextSize)
textSize = latex.GetTextSize()

#latex.SetTextFont(42)
#latex.SetTextSize(textSize*0.6/0.75)
#latex.DrawLatexNDC(0.845, 0.954, "13.6 TeV")

latex.SetTextFont(61)
latex.SetTextSize(textSize)
latex.DrawLatexNDC(0.202, 0.88, "CMS")

latex.SetTextFont(52)
latex.SetTextSize(textSize*0.76)
latex.DrawLatexNDC(0.202, 0.83, "Simulation")
latex.DrawLatexNDC(0.282, 0.88, "Preliminary")

latex.SetTextFont(42)
latex.SetTextSize(textSize)
latex.DrawLatexNDC(0.25, 0.76, args.process)

output_path = f"{WORKDIR}/plots/BackendComparison_{PROCESS}.pdf"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
canvas.SaveAs(f"{WORKDIR}/plots/BackendComparison_{PROCESS}.pdf")
