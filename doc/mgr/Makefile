all: mpost latex copy

mpost:
	mpost -interaction=errorstopmode mgr.mp

latex:
	pdflatex -interaction=errorstopmode mgr.tex

copy:
	cp mgr.pdf mj219450.pdf

clean:
	rm -f *.log
	rm -f *.aux
	rm -f *.toc
	rm -f *.out
	rm -f *.mps
	rm -f *.mpx
	rm -f mptextmp.*
	rm -f mpxerr.tex

mrproper: clean
	rm -f mgr.pdf
	rm -f mj219450.pdf
