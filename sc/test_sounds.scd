(
SynthDef(\WhiteNoiseLPSweep, { | dur=5 |
	var src = WhiteNoise.ar(0.7);
	src = LPF.ar(src, XLine.ar(50, 20000, dur, doneAction:2));
	Out.ar(0, src)
}).add;
SynthDef(\SawtoothLPSweep, { | dur=5 |
	var src = Saw.ar(220, 1);
	var env = EnvGen.ar(Env.new([0, 1, 1, 0], [0.01, dur+0.8, 0.01]), doneAction:2);
	src = BLowPass4.ar(src, Line.ar(220, 220*16, dur));
	//src = LPF.ar(src, Line.ar(220, 220*16, dur));
	Out.ar(0, src*env);
}).add;
SynthDef(\WhiteNoiseBPF, { | dur=5 |
	var src = WhiteNoise.ar(0.7);
	var env = EnvGen.ar(Env.new([0, 1, 1, 0], [0.01, dur+0.8, 0.01]), doneAction:2);
	src = BBandPass.ar(src, SinOsc.ar(0.2, 0, 5000, 5500), 0.05);
	Out.ar(0, src*env)
}).add;
SynthDef(\SineSine, { | dur=5 |
	var src = SinOsc.ar(SinOsc.ar(0.2, 0, 1000, 1500));
	var env = EnvGen.ar(Env.new([0, 1, 1, 0], [0.01, dur+0.8, 0.01]), doneAction:2);
	Out.ar(0, src*env)
}).add;
SynthDef(\Harmonics, { | dur=5 |
	var nharm = 8, maxdev = 0.89;
	var dev = Line.ar(1, maxdev, dur);
	var freqs = (2..nharm);
	var src = SinOsc.ar([440, 440 * 3 * dev].flat).sum /3;
	var env = EnvGen.ar(Env.new([0, 1, 1, 0], [0.01, dur+0.8, 0.01]), doneAction:2);
	Out.ar(0, src*env)
}).add;
SynthDef(\BPFSpread, { | dur=5 |
	var src = BBandPass.ar(WhiteNoise.ar, 1200, XLine.ar(0.001, 1, dur), 1.0-XLine.ar(0.001, 0.9, dur)) * 3;
	var env = EnvGen.ar(Env.new([0, 1, 1, 0], [0.01, dur+0.8, 0.01]), doneAction:2);
	Out.ar(0, src*env)
}).add;
SynthDef(\SkewTest, { | dur=5 |
	var hpfe, lpfe;
	var src;
	var env = EnvGen.ar(Env.new([0, 1, 1, 0], [0.01, dur+0.8, 0.01]), doneAction:2);
	var freqs = [1, 2, 3, 4, 6, 7, 8, 9] * 440;
	src = SinOsc.ar(440 * 5, 0, 1);
	src = BBandPass.ar(WhiteNoise.ar, 1200, 0.01, 10);
	src = src + BBandPass.ar(WhiteNoise.ar, XLine.ar(200, 5000, dur), 0.05, 2);
	Out.ar(0, src*env)
}).add;
SynthDef(\SkewTest, { | dur=5 |
	var hpfe, lpfe;
	var src;
	var env = EnvGen.ar(Env.new([0, 1, 1, 0], [0.01, dur+0.8, 0.01]), doneAction:2);
	var freqs = [1, 2, 3, 4, 6, 7, 8, 9] * 440;
	freqs = (1..100) * 144;
	src = SinOsc.ar(440 * 5, 0, 0.5);
	//src = BBandPass.ar(WhiteNoise.ar, 1200, 0.01, 10);
	src = src + BBandPass.ar(SinOsc.ar(freqs, 0, 1/20).sum, XLine.ar(200, 5000, dur), 0.002, 3);
	Out.ar(0, src*env)
}).add;
SynthDef(\SkewTest, { | dur=5 |
	var hpfe, lpfe;
	var src;
	var env = EnvGen.ar(Env.new([0, 1, 1, 0], [0.01, dur+0.8, 0.01]), doneAction:2);
	src = SinOsc.ar(XLine.ar(110, 15000, dur), 0, 1);
	Out.ar(0, src*env)
}).add;
SynthDef(\KurtTest, { | dur=5 |
	var hpfe, lpfe, mod1, mod2;
	var src;
	var env = EnvGen.ar(Env.new([0, 1, 1, 0], [0.01, dur+0.8, 0.01]), doneAction:2);
	var freqs = [1, 2, 3, 4, 6, 7, 8, 9] * 440;
	freqs = (1..100) * 144;
	hpfe = BHiPass4.ar(WhiteNoise.ar, 1200, 0.2);
	lpfe = BLowPass4.ar(WhiteNoise.ar, 1200, 0.2);
	mod1 = SinOsc.ar(0.5, 0, 1);
	mod2 = SinOsc.ar(0.5, 0).neg;
	hpfe = hpfe * mod1.clip(0.0, 1.0);
	lpfe = lpfe * mod2.clip(0.0, 1.0);

	//src = BBandPass.ar(WhiteNoise.ar, 1200, 0.01, 10);
	src = lpfe+hpfe / 2;
	Out.ar(0, src*env)
}).add;
SynthDef(\KurtTest, { | dur=5 |
	var hpfe, lpfe, mod1, mod2;
	var src;
	var env = EnvGen.ar(Env.new([0, 1, 1, 0], [0.01, dur+0.8, 0.01]), doneAction:2);
	src = Saw.ar(440);
	src = BBandPass.ar(src, 440*4, XLine.ar(0.01, 1, dur), 1-XLine.ar(0.00001, 0.5, dur));
	Out.ar(0, src*env)
}).add;
)
Synth(\WhiteNoiseLPSweep)
Synth(\SawtoothLPSweep)
Synth(\SineSine)
Synth(\Harmonics)
Synth(\BPFSpread)
Synth(\SkewTest)
Synth(\KurtTest)
s.freqscope
s.record

440 * 3
(440 * 3 * 0.89)


s.sendMsg(\b_play, [0])

220*16