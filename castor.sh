#!/bin/sh

CLASSPATH=$(build-classpath castor)

java -classpath $CLASSPATH org.exolab.castor.builder.SourceGeneratorMain "$@"
