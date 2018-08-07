#!/bin/bash

echo ""
echo "Trying json msg with wrong type.."
curl --silent "http://localhost:80/messages" -X POST -H "Content-Type: application/json" -d '{"message": 100}'
# expect 404 wrong json

echo ""
echo "Trying json msg with missing message field..."
curl --silent "http://localhost:80/messages" -X POST -H "Content-Type: application/json" -d '{"no_msg": "foo"}'
# expect 404 wrong json

echo ""
echo "hashing 'foo' using shasum.."
echo -n "foo" | shasum -a 256 | sed 's/..$//' > foo.shasum
echo "result: "`cat foo.shasum`

echo ""
echo "hashing 'foo' using webapp.."
curl --silent "http://localhost:80/messages" -X POST -H "Content-Type: application/json" -d '{"message": "foo"}' | python -c "import sys, json; print json.load(sys.stdin)['digest']" > foo.webapp
echo "result: "`cat foo.webapp`

# expect 2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae

echo ""
echo "diffing shasum and webapp..."
diff -w foo.shasum foo.webapp
if [ $? == 0 ]
then
    echo "Same"
else
    echo "Different"
fi
rm foo.shasum foo.webapp

echo ""
echo "fetching 2c26b4..'s hashing msg.."
curl --silent "http://localhost:80/messages/2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae"
# expect foo


echo "fetching http://localhost:80/messages/aaaaa..."
curl --silent "http://localhost:80/messages/aaaaa"
# expect 404 message not found