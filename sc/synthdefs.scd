(
// FX Synth
SynthDef(\Effect1, { | inCh=0, outCh=0, if=7 |
	var in, out, ampfollows, phasers;
	// stereo input
	in = In.ar( inCh, 2 );
	in = Pan2.ar(SinOsc.ar(440,  0, 0.1) * Decay2.ar(Impulse.ar(if))!2, TRand.ar(0.0, 1.0, Impulse.ar(if)));
	// amplitude followers
	ampfollows = Array.fill( 8, { | id |
		Amplitude.ar( in.sum, 2 * ( id + 1 ), 4 * ( id + 1 ) );
	} );
	// phasers
	phasers = Array.fill( 8, { | id |
		CombC.ar( in, 1, ( ampfollows[ id ] * 0.006 * ( id + 1) ) + 0.001, ampfollows[ id ] * ( id + 6 ) ).reverse;
	} ).sum / 8;
	out = in + ( phasers * 0.3 );
	// distorsion
	//out = out.round( ampfollows[ 7 ] * 0.001 ).tanh;
	out = ExpDistorsion.ar( out, 1.0 + ( ampfollows[ 7 ] * 3 ) );


	Out.ar( outCh, out );
}).add;
)

[[1, 2], [2, 3]].sum

a = Synth(\Effect1)
a.set(\if, 5)