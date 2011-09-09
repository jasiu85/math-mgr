all:
	pdflatex -interaction batchmode mgr.tex
	cp mgr.pdf mj219450.pdf

clean:
	rm -f mgr.log
	rm -f mgr.aux
	rm -f mgr.toc
	rm -f mgr.out

mrproper: clean
	rm -f mgr.pdf
	rm -f mj219450.pdf
