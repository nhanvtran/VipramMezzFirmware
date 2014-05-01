import os
import sys

import uhal
import ROOT

from pVIPRAM_inputBuilderClass import *
from pVIPRAM_inputVisualizerClass import *






manager = uhal.ConnectionManager("file://vipram_connections.xml")
hw = manager.getDevice("Mezz1")

