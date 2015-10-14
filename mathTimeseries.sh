#!/usr/local/bin/MathematicaScript -script

lst  = ToExpression[$ScriptCommandLine[[2]]];
tsm = TimeSeriesModelFit[lst, "ARIMA"];
limits = tsm["PredictionLimits"][Length[lst]];
output = TimeSeriesForecast[tsm, 1];
If[Abs[output] > 1000,
   Print /@ {1000, 1000, 1000} , 
Print /@ {output, limits[[1]], limits[[2]]}]
