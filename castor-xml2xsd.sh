#!/bin/sh

CLASSPATH=$(build-classpath castor)

java -classpath $CLASSPATH org.exolab.castor.xml.schema.util.XMLInstance2Schema "$@"
