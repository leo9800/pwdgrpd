#!/bin/sh

{
	cd "$(dirname "$(readlink -f "$0")")";
	rm ./coverage/ -rf;
	rm /tmp/pwdgrpd-test -rf;
	mkdir /tmp/pwdgrpd-test;
	cp ./tests/{passwd,group,db.json} /tmp/pwdgrpd-test -p;
	PYTHONPATH=fsh/:tests/ pytest \
		--cov-report html:coverage/ \
		--cov=pwdgrpd.models \
		./tests/;
	rm /tmp/pwdgrpd-test -rf
}