/////////////////////////////////////////////////////////////////////////////////
// Extract features from sound.
// Copyright (C) 2017  Francesco Roberto Dani
// Mail of the author: f.r.d@hotmail.it
//
// This program is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation; either version 2
// of the License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
/////////////////////////////////////////////////////////////////////////////////

/*
Features:
- Flatness
- HFC
- SpectralComplexity
- Centroid
- Crest
- DistributionShape (spread, skewness and kurtosis)
- Inharmonicity
*/


#include <iostream>
#include <stdlib.h>
#include <essentia/algorithmfactory.h>
#include <essentia/scheduler/network.h>
#include <essentia/streaming/algorithms/poolstorage.h>
#include "credit_libav.h"
#include <string> 

using namespace std;
using namespace essentia;
using namespace essentia::streaming;
using namespace essentia::scheduler;

/*
PARAMETRI ESTERNI:
1) file audio in input (wav, mono)
2) file yaml in output
3) sample rate file input
4) frame size FFT
5) hop size FFT
6) num bands Bark
7) number bands MFCC
8) number coeffs MFCC
9) silence threshold(dB)
*/

int main(int argc, char* argv[]) {
	
  int sr, framesize, hopsize;
  vector<Real> silenceThresholdsArray(1);
  

  if (argc < 6 ) {
    cout << "Error: wrong number of arguments" << endl;
    cout << "Usage: " << argv[0] << " input_audiofile output_yamlfile samplerate(audiofile) framesize(fft) hopsize(fft)" << endl;
    exit(1);
  }
  
	  sr = atoi(argv[3]);
    framesize = atoi(argv[4]);
    hopsize = atoi(argv[5]);
    
  // register the algorithms in the factory(ies)
  essentia::init();

  // instanciate facgory and create algorithms:
  streaming::AlgorithmFactory& factory = streaming::AlgorithmFactory::instance();

  Algorithm* audioload    = factory.create("MonoLoader",
                                           "filename", argv[1],
                                           "sampleRate", sr,
                                           "downmix", "mix");

  Algorithm* frameCutter  = factory.create("FrameCutter",
                                           "frameSize", framesize,
                                           "hopSize", hopsize,
                                           "silentFrames", "noise",
                                           "startFromZero", false );

  Algorithm* window       = factory.create("Windowing", "type", "hann");

  Algorithm* spectrum     = factory.create("Spectrum");
  
  Algorithm* envelope  = factory.create("Envelope",
                                        "applyRectification", true,
                                        "attackTime", 20,
                                        "releaseTime", 20, // 200
                                        "sampleRate", sr);

  Algorithm* flatness    = factory.create("Flatness");

  Algorithm* hfc         = factory.create("HFC",
                                          "sampleRate", sr,
                                          "type", "Masri");

  Algorithm* spec_comp   = factory.create("SpectralComplexity",
                                          "magnitudeThreshold", 0.005,
                                          "sampleRate", sr);

  Algorithm* centroid    = factory.create("Centroid",
                                          "range", real(int(sr / 2)));

  Algorithm* crest       = factory.create("Crest");

  Algorithm* central_mom = factory.create("CentralMoments",
                                          "mode", "sample",
                                          "range", 1);

  Algorithm* dist_shape  = factory.create("DistributionShape");

  Algorithm* spec_peaks  = factory.create("SpectralPeaks",
                                          "minFrequency", 40,
                                          "sampleRate", sr);

  Algorithm* inharm  = factory.create("Inharmonicity");

  // data storage
  Pool pool;








  /////////// CONNECTING THE ALGORITHMS ////////////////
  cout << "-------- connecting algos --------" << endl;
  
  // FRAME CUTTER
  audioload->output("audio")              >>  frameCutter->input("signal");

  // ENVELOPE
  audioload->output("audio")              >>  envelope->input("signal");
  envelope->output("signal")              >>  NOWHERE; //PC(pool, "envelope");

  // CENTROID
  //frameCutter->output("frame")            >>  centroid->input("array");
  //centroid->output("centroid")            >>  PC(pool, "centroid");

  // CENTRAL MOMENTS
  //frameCutter->output("frame")            >>  central_mom->input("array");

  // WINDOWING
  frameCutter->output("frame")            >>  window->input("frame");
 
  // SPECTRUM
  window->output("frame")                 >>  spectrum->input("frame");

  // CENTRAL MOMENTS
  spectrum->output("spectrum")            >>  central_mom->input("array");

  // CENTROID
  spectrum->output("spectrum")            >>  centroid->input("array");
  centroid->output("centroid")            >>  PC(pool, "centroid");

  // FLATNESS
  spectrum->output("spectrum")            >>  flatness->input("array");
  flatness->output("flatness")            >>  PC(pool, "flatness");

  // HFC
  spectrum->output("spectrum")            >>  hfc->input("spectrum");
  hfc->output("hfc")                      >>  PC(pool, "hfc");

  // SPECTRAL COMPLEXITY
  spectrum->output("spectrum")            >>  spec_comp->input("spectrum");
  spec_comp->output("spectralComplexity") >>  NOWHERE; //PC(pool, "spectralComplexity");

  // CREST
  spectrum->output("spectrum")            >>  crest->input("array");
  crest->output("crest")                  >>  PC(pool, "crest");

  // DISTRIBUTION SHAPE
  central_mom->output("centralMoments")   >>  dist_shape->input("centralMoments");
  dist_shape->output("spread")            >>  PC(pool, "spread");
  dist_shape->output("skewness")          >>  PC(pool, "skewness");
  dist_shape->output("kurtosis")          >>  PC(pool, "kurtosis");

  // SPCTRAL PEAKS
  spectrum->output("spectrum")            >>  spec_peaks->input("spectrum");  

  // INHARMONICITY
  spec_peaks->output("magnitudes")        >>  inharm->input("magnitudes");
  spec_peaks->output("frequencies")       >>  inharm->input("frequencies");
  inharm->output("inharmonicity")         >>  PC(pool, "inharmonicity");

  
  






  /////////// STARTING THE ALGORITHMS //////////////////
  cout << "-------- start processing " << argv[1]<< " --------" << endl;

  Network(audioload).run();

  // write results to yamlfile
  cout << "-------- writing results to file " << argv[2] << " --------" << endl;

  //standard::Algorithm* aggregator = standard::AlgorithmFactory::create("PoolAggregator");

  standard::Algorithm* output = standard::AlgorithmFactory::create("YamlOutput",
                                                                   "filename", argv[2],
                                                                   "format", "json");

  Pool poolStats;

  //aggregator->input("input").set(pool);
  //aggregator->output("output").set(poolStats);
  // no media, voglio la raw data:
  //output->input("pool").set(poolStats);
  output->input("pool").set(pool);

  //aggregator->compute();
  output->compute();

  // clean up:
  //deleteNetwork(audioload);
  delete output;
  //delete aggregator;
  essentia::shutdown();

  return 0;
}
