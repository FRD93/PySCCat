(
~ambiDec =  FoaDecoderMatrix.newPanto(Server.local.options.numOutputBusChannels, k:'dual');
~ambiEncS= FoaEncoderMatrix.newStereo;
SynthDef(\Spat, { | inCh=20, outCh=0 |
	var in, out, spat, fft, loud, centr, slope, spread, lagTime=0.5, maxSpeed=3;
	in = In.ar(inCh, 2);
	fft = FFT(LocalBuf(128), in.sum/2, 0.5);
	loud = Loudness.kr(fft) / 64; // range: 0..64
	//loud = SinOsc.ar(loud * maxSpeed, Rand(0.0, 2pi), 0.5, 0.5);
	centr = SpecCentroid.kr(fft) / 15000;
	//centr = SinOsc.ar(centr * maxSpeed, Rand(0.0, 2pi), 0.5, 0.5);
	slope = FFTSlope.kr(fft).neg / 10;
	//slope = SinOsc.ar(slope * maxSpeed, Rand(0.0, 2pi), 0.5, 0.5);
	spread = FFTSpread.kr(fft, centr);
	in = FoaEncode.ar(in, ~ambiEncS);
	in = FoaTransform.ar(in, 'push',        centr, slope, loud);
	in = FoaTransform.ar(in, 'dominate', loud, centr, slope);
	in = FoaTransform.ar(in, 'rtt',           slope, loud, centr);
	Out.ar(outCh, FoaDecode.ar(in, ~ambiDec));
}).add;

)


(
SynthDef(\AnalyzeStream, { | inCh=4, replyFreq=10 |
	//var in = In.ar(inCh, 2).sum;
	var in = SinOsc.ar(4400);
	var amp = Amplitude.kr(in, 0.1, 0.1);
	var fft = FFT(LocalBuf(128), in);
	var centr = SpecCentroid.kr(fft) / 15000;
	var slope = FFTSlope.kr(fft).neg / 10;
	var spread = FFTSpread.kr(fft, centr);
	SendReply.kr(Impulse.kr(replyFreq), cmdName:'/AnalyzeStream/', values:[inCh, amp, centr, slope, spread]);
}).add;
)
Synth(\AnalyzeStream)
OSCdef('ciao', {|msg| msg.postln;}, '/AnalyzeStream/');

s.scope






(
/*
* * ReverbA * *
*
* Presence is directly proportional
* to the amplitude of the input signal.
* Stereo input, stereo output.
*
* Parameters:
* * inCh: input bus
* * outCh: output bus
* * scale: scale the amplitude follower to this value
* * add: add this value to the amplitude follower
*/
SynthDef(\ReverbA, { | inCh=20, outCh=0, scale=1.0, add=0.0 |
	var in, amp, rev;
	in = In.ar(inCh, 2);
	amp = ((Amplitude.ar(in.sum, 0.05, 0.05) * scale) + add).abs.clip(0.0, 1.0);
	rev = PucketteReverb.ar(
		left:in[0],
		right:in[1],
		lp:(amp * 19700) + 300,
		dump:1.0 - amp,
		fb:0.98 - amp.clip(0.0, 0.95),
		wet:1.0 - amp,
		outfilter:(amp * 19700) + 300);
	Out.ar(outCh, rev);
}).add;

/*
* * ReverbB * *
*
* Presence is inversely proportional
* to the amplitude of the input signal.
* Stereo input, stereo output.
*
* Parameters:
* * inCh: input bus
* * outCh: output bus
* * scale: scale the amplitude follower to this value
* * add: add this value to the amplitude follower
*/
SynthDef(\ReverbB, { | inCh=20, outCh=0, scale=1.0, add=0.0 |
	var in, amp, rev;
	in = In.ar(inCh, 2);
	amp = ((Amplitude.ar(in.sum, 0.05, 0.05) * scale) + add).abs.clip(0.0, 1.0);
	rev = PucketteReverb.ar(
		left:in[0],
		right:in[1],
		lp:20000 - ((amp * 19700) + 300),
		dump:amp,
		fb:0.98 - amp.clip(0.0, 0.95),
		wet:amp,
		outfilter:20000 - ((amp * 19700) + 300));
	Out.ar(outCh, rev);
}).add;


/*
* * RedirectStereo * *
*
* Redirect a stereo bus
* to another bus.
* Stereo input, stereo output.
*
* Parameters:
* * inCh: input bus
* * outCh: output bus
*/
SynthDef(\RedirectStereo, { | inCh=20, outCh=10 |
	var in = In.ar(inCh, 2);
	Out.ar(outCh, in);
}).add;
)
















































































