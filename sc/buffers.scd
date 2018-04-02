(
a = Buffer.read(s, "/Users/admin/Documents/BackupGoogleDrive/ConcatenativeSynthesizer/src/snd/chitarra.wav");
b = Buffer.read(s, "/Users/admin/Documents/BackupGoogleDrive/ConcatenativeSynthesizer/src/snd/dataset.wav");
c = Buffer.read(s, "/Users/admin/Documents/BackupGoogleDrive/ConcatenativeSynthesizer/src/snd/fmtest.wav");
d = Buffer.read(s, "/Users/admin/Documents/BackupGoogleDrive/ConcatenativeSynthesizer/src/snd/fmtest2.wav");
e = Buffer.read(s, "/Users/admin/Documents/BackupGoogleDrive/ConcatenativeSynthesizer/src/snd/insects3.wav");
f = Buffer.read(s, "/Users/admin/Documents/BackupGoogleDrive/ConcatenativeSynthesizer/src/snd/me_emb.wav");
g = Buffer.read(s, "/Users/admin/Documents/BackupGoogleDrive/ConcatenativeSynthesizer/src/snd/orchestra.wav");
)
a.bufnum
b.bufnum
c.bufnum
d.bufnum
e.bufnum
f.bufnum
g.bufnum

c.play
c.stop

x.play

Synth(\Grano, [\buf, c, \dur, 0.1, \pos, 44100*1, \amp, 1])


(
SynthDef(\Grano, { | buf, dur, pos, amp, rate=1, pan=0.5, atk=0.5, outCh=20 |
	var play = PlayBuf.ar(1, buf, rate, 1, pos, 0, 0);
	atk = atk.clip(0.0, 1.0);
	play = play * EnvGen.ar(Env.new([0, 1, 0], [dur * atk, dur * (1.0 - atk)]), 1, amp, 0, 1, 2);
	play = PanX.ar(2, play, pan);
	Out.ar(outCh, play);
}).add;
SynthDef(\Reverb, { | inCh=20, outCh=0 |
	var in = In.ar(inCh, 1);
	in = Pan2.ar(in, Lag.ar(LFClipNoise.ar(1), 1));
	Out.ar(0, PucketteReverb.ar(in[0], in[1], fb:0.89));
}).add;
)
Synth.tail(s, \Reverb, [\inCh, 20, \outCh, 0])
s.scope


s.record("/Users/admin/Documents/BackupGoogleDrive/ConcatenativeSynthesizer/test3.wav")
s.stopRecording

NetAddr.langPort