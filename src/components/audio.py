from pyo import *

class StereoSynth:
    def __init__(self):
        self.server = Server(duplex=0)
        self.server.setOutputDevice(7)
        self.server.boot()

        self.osc1 = Osc(TriangleTable(order=1))
        # self.osc1 = Sine()
        self.osc2 = Sine(freq=500)

        self.server.boot()
        self.mixer = Mixer(1,2)
        self.mixer.addInput(0,self.osc1)
        self.mixer.setAmp(0, 0, 0.5)
        self.mixer.setAmp(0, 1, 0.5)
        self.mixer.addInput(1,self.osc2)
        self.mixer.setAmp(1, 0, 0.5)
        self.mixer.setAmp(1, 1, 0.5)

    def out(self):
        self.mixer.out()
        sp = Spectrum(self.osc1)
        self.server.start().gui(locals())
        return self
    

StereoSynth().out()
example(SincTable)