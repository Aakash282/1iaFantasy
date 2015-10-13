#!/usr/local/bin/MathematicaScript -script

lst  = ToExpression[$ScriptCommandLine[[2]]];
tsm = TimeSeriesModelFit[lst];
limits = tsm["PredictionLimits"][Length[lst]];
output = TimeSeriesForecast[tsm, 1];
Print /@ {output, limits[[1]], limits[[2]]}
