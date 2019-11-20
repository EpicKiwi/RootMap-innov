#! /bin/bash

(
  echo "set datafile separator \";\""
  echo "plot '<tail -n500 positions.csv' using 1:2 with linespoints";
  while :; do sleep .1; echo replot; done
) | gnuplot -persist
